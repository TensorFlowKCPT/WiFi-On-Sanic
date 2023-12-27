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
  ProviderFilters.forEach((element) => {
    if (element.checked) {
      activeProviders.push(element.name); // Убран доступ к childNodes, так как name прямо доступен у элемента
    }
  });
  console.log(activeProviders);
  var tariffsContainer = document.getElementById("tariffs");
  // Перебираем все потомки элемента с id "tariffs"
  tariffsContainer?.childNodes.forEach((element) => {
    if (element.nodeType === 1) {
      var providerName = element.dataset.provider; // Заменено на dataset.provider
      console.log(providerName);
      element.style.display = "none";
      if (
        activeProviders.includes(providerName) ||
        activeProviders.length === 0
      ) {
        // Исправлено условие
        element.style.display = "block";
      }
    }
  });
}

$(function () {
  // СОЗДАНИЕ И ОБРАБОТКА ПЕРВОГО СЛАЙДЕРА ЧЕРЕЗ JQUERY
  $("#slider-range1").slider({
    range: true,
    min: 0,
    max: 10000,
    values: [0, 10000],
    slide: function (event, ui) {
      $("#input11").val(ui.values[0]);
      $("#input12").val(ui.values[1]);
    },
  });
  $("#input11").val($("#slider-range1").slider("values", 0));
  $("#input12").val($("#slider-range1").slider("values", 1));
  $(".slider-input").on("input", function () {
    var inputValue = parseFloat($(this).val());
    var inputId = $(this).attr("id");

    // Убедимся, что введенное значение находится в допустимом диапазоне
    if (!isNaN(inputValue)) {
      inputValue = Math.min(10000, Math.max(0, inputValue));

      // Обновим значение слайдера в зависимости от того, к какому инпуту относится изменение
      if (inputId === "input11") {
        $("#slider-range1").slider("values", 0, inputValue);
      } else if (inputId === "input12") {
        $("#slider-range1").slider("values", 1, inputValue);
      }
    }
  });
  // СОЗДАНИЕ И ОБРАБОТКА ВТОРОГО СЛАЙДЕРА ЧЕРЕЗ JQUERY
  $("#slider-range2").slider({
    range: true,
    min: 0,
    max: 10000,
    values: [0, 10000],
    slide: function (event, ui) {
      $("#input21").val(ui.values[0]);
      $("#input22").val(ui.values[1]);
    },
  });
  $("#input21").val($("#slider-range2").slider("values", 0));
  $("#input22").val($("#slider-range2").slider("values", 1));
  $(".slider-input").on("input", function () {
    var inputValue = parseFloat($(this).val());
    var inputId = $(this).attr("id");

    // Убедимся, что введенное значение находится в допустимом диапазоне
    if (!isNaN(inputValue)) {
      inputValue = Math.min(10000, Math.max(0, inputValue));

      // Обновим значение слайдера в зависимости от того, к какому инпуту относится изменение
      if (inputId === "input21") {
        $("#slider-range2").slider("values", 0, inputValue);
      } else if (inputId === "input22") {
        $("#slider-range2").slider("values", 1, inputValue);
      }
    }
  });
});
