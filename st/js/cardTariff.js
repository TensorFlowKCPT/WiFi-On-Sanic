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
    });
  });
};
