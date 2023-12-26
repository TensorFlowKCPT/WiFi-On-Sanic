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




function CheckTariffs() {
  const ProviderFilters = document.querySelectorAll(".providersFilterCheckbox"); // Добавлен точечный селектор перед классом
  var activeProviders = [];
  //console.log(ProviderFilters);
  ProviderFilters.forEach(element => {
    if (element.checked) {
      activeProviders.push(element.name); // Убран доступ к childNodes, так как name прямо доступен у элемента
    }
  });
  console.log(activeProviders)
  var tariffsContainer = document.getElementById("tariffs");
  // Перебираем все потомки элемента с id "tariffs"
  tariffsContainer?.childNodes.forEach(element => {
    if (element.nodeType === 1) {
      var providerName = element.dataset.provider; // Заменено на dataset.provider
      console.log(providerName)
      element.style.display = "none";
      if (activeProviders.includes(providerName) || activeProviders.length === 0) { // Исправлено условие
        element.style.display = "block";
      }
    }
  });
}
