let slides = document.querySelectorAll(".banner-slide");
let currentSlide = 0;

function showNextSlide() {
  slides[currentSlide].classList.remove("active");
  currentSlide = (currentSlide + 1) % slides.length;
  slides[currentSlide].classList.add("active");
}

// Change slide every 3 seconds
setInterval(showNextSlide, 3000);
