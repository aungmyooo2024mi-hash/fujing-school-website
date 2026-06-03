document.addEventListener('DOMContentLoaded', () => {

  // 1. 手机端菜单切换逻辑
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');

  menuToggle.addEventListener('click', () => {
    nav.classList.toggle('active'); // 切换显示与隐藏
  });

  // 2. 简易轮播图自动播放逻辑
  const slides = document.querySelectorAll('.banner-slide');
  let currentSlide = 0;
  const slideInterval = 4000; // 每 4 秒换一张图

  function nextSlide() {
    // 移除当前图片的 active 状态
    slides[currentSlide].classList.remove('active');
    // 计算下一张图的索引
    currentSlide = (currentSlide + 1) % slides.length;
    // 为下一张图加上 active 状态
    slides[currentSlide].classList.add('active');
  }

  // 启动定时器
  setInterval(nextSlide, slideInterval);
});