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
  animationCards.restart();
  const ProviderFilters = document.querySelectorAll(".providersFilterCheckbox"); // Добавлен точечный селектор перед классом
  const MinTP = parseInt(document.getElementById("input11").value);
  const MaxTP = parseInt(document.getElementById("input12").value);
  const MinTIS = parseInt(document.getElementById("input21").value);
  const MaxTIS = parseInt(document.getElementById("input22").value);
  var activeProviders = [];
  //console.log(ProviderFilters);
  ProviderFilters.forEach((element) => {
    if (element.checked) {
      activeProviders.push(element.name); // Убран доступ к childNodes, так как name прямо доступен у элемента
    }
  });
  var tariffsContainer = document.getElementById("tariffs");
  tariffsContainer?.childNodes.forEach((element) => {
    if (element.nodeType === 1) {
      var providerName = element.dataset.provider;
      var tariffprice = parseInt(element.dataset.price);
      var tis = parseInt(element.dataset.internetspeed);
      element.style.display = "none";
      if (
        (activeProviders.includes(providerName) ||
          activeProviders.length === 0) &&
        MaxTP > tariffprice &&
        MinTP < tariffprice &&
        (Number.isNaN(tis) || (MaxTIS > tis && MinTIS < tis))
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
    min: parseFloat($("#slider-range1").data("min")),
    max: parseFloat($("#slider-range1").data("max")),
    values: [0, 10000],
    slide: function (event, ui) {
      $("#input11").val(ui.values[0]);
      $("#input12").val(ui.values[1]);
      CheckTariffs();
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
    min: parseFloat($("#slider-range2").data("min")),
    max: parseFloat($("#slider-range2").data("max")),
    values: [0, 10000],
    slide: function (event, ui) {
      $("#input21").val(ui.values[0]);
      $("#input22").val(ui.values[1]);
      CheckTariffs();
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

// АНИМАЦИЯ ПРИ ОБНОВЛЕНИИ ФИЛЬТРОВ
const animationCards = anime({
  targets: document.querySelectorAll(".cards"),
  opacity: [0, 1], // Переход от невидимости к видимости
  translateY: [0, 0], // Смещение по оси Y
  easing: "easeInOutQuad",
  duration: 700,
});
