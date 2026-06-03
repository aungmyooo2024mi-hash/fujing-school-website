document.addEventListener("DOMContentLoaded", () => {
  // 汉堡菜单折叠
  const toggleBtn = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav");
  toggleBtn.addEventListener("click", () => {
    nav.style.display = nav.style.display === "block" ? "none" : "block";
  });

  // Banner轮播
  const slides = document.querySelectorAll(".banner-slide");
  let index = 0;
  function showSlide(i) {
    slides.forEach((slide, idx) => {
      slide.classList.toggle("active", idx === i);
    });
  }
  function nextSlide() {
    index = (index + 1) % slides.length;
    showSlide(index);
  }
  showSlide(index);
  setInterval(nextSlide, 4000); // 每4秒切换一次
});
