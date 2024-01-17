<<<<<<< HEAD
window.onload = function () {
  // ЯКОРЬ НА ЛИД
  const anchors = document.querySelectorAll(".card button");
  const feedback = document.querySelector("#feedback");
  anchors.forEach(function (anchor, index) {
    anchor.addEventListener("click", function () {
      window.scrollTo({
        top: feedback.offsetTop,
        behavior: "smooth",
      });
=======
// ЯКОРЬ НА ЛИД
const anchors = document.querySelectorAll(".card button");
const feedback = document.querySelector("#feedback");
console.log(anchors, feedback);
anchors.forEach(function (anchor, index) {
  anchor.addEventListener("click", function () {
    window.scrollTo({
      top: feedback.offsetTop,
      behavior: "smooth",
>>>>>>> c3dba80874398690668e91293201e358171315f4
    });
  });
};
