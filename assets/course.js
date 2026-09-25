"use strict";
const key = "applied-ai-course-v1";
let completed = [];
try { completed = JSON.parse(localStorage.getItem(key) || "[]"); if (!Array.isArray(completed)) completed = []; } catch { completed = []; }
const moduleId = document.body.dataset.module;
const completion = document.querySelector("#complete");
function renderProgress() {
  const count = new Set(completed.filter(x => /^[1-6]$/.test(x))).size;
  document.querySelector("progress").value = count;
  document.querySelector(".progress-text").textContent = `${count} of 6 modules marked complete`;
  completion.checked = completed.includes(moduleId);
}
completion.addEventListener("change", () => {
  completed = completed.filter(x => x !== moduleId);
  if (completion.checked) completed.push(moduleId);
  try { localStorage.setItem(key, JSON.stringify(completed)); } catch { /* Progress remains available in this page session. */ }
  renderProgress();
});
renderProgress();
// A help link opens its answer; ordinary browsing leaves solutions collapsed.
function revealSolution(hash = location.hash) {
  const target = document.getElementById(hash.slice(1));
  if (target && target.matches("#solutions details")) target.open = true;
}
window.addEventListener("hashchange", () => revealSolution());
document.querySelectorAll('a[href^="#solution-"]').forEach(link => {
  link.addEventListener("click", () => revealSolution(link.hash));
});
revealSolution();
document.querySelectorAll("pre").forEach(pre => {
  const wrapper = document.createElement("div"); wrapper.className = "code-wrap";
  pre.before(wrapper); wrapper.append(pre);
  const button = document.createElement("button"); button.className = "copy"; button.textContent = "Copy";
  button.setAttribute("aria-label", "Copy code to clipboard"); wrapper.append(button);
  button.addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(pre.textContent); button.textContent = "Copied"; }
    catch { button.textContent = "Select and copy"; const range = document.createRange(); range.selectNodeContents(pre); const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range); }
    setTimeout(() => { button.textContent = "Copy"; }, 2000);
  });
});
const topK = document.querySelector("#top-k");
if (topK) {
  const chunks = ["[refund] Course refunds are available until 7 days before the start date.", "[refund-detail] Refund requests go to the course office.", "[schedule] Teaching begins at 09:00.", "[lab] Bring a laptop with Python installed.", "[contact] The library closes at 18:00."];
  topK.addEventListener("input", () => {
    const k = Number(topK.value); document.querySelector("#k-value").value = k;
    document.querySelector("#retrieved").replaceChildren(...chunks.slice(0,k).map(text => { const li=document.createElement("li");li.textContent=text;return li; }));
    document.querySelector("#k-explain").textContent = k === 1 ? "One relevant chunk: focused, but missing the request procedure." : k === 2 ? "Both relevant chunks: the policy and the procedure are covered." : `${k-2} unrelated chunk(s) added: more context consumes tokens without adding evidence for this question.`;
  });
  topK.dispatchEvent(new Event("input"));
}
