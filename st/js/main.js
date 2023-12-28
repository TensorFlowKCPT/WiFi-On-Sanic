const SearchBox = document.getElementById("SearchBox");
const url =
  "http://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address";
const token = "37246a81de5e3317c98fb92126a5e5bf19aae2b2";
function CheckAddress() {
  var query = SearchBox.value;
  const suggestionsContainer = document.getElementById("SuggestionsContainer");
  if (query == "") {
    // Удаляем все дочерние элементы
    while (suggestionsContainer.firstChild) {
      suggestionsContainer.removeChild(suggestionsContainer.firstChild);
    }
  }
  var options = {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Authorization: "Token " + token,
    },
    body: JSON.stringify({ query: query, count: 5 }),
  };
  fetch(url, options)
    .then((response) => response.text())
    .then(async (result) => {
      console.log(JSON.parse(result));
      const suggestions = JSON.parse(result)
        .suggestions.filter((suggestion) => suggestion.data.fias_level < 9)
        .map((suggestion) => suggestion);
      if (
        suggestions[0].value === query &&
        suggestions[0].data.fias_level == 8
      ) {
        window.location.href = "/tariffs?address=" + query;
      }
      setSuggestions(suggestions.map((suggestion) => suggestion.value));
      animationElemetsSearch.restart();
    })
    .catch((error) => console.log("error", error));
}
const suggestionsContainer = document.getElementById("SuggestionsContainer");
function setSuggestions(suggestions) {
  suggestionsContainer.innerHTML = "";
  suggestions.forEach((element) => {
    suggestion = document.createElement("div");
    suggestion.innerHTML = element;
    suggestion.onclick = function () {
      SelectSuggestion(element);
    };
    suggestionsContainer.appendChild(suggestion);
  });
}
function SelectSuggestion(text) {
  SearchBox.value = text;
  CheckAddress();
}

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

// АНИМАЦИИ ДЛЯ ПОИСКА
const animationElemetsSearch = anime({
  targets: document.getElementById("SuggestionsContainer"),
  opacity: [0, 1], // Переход от невидимости к видимости
  translateY: [0, 0], // Смещение по оси Y
  easing: "easeInOutQuad",
  duration: 700,
});
// menuMobile
function menuMobile() {
  var mobileMenu = document.getElementById("mobileMenu");
  mobileMenu.classList.toggle("show");
}
function CheckCity(){
  var city = document.getElementById("cityButton").dataset.city
  if(city==='unknown'){
    console.log('Отправляю свой ip')
  }
}
CheckCity()