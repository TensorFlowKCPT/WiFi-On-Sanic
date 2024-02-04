const create = document.getElementById("create-application");
const sells = document.getElementById("sells-application");
const history = document.getElementById("history-applications");

function createPage() {
  create.style.display = "flex";
  sells.style.display = "none";
  history.style.display = "none";
}
function sellsPage() {
  create.style.display = "none";
  sells.style.display = "flex";
  history.style.display = "none";
}
function historyPage() {
  create.style.display = "none";
  sells.style.display = "none";
  history.style.display = "flex";
}

function PayMeOne(DealId) {
  var PayMeOneButton = document.getElementById('paymeoneid'+DealId)
  PayMeOneButton.disabled = true;

  const data = {
    DealId: DealId,
  };
  fetch("/pay_one", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      location.reload();
    });
}
function PayMeAll() {
  //Здесь код перед отправкой запроса
  var PayMeAllButton = document.getElementById('PayMeAllButton')
  PayMeAllButton.disabled = true;

  fetch("/pay_all", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      location.reload();
    });
}

function sendlead() {
  var address = document.getElementById("address-input").value;
  var phone = document.getElementById("clientNumber-input").value;
  var clientName = document.getElementById("clientName-input").value;
  var sendleadbutton = document.getElementById('send-lead-button');
  //Здесь код перед отправкой запроса
  sendleadbutton.disabled = true;

  const data = {
    Address: address,
    Phone: phone,
    Name: clientName,
  };
  
  fetch("/send_partner_lead", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      location.reload();
    });
}
// КОД ДЛЯ ПОИСКОВИКА
const SearchBox = document.getElementById("address-input");
const url =
  "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address";
const token = "37246a81de5e3317c98fb92126a5e5bf19aae2b2";
function CheckAddress(clicked) {
  var query = document.getElementById("address-input").value;
  const suggestionsContainer = document.getElementById("suggestions-container");
  if (query == "") {
    suggestionsContainer.innerHTML = "";
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
        .suggestions.filter((suggestion) => suggestion.data.fias_level < 10)
        .map((suggestion) => suggestion);
      setSuggestions(suggestions.map((suggestion) => suggestion.value));
    })
    .catch((error) => console.log("error", error));
}
const suggestionsContainer = document.getElementById("suggestions-container");
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
  .getElementById("address-input")
  .addEventListener("oninput", CheckAddress());

// ВАЛИДАЦИЯ ДАННЫХ
const validNumber = () => {
  const inputNumber = document.querySelector("#clientNumber-input");
  var phoneRegex = /^(\+\d{11}|\d{11})$/;
  if (!phoneRegex.test(inputNumber.value)) {
    inputNumber.style.borderColor = "red";
    return false;
  }
  inputNumber.style.borderColor = "rgb(255, 255, 255, 0.09)";
  return true;
};
document
  .querySelector("#clientNumber-input")
  .addEventListener("input", validNumber);
const validName = () => {
  const inputName = document.querySelector("#clientName-input");
  if (inputName.value.length < 2) {
    inputName.style.borderColor = "red";
    return false;
  }
  inputName.style.borderColor = "rgb(255, 255, 255, 0.09)";
  return true;
};
document
  .querySelector("#clientName-input")
  .addEventListener("input", validName);
const validAddress = () => {
  const inputAddress = document.querySelector("#address-input");
  const wrapperInputAddress = document.querySelector(".listInput");
  if (inputAddress.value.length < 2) {
    wrapperInputAddress.style.borderColor = "red";
    return false;
  }
  wrapperInputAddress.style.borderColor = "rgb(255, 255, 255, 0.09)";
  return true;
};
document
  .querySelector("#address-input")
  .addEventListener("input", validAddress);
const allValid = () => {
  const leadButton = document.querySelector(".create button");
  if (validName() && validNumber() && validAddress()) {
    leadButton.disabled = false;
  } else {
    leadButton.disabled = true;
  }
};
document
  .querySelector("#clientNumber-input")
  .addEventListener("input", allValid);
document.querySelector("#clientName-input").addEventListener("input", allValid);
document.querySelector("#address-input").addEventListener("input", allValid);
