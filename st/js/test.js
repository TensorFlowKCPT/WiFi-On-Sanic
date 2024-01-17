const swiper = new Swiper(".swiper", {
  navigation: {
    nextEl: ".right",
    prevEl: ".left",
  },
  slidesPerView: "auto",
  spaceBetween: 40,
  initialSlide: 1,
  loop: true,

  centeredSlides: true,
});
