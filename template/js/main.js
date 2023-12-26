// ЭТО ЭФФЕКТ ПЕЧАТНОЙ МАШИНКИ
var options = {
  strings: ["интернет", "телевидение", "связь"], // Замените это на свои фразы
  typeSpeed: 130,
  backSpeed: 50,
  backDelay: 1000,
  startDelay: 500,
  loop: true,
};

var typed = new Typed("#typed-output", options);

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
