// ЭТО ЭФФЕКТ ПОЯВЛЕНИЯ ПРИ ЗАГРУЗКЕ
const animeBody = anime({
  targets: document.querySelector("body"),
  opacity: [0, 1], // Переход от невидимости к видимости
  translateY: [0, 0], // Смещение по оси Y
  easing: "easeInOutQuad",
  duration: 1000,
});

// ЭФФЕКТ ПЕЧАТНОЙ МАШИНКИ
var options = {
  strings: ["интернет", "телевидение", "связь"], // Замените это на свои фразы
  typeSpeed: 130,
  backSpeed: 50,
  backDelay: 1000,
  startDelay: 500,
  loop: true,
};

var typed = new Typed("#typed-output", options);
// КОД ДЛЯ ПОИСКОВИКА
const SearchBox = document.getElementById("SearchBox");
const url ="https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address";
const token = "37246a81de5e3317c98fb92126a5e5bf19aae2b2";
function CheckAddress() {
  var query = document.querySelector(".custom-search input").value;
  const suggestionsContainer = document.querySelector(".custom-listbox");
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
document
  .querySelector(".custom-search input")
  .addEventListener("oninput", CheckAddress());
// КОД СЛАЙДЕРА
const swiper = new Swiper(".swiper", {
  navigation: {
    nextEl: ".rightSliderButton",
    prevEl: ".leftSliderButton",
  },
  slidesPerView: "auto",
  spaceBetween: 40,
  initialSlide: 1,
  loop: true,

  centeredSlides: true,
});
// КОД ВОПРОСОВ
function toggleAccordion(question) {
  if (question.classList.contains("question-unactive")) {
    question.classList.remove("question-unactive");
    question.classList.add("question-active");
  } else {
    question.classList.remove("question-active");
    question.classList.add("question-unactive");
  }
}
const questions = document.querySelectorAll(".question");
// Добавляем слушатели событий для каждого элемента
questions.forEach(function (question, index) {
  question.addEventListener("click", function () {
    toggleAccordion(question);
  });
});

