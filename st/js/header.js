// ЯКОРЬ НА FAQ
const navigateFAQ = document.querySelectorAll(".header a")[2];
const FAQ = document.querySelector("#question");
navigateFAQ.addEventListener("click", function () {
  window.scrollTo({
    top: FAQ.offsetTop,
    behavior: "smooth",
  });
});
// ЯКОРЬ НА ПОПУЛЯРНЫЕ ТАРИФЫ
const navigatePopular = document.querySelectorAll(".header a")[3];
const popularRates = document.querySelector("#popularRates");
navigatePopular.addEventListener("click", function () {
  window.scrollTo({
    top: popularRates.offsetTop,
    behavior: "smooth",
  });
});
// ЯКОРЬ НА КОНТАКТЫ
const navigateContacts = document.querySelectorAll(".header a")[4];
const contacts = document.querySelector("#footer");
navigateContacts.addEventListener("click", function () {
  window.scrollTo({
    top: contacts.offsetTop,
    behavior: "smooth",
  });
});
