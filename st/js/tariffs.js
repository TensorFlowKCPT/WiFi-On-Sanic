var currentPage = 1;
var currentPageCount = 0;
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
const tariffsContainer = document.getElementById("tariffs");

document.addEventListener("DOMContentLoaded", CheckTariffs(1));

function CheckTariffs(page) {
  const pagesGroup = document.getElementById("pagesGroup");
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
  var pageNum = 1;
  if (page) {
    pageNum = parseInt(page);
  }

  const data = {
    MinTP: MinTP,
    MaxTP: MaxTP,
    MinTIS: MinTIS,
    MaxTIS: MaxTIS,
    activeProviders: activeProviders,
    activeOptions: activeOptions,
    page: pageNum,
  };
  var currentUrl = window.location.href;
  if (currentUrl.includes("address")) {
    data["adr"] = decodeURIComponent(currentUrl.split("=")[1]);
  } else if (currentUrl.includes("city")) {
    data["cityadd"] = decodeURIComponent(currentUrl.split("=")[1]);
  }

  fetch("/get_tariffs", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      tariffsContainer.innerHTML = "";
      if (data["tariffs"].length != 0) {
        document.getElementById("noTariff").style.display = "none";
      } else {
        document.getElementById("noTariff").style.display = "block";
      }
      data["tariffs"].forEach((tariff) => {
        var card = document.createElement("div");
        card.classList.add("card");
        card.dataset.provider = tariff["Provider"]["Name"];
        card.dataset.price = tariff["Price"];

        if (tariff["Options"]["Internet"]) {
          card.dataset.internetspeed =
            tariff["Options"]["Internet"]["InternetSpeed"];
        }
        if (tariff["Options"]["TV"]) {
          card.dataset.channels = tariff["Options"]["TV"]["Channels"];
        }
        if (tariff["Options"]["Mobile"]) {
          card.dataset.mobile = tariff["Options"]["Mobile"]["гигабайт"];
        }

        var headercard = document.createElement("div");
        headercard.classList.add("header-card");

        var TariffName = document.createElement("span");
        TariffName.innerText = tariff["Name"];
        headercard.appendChild(TariffName);

        card.appendChild(headercard);

        var bodycard = document.createElement("div");
        bodycard.classList.add("body-card");

        var nameAndImg = document.createElement("div");
        nameAndImg.classList.add("nameAndImg");

        var providerName = document.createElement("span");
        providerName.innerText = tariff["Provider"]["Name"];
        nameAndImg.appendChild(providerName);

        var providerImage = document.createElement("img");
        providerImage.src = "/static/img/" + tariff["Provider"]["ImageUrl"];
        providerImage.alt = "";
        nameAndImg.appendChild(providerImage);

        var paramsTariff = document.createElement("div");
        paramsTariff.classList.add("paramsTariff");

        //Скорость интернета
        if (tariff["Options"]["Internet"]) {
          var paramTariffInternet = document.createElement("div");
          paramTariffInternet.classList.add("paramTariff");

          var imgSpeedInternet = document.createElement("img");
          imgSpeedInternet.src = "/static/img/speedInternetTariff.svg";
          imgSpeedInternet.alt = "";
          paramTariffInternet.appendChild(imgSpeedInternet);

          var spanInternetSpeed = document.createElement("span");
          spanInternetSpeed.innerText =
            tariff["Options"]["Internet"]["InternetSpeed"] + " мбит./с.";
          paramTariffInternet.appendChild(spanInternetSpeed);

          paramsTariff.appendChild(paramTariffInternet);
        }

        //Количество каналов
        if (tariff["Options"]["TV"]) {
          var paramTariffTV = document.createElement("div");
          paramTariffTV.classList.add("paramTariff");

          var imgChannels = document.createElement("img");
          imgChannels.src = "/static/img/channelsTariff.svg";
          imgChannels.alt = "";
          paramTariffTV.appendChild(imgChannels);

          var spanChannels = document.createElement("span");
          spanChannels.innerText = tariff["Options"]["TV"]["Channels"];
          paramTariffTV.appendChild(spanChannels);

          paramsTariff.appendChild(paramTariffTV);
        }

        //Мобильный интернет
        if (tariff["Options"]["Mobile"]) {
          var paramTariffMobile = document.createElement("div");
          paramTariffMobile.classList.add("paramTariff");

          var imgMobile = document.createElement("img");
          imgMobile.src = "/static/img/mobileTariff.svg";
          imgMobile.alt = "";
          paramTariffMobile.appendChild(imgMobile);

          var spanMobile = document.createElement("span");
          spanMobile.innerHTML =
            (tariff["Options"]["Mobile"]["гигабайт"]
              ? tariff["Options"]["Mobile"]["гигабайт"] + "Гб "
              : "") +
            (tariff["Options"]["Mobile"]["минут"]
              ? "| " + tariff["Options"]["Mobile"]["минут"] + " минут "
              : "") +
            (tariff["Options"]["Mobile"]["смс"]
              ? "| " + tariff["Options"]["Mobile"]["смс"] + " смс"
              : "");

          paramTariffMobile.appendChild(spanMobile);

          paramsTariff.appendChild(paramTariffMobile);
        }
        //Цена роутера
        if (
          tariff["Options"]["Internet"] &&
          tariff["Options"]["Internet"]["Router"]
        ) {
          var paramTariffRouter = document.createElement("div");
          paramTariffRouter.classList.add("paramTariff");
          var imgRouter = document.createElement("img");
          imgRouter.src = "/static/img/routerTariff.svg";
          imgRouter.alt = "";
          paramTariffRouter.appendChild(imgRouter);

          var spanRouter = document.createElement("span");
          spanRouter.innerHTML =
            "Роутер:<br/>" + tariff["Options"]["Internet"]["Router"];
          paramTariffRouter.appendChild(spanRouter);
          paramsTariff.appendChild(paramTariffRouter);
        }
        //Тв приставка
        if (tariff["Options"]["TV"] && tariff["Options"]["TV"]["TvBox"]) {
          var paramTariffTVBox = document.createElement("div");
          paramTariffTVBox.classList.add("paramTariff");
          var imgTvBox = document.createElement("img");
          imgTvBox.src = "/static/img/routerTariff.svg";
          imgTvBox.alt = "";
          paramTariffTVBox.appendChild(imgTvBox);

          var spanTvBox = document.createElement("span");
          spanTvBox.innerHTML =
            "Тв приставка:<br/>" + tariff["Options"]["TV"]["TvBox"];
          paramTariffTVBox.appendChild(spanTvBox);
          paramsTariff.appendChild(paramTariffTVBox);
        }
        bodycard.appendChild(nameAndImg);
        bodycard.appendChild(paramsTariff);

        card.appendChild(bodycard);

        var footerCard = document.createElement("div");
        footerCard.classList.add("footer-card");

        var footerCard = document.createElement("div");
        footerCard.classList.add("footer-card");

        var textAndImg = document.createElement("div");
        textAndImg.classList.add("textAndImg");

        var spanComparingTo = document.createElement("span");
        spanComparingTo.innerText = "Цена";
        textAndImg.appendChild(spanComparingTo);

        var imgPriceTariff = document.createElement("img");
        imgPriceTariff.src = "/static/img/priceTariff.svg";
        imgPriceTariff.alt = "";
        textAndImg.appendChild(imgPriceTariff);

        footerCard.appendChild(textAndImg);

        var twoPrice = document.createElement("div");
        twoPrice.classList.add("twoPrice");

        var spanPrice = document.createElement("span");
        spanPrice.innerText = tariff["Price"] + " руб";
        twoPrice.appendChild(spanPrice);

        if (tariff["PriceOld"]) {
          var spanOldPrice = document.createElement("span");
          spanOldPrice.innerText = tariff["PriceOld"] + " руб";
          twoPrice.appendChild(spanOldPrice);
        }

        footerCard.appendChild(twoPrice);

        card.appendChild(footerCard);
        var button = document.createElement("button");
        const feedback = document.querySelector("#feedback");
        button.onclick = function () {
          window.scrollTo({
            top: feedback.offsetTop,
            behavior: "smooth",
          });
        };
        button.innerText = "Подключить";
        card.appendChild(button);
        tariffsContainer.appendChild(card);
      });

      pagesGroup.innerHTML = "";
      currentPage = pageNum;
      currentPageCount = data["pages"];
      for (var i = 1; i <= data["pages"]; i++) {
        pagebtn = document.createElement("button");
        pagebtn.classList.add("pageNumber");
        PgNum = document.createElement("span");
        PgNum.innerHTML = i;
        pagebtn.appendChild(PgNum);
        pagebtn.id = i;
        pagebtn.onclick = function () {
          CheckTariffs(this.id);
        };
        if (i === pageNum) {
          pagebtn.classList.add("activePage");
        } else {
          pagebtn.classList.add("unactivePage");
        }
        pagesGroup.appendChild(pagebtn);
      }
    })
    .catch((error) => {
      console.error("Ошибка сети: " + error);
      return;
    });

  tariffsContainer?.childNodes.forEach((element) => {
    if (element.nodeType === 1) {
      var providerName = element.dataset.provider;
      var tariffprice = parseInt(element.dataset.price);
      var tis = parseInt(element.dataset.internetspeed);
      element.style.display = "none";
      if (
        true &&
        (activeProviders.includes(providerName) ||
          activeProviders.length === 0) &&
        MaxTP >= tariffprice &&
        MinTP <= tariffprice &&
        (Number.isNaN(tis) || (MaxTIS >= tis && MinTIS <= tis))
      ) {
        if (activeOptions.length == 0) {
          element.style.display = "block";
          return;
        }
        var allOptionsPresent = activeOptions.every(function (Option) {
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
function ChangePageRight() {
  if (currentPage < currentPageCount) {
    CheckTariffs(currentPage + 1);
  }
}
function ChangePageLeft() {
  if (currentPage > 0) {
    CheckTariffs(currentPage - 1);
  }
}
// ОТКРЫТИЕ И ЗАКРЫТИЕ ДЛЯ ФИЛЬТРОВ
const filtersHeader = document.querySelector(".filters-header");
const filtersBody = document.querySelector(".filters-body");
const filtersRangeHeader = document.querySelectorAll(".filter-price-header");
const filtersRangeBody = document.querySelectorAll(".filter-price-body");
const filtersCheckboxHeader = document.querySelectorAll(".filter-header");
const filtersCheckboxBody = document.querySelectorAll(".filter-body");

// Добавляем обработчик события клика для filtersHeader
filtersHeader.addEventListener("click", () => {
  filtersBody.classList.toggle("filterUnactive");
  filtersBody.classList.toggle("filterActive");
});

// Добавляем обработчик события клика для каждого элемента в filtersRange
filtersRangeHeader.forEach(function (element, number) {
  element.addEventListener("click", () => {
    filtersRangeBody[number].classList.toggle("filterUnactive");
    filtersRangeBody[number].classList.toggle("filterActive");
  });
});

// Добавляем обработчик события клика для каждого элемента в filtersCheckbox
filtersCheckboxHeader.forEach(function (element, number) {
  element.addEventListener("click", () => {
    filtersCheckboxBody[number].classList.toggle("filterUnactive");
    filtersCheckboxBody[number].classList.toggle("filterActive");
  });
});
