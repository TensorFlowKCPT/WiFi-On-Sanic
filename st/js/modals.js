// ЦВЕТ ДЛЯ АКТИВНЫХ КНОПОК
function changeRoom(button) {
  // Удаление класса 'active-typeRoom' у всех кнопок
  var buttons = document.querySelectorAll(".typeRooms button");
  buttons.forEach(function (btn) {
    btn.classList.remove("active-typeRoom");
    btn.classList.add("unactive-typeRoom");
  });

  // Добавление класса 'active-typeRoom' к выбранной кнопке
  button.classList.remove("unactive-typeRoom");
  button.classList.add("active-typeRoom");
}
const typeRoomsButton = document.querySelectorAll(".typeRooms button");
typeRoomsButton.forEach(function (btn) {
  btn.addEventListener("click", function () {
    changeRoom(btn);
  });
});
// ОТПРАВКА И ПРОВЕРКА ЛИДА В CRM
// проверка номера телефона
const validNumber = () => {
  const inputNumber = document.querySelectorAll(
    ".inputs-data-feedback input"
  )[1];
  var phoneRegex = /^\+\d{11}$/;
  if (!phoneRegex.test(inputNumber.value)) {
    inputNumber.classList.remove("validInput");
    inputNumber.classList.add("unvalidInput");
    return false;
  }
  inputNumber.classList.remove("unvalidInput");
  inputNumber.classList.add("validInput");
  return true;
};
document
  .querySelectorAll(".inputs-data-feedback input")[1]
  .addEventListener("input", validNumber);
// проверка имени
const validName = () => {
  const inputName = document.querySelectorAll(".inputs-data-feedback input")[0];
  if (inputName.value.length < 2) {
    inputName.classList.remove("validInput");
    inputName.classList.add("unvalidInput");
    return false;
  }
  inputName.classList.remove("unvalidInput");
  inputName.classList.add("validInput");
  return true;
};
document
  .querySelectorAll(".inputs-data-feedback input")[0]
  .addEventListener("input", validName);
// проверка адреса подкючения
const validAddress = () => {
  const inputAddress = document.querySelector(".inputs-data-feedback textarea");
  if (!inputAddress.value) {
    inputAddress.classList.remove("validInput");
    inputAddress.classList.add("unvalidInput");
    return false;
  }
  inputAddress.classList.remove("unvalidInput");
  inputAddress.classList.add("validInput");
  return true;
};
document
  .querySelector(".inputs-data-feedback textarea")
  .addEventListener("input", validAddress);
// полная проверка перед отправкой
const allValidInput = () => {
  const checkBoxData = document.querySelector(".custom-checkbox input");
  const buttonLead = document.querySelector(".checkAndSubmit button");
  console.log(checkBoxData.checked);
  if (validName() && validNumber() && validAddress() && checkBoxData.checked) {
    buttonLead.disabled = false;
  } else {
    buttonLead.disabled = true;
  }
};
document
  .querySelectorAll(".inputs-data-feedback input")[1]
  .addEventListener("input", allValidInput);
document
  .querySelectorAll(".inputs-data-feedback input")[0]
  .addEventListener("input", allValidInput);
document
  .querySelector(".inputs-data-feedback textarea")
  .addEventListener("input", allValidInput);
document
  .querySelector(".custom-checkbox input")
  .addEventListener("change", allValidInput);
