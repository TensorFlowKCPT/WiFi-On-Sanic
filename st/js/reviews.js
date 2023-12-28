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
  modal.style.display = "block";
  document.body.style.overflow = "hidden";
};

// Функция закрытия модального окна
const closeModalApplication = () => {
  const modal = document.getElementById("modal");
  modal.style.display = "none";
  document.body.style.overflow = "auto";
};
// ЭТО ФУНКЦИОНАЛ МОДАЛКИ ГОРОДОВ
// Функция открытия модального окна
const openModalCities = () => {
  const modal = document.getElementById("cities");
  if (modal.style.display == "none") {
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
};

// menuMobile
function menuMobile() {
  var mobileMenu = document.getElementById("mobileMenu");
  mobileMenu.classList.toggle("show");
}