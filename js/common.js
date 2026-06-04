document.addEventListener('DOMContentLoaded', () => {

  // 1. 手机端菜单切换逻辑
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');

  menuToggle.addEventListener('click', () => {
    nav.classList.toggle('active'); // 切换显示与隐藏
  });

}); 