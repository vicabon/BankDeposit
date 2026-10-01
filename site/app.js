const DATA_URL = "./latest.json";
const text = (value) => value || "官方資料未載明";

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[char]));
}

function planRows(banks) {
  const plans = banks.flatMap((bank) => (bank.plans || []).map((plan) => ({ ...plan, bank: bank.bank })));
  if (!plans.length) return '<tr><td colspan="7" class="muted">目前尚未取得可呈現的官方方案資料；這不代表銀行目前沒有方案。</td></tr>';
  return plans.map((plan) => `<tr><td>${esc(plan.bank)}</td><td>${esc(plan.product_name)}</td><td>${esc(plan.annual_rate)}</td><td>${esc(plan.term)}</td><td>${esc(plan.minimum_amount)}～${esc(plan.maximum_amount)}</td><td>${esc(plan.interest_payment)}</td><td>${plan.official_url ? `<a href="${esc(plan.official_url)}" rel="noopener noreferrer">官方連結</a>` : "官方網址未取得"}</td></tr>`).join("");
}

function render(data) {
  const banks = data.banks || [];
  const plans = banks.flatMap((bank) => bank.plans || []);
  document.querySelector("#generatedAt").textContent = data.generated_at || "官方資料未載明";
  document.querySelector("#dataNotice").textContent = `${text(data.data_status)}。最近資料版本不代表銀行即時承作保證。`;
  document.querySelector("#summary").innerHTML = `<div class="card"><strong>${plans.length}</strong><span>已載入方案</span></div><div class="card"><strong>${banks.length}</strong><span>指定銀行</span></div><div class="card"><strong>${esc(data.timezone)}</strong><span>時間基準</span></div>`;
  document.querySelector("#plans").innerHTML = planRows(banks);
  document.querySelector("#banks").innerHTML = banks.map((bank) => `<article class="card"><strong>${esc(bank.bank)}</strong><div>${esc(bank.search_status)}</div><div class="muted">最近成功校對：${esc(bank.last_successful_check_at || "官方資料未載明")}</div><div class="muted">${esc((bank.notes || []).join(" "))}</div></article>`).join("");
}

async function loadData() {
  const notice = document.querySelector("#dataNotice");
  notice.textContent = "正在讀取資料…";
  try { const response = await fetch(`${DATA_URL}?v=${Date.now()}`); if (!response.ok) throw new Error(`HTTP ${response.status}`); render(await response.json()); }
  catch (error) { notice.textContent = `資料目前無法讀取：${error.message}。請確認 latest.json 已發布。`; }
}

document.querySelector("#reload").addEventListener("click", loadData);
loadData();
