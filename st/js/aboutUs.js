// ЭТО ЭФФЕКТ ПОЯВЛЕНИЯ ПРИ ЗАГРУЗКЕ
var elements = document.querySelectorAll("body");

// Определяем анимацию для каждого элемента
elements.forEach(function (element, index) {
  anime({
    targets: element,
    opacity: [0, 1], // Переход от невидимости к видимости
    translateY: [0, 0], // Смещение по оси Y
    easing: "easeInOutQuad",
    duration: 1000,
    delay: index, // Задержка для последовательного запуска анимации для каждого элемента
  });
});
// ЭТО ФУНКЦИОНАЛ МОДАЛКИ ЗАЯВКИ
// Функция открытия модального окна
const openModalApplication = () => {
  const modal = document.getElementById("modal");
  modal.classList.remove("modals-inactive");
  modal.classList.add("modals-active");
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
  document.body.style.overflow = "hidden";
};
// Функция закрытия модального окна
const closeModalApplication = () => {
  const modal = document.getElementById("modal");
  modal.classList.remove("modals-active");
  modal.classList.add("modals-inactive");
  document.body.style.overflow = "auto";
};

// ЭТО ФУНКЦИОНАЛ МОДАЛКИ ГОРОДОВ
const modal = document.getElementById("cities");
// Определяем анимацию
const animationStart = anime({
  targets: modal,
  opacity: [0, 1], // Переход от невидимости к видимости
  translateY: [0, 0], // Смещение по оси Y
  easing: "easeInOutQuad",
  duration: 250,
});
const animationEnd = anime({
  targets: modal,
  opacity: [1, 0], // Переход от невидимости к видимости
  translateY: [0, 0], // Смещение по оси Y
  easing: "easeInOutQuad",
  duration: 250,
});
// Функция открытия модального окна
const openModalCities = () => {
  const modal = document.getElementById("cities");
  if (modal.style.display == "none") {
    modal.style.display = "flex";
    animationStart.restart();
  } else {
    animationEnd.restart();
    setTimeout(() => {
      modal.style.display = "none";
    }, 250);
  }
};
