$(function () {
  // СОЗДАНИЕ И ОБРАБОТКА ПЕРВОГО СЛАЙДЕРА ЧЕРЕЗ JQUERY
  $("#inputRange1").slider({
    range: true,
    min: parseFloat($("#inputRange1").data("min")),
    max: parseFloat($("#inputRange1").data("max")),
    values: [0, 10000],
    slide: function (event, ui) {
      $("#inputNumber11").val(ui.values[0]);
      $("#inputNumber12").val(ui.values[1]);
      CheckTariffs();
    },
  });

    

  $("#inputNumber11").val($("#inputRange1").slider("values", 0));
  $("#inputNumber12").val($("#inputRange1").slider("values", 1));
  $(".inputNumber").on("input", function () {
    var inputValue = parseFloat($(this).val());
    var inputId = $(this).attr("id");

    // Убедимся, что введенное значение находится в допустимом диапазоне
    if (!isNaN(inputValue)) {
      inputValue = Math.min(10000, Math.max(0, inputValue));

      // Обновим значение слайдера в зависимости от того, к какому инпуту относится изменение
      if (inputId === "inputNumber11") {
        $("#inputRange1").slider("values", 0, inputValue);
      } else if (inputId === "inputNumber12") {
        $("#inputRange1").slider("values", 1, inputValue);
      }
    }
  });
});

$(function () {
  // СОЗДАНИЕ И ОБРАБОТКА ВТОРОГО СЛАЙДЕРА ЧЕРЕЗ JQUERY
  $("#inputRange2").slider({
    range: true,
    min: parseFloat($("#inputRange2").data("min")),
    max: parseFloat($("#inputRange2").data("max")),
    values: [0, 10000],
    slide: function (event, ui) {
      $("#inputNumber21").val(ui.values[0]);
      $("#inputNumber22").val(ui.values[1]);
      CheckTariffs();
    },
  });


  $("#inputNumber21").val($("#inputRange2").slider("values", 0));
  $("#inputNumber22").val($("#inputRange2").slider("values", 1));
  $(".inputNumber").on("input", function () {
    var inputValue = parseFloat($(this).val());
    var inputId = $(this).attr("id");

    // Убедимся, что введенное значение находится в допустимом диапазоне
    if (!isNaN(inputValue)) {
      inputValue = Math.min(10000, Math.max(0, inputValue));

      // Обновим значение слайдера в зависимости от того, к какому инпуту относится изменение
      if (inputId === "inputNumber21") {
        $("#inputRange2").slider("values", 0, inputValue);
      } else if (inputId === "inputNumber22") {
        $("#inputRange2").slider("values", 1, inputValue);
      }
    }
  });
});

function CheckTariffs() {
  const ProviderFilters = document.querySelectorAll(".provider-checkbox");

  const MinTP = parseInt(document.getElementById("inputNumber11").value);
  const MaxTP = parseInt(document.getElementById("inputNumber12").value);
  const MinTIS = parseInt(document.getElementById("inputNumber21").value);
  const MaxTIS = parseInt(document.getElementById("inputNumber22").value);
  var activeProviders = [];
  ProviderFilters.forEach((element) => {
    if (element.checked) {
      activeProviders.push(element.name);
    }
  });
  activeOptions = [];
  const OptionFilters = document.querySelectorAll(".OptionCheckbox");
  OptionFilters.forEach((element) => {
    if (element.checked) {
      activeOptions.push(element.name);
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
        (true)&&(activeProviders.includes(providerName) ||
          activeProviders.length === 0) &&
        MaxTP >= tariffprice &&
        MinTP <= tariffprice &&
        (Number.isNaN(tis) || (MaxTIS >= tis && MinTIS <= tis))
      ) {
        if (activeOptions.length == 0){element.style.display = "block"; return}
        var allOptionsPresent = activeOptions.every(function(Option) {
          return Object.keys(element.dataset).includes(Option);
        });
        if (allOptionsPresent) {
          element.style.display = "block";
        } else {
          element.style.display = "none";
        }
      }
    }
  });
}