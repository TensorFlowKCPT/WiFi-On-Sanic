window.onload = () => {
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
};
