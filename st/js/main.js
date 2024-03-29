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
var clicker = 0;
var typed = new Typed("#typed-output", options);
// КОД ДЛЯ ПОИСКОВИКА
const SearchBox = document.getElementById("SearchBox");
const url =
  "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address";
const token = "37246a81de5e3317c98fb92126a5e5bf19aae2b2";
function CheckAddress(clicked) {
  var query = document.querySelector(".custom-search input").value;
  const suggestionsContainer = document.querySelector(".custom-listbox");
  if (query == "") {
    // Удаляем все дочерние элементы
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
        (suggestions[0].value == query &&
        suggestions[0].data.fias_level == 8)||(suggestions[0].value == query &&query.includes(", д ")&&clicked)
      ) {
        window.location.href = "/tariffs?address=" + query;
      } else if (
        clicked &&
        (suggestions[0].data.fias_level == 4 ||
          (suggestions[0].value.includes("г ") &&
            !suggestions[0].value.includes(","))) &&
        query == suggestions[0].value
      ) {
        if (clicker === 1) {
          window.location.href = "/tariffs?city=" + query;
        } else {
          clicker++;
        }
      } else {
        clicker = 0;
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
  CheckAddress(true);
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

function setCookie(name, value, days) {
  var expires = "";
  if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

const TermsDiv = document.getElementById('TermsDiv')
document.getElementById('TermsDivButton').addEventListener('click', function () {
  setCookie('Terms',true,100)
  TermsDiv.style.display = 'none'
})

// Функция для получения значения куки по имени
function getCookie(cookieName) {
  // Разбиваем строку cookie на отдельные куки
  var cookies = document.cookie.split(';');
  
  // Проходим по каждому куки
  for(var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i];
      // Удаляем пробелы из начала и конца строки
      cookie = cookie.trim();
      // Проверяем, начинается ли куки с имени, которое мы ищем
      if (cookie.indexOf(cookieName + '=') === 0) {
          // Если да, возвращаем значение куки
          return cookie.substring(cookieName.length + 1);
      }
  }
  // Если куки с указанным именем не найдено, возвращаем пустую строку
  return "";
}

// Пример использования
var TermsCookieValue = getCookie("Terms");
if(TermsCookieValue === 'true'){
  TermsDiv.style.display = 'none'
}