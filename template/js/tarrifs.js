var elements = document.querySelectorAll("body");

// Определяем анимацию для каждого элемента
elements.forEach(function (element, index) {
  anime({
    targets: element,
    opacity: [0, 1], // Переход от невидимости к видимости
    translateY: [, 0], // Смещение по оси Y
    easing: "easeInOutQuad",
    duration: 500,
    delay: index, // Задержка для последовательного запуска анимации для каждого элемента
  });
});
