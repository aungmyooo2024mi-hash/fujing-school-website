document.addEventListener('DOMContentLoaded', () => {

  /* ==========================================================================
     1. 手机端菜单切换逻辑
     ========================================================================== */
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');

  if (menuToggle && nav) {
    menuToggle.addEventListener('click', (e) => {
      nav.classList.toggle('active');
      // 阻止事件冒泡，防止点击按钮时直接触发下方的 document 点击关闭事件
      e.stopPropagation();
    });

    // 💡 体验优化：点击页面其他任何地方时，自动收起手机端菜单
    document.addEventListener('click', () => {
      if (nav.classList.contains('active')) {
        nav.classList.remove('active');
      }
    });
  }


  /* ==========================================================================
     2. 全功能轮播图逻辑 (含自动播放、前后切换、圆点同步、悬停暂停)
     ========================================================================== */
  const banner = document.querySelector('.banner');
  const slides = document.querySelectorAll('.banner-slide');
  const dots = document.querySelectorAll('.banner-dots .dot');
  const prevBtn = document.querySelector('.banner-prev');
  const nextBtn = document.querySelector('.banner-next');

  // 安全检查：确保页面上确实存在轮播图组件再执行
  if (slides.length > 0) {
    let currentSlide = 0;
    let slideTimer = null;
    const slideInterval = 4000; // 每 4 秒换一张图

    // 核心切换函数
    function goToSlide(index) {
      // 1. 移除当前所有激活状态
      slides[currentSlide].classList.remove('active');
      if (dots.length > 0) dots[currentSlide].classList.remove('active');

      // 2. 更新当前索引值
      currentSlide = index;

      // 3. 为目标图片和对应圆点添加激活状态
      slides[currentSlide].classList.add('active');
      if (dots.length > 0) dots[currentSlide].classList.add('active');
    }

    // 下一张
    function handleNext() {
      const nextIndex = (currentSlide + 1) % slides.length;
      goToSlide(nextIndex);
    }

    // 上一张
    function handlePrev() {
      const prevIndex = (currentSlide - 1 + slides.length) % slides.length;
      goToSlide(prevIndex);
    }

    // 定时器控制：启动
    function startTimer() {
      if (!slideTimer) {
        slideTimer = setInterval(handleNext, slideInterval);
      }
    }

    // 定时器控制：停止
    function stopTimer() {
      if (slideTimer) {
        clearInterval(slideTimer);
        slideTimer = null;
      }
    }

    /* --- 事件监听 --- */

    // 左右按钮点击事件（加入定时器重置）
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        stopTimer();
        handleNext();
        startTimer();
      });
    }
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        stopTimer();
        handlePrev();
        startTimer();
      });
    }

    // 底部圆点点击切换事件（加入定时器重置）
    dots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        stopTimer();
        goToSlide(index);
        startTimer();
      });
    });

    // 💡 体验优化：鼠标移入轮播图区域暂停自动播放，移出后恢复
    if (banner) {
      banner.addEventListener('mouseenter', stopTimer);
      banner.addEventListener('mouseleave', startTimer);
    }


    // 初始化启动自动播放
    startTimer();
  }
});