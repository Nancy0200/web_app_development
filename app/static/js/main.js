// 全站互動效果

// 籤筒搖籤動畫
function shakeLot() {
  const bowl = document.getElementById('lot-bowl');
  const btn = document.getElementById('draw-btn');
  if (!bowl || !btn) return;

  bowl.classList.add('shaking');
  btn.disabled = true;
  btn.textContent = '靜心凝神中...';

  setTimeout(() => {
    bowl.classList.remove('shaking');
    document.getElementById('divination-form').submit();
  }, 1600);
}

// 五行條動畫（八字結果頁）
function animateElementBars() {
  const fills = document.querySelectorAll('.element-bar-fill');
  fills.forEach(fill => {
    const target = fill.dataset.width || '0%';
    setTimeout(() => { fill.style.width = target; }, 300);
  });
}

// 歷史紀錄分頁切換
function switchTab(tabName) {
  document.querySelectorAll('.history-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.history-panel').forEach(p => p.classList.remove('active'));
  document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
  document.getElementById(`panel-${tabName}`).classList.add('active');
}

// DOM 載入後執行
document.addEventListener('DOMContentLoaded', () => {
  animateElementBars();

  // 籤筒點擊
  const bowl = document.getElementById('lot-bowl');
  if (bowl) {
    bowl.addEventListener('click', shakeLot);
  }

  // 預設顯示第一個歷史分頁
  const firstTab = document.querySelector('.history-tab');
  if (firstTab) {
    switchTab(firstTab.dataset.tab);
  }
});
