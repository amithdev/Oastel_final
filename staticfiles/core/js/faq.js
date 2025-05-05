document.addEventListener("DOMContentLoaded", function () {
  const faqButtons = document.querySelectorAll(".faq-question");

  faqButtons.forEach(button => {
    button.addEventListener("click", () => {
      const answer = button.nextElementSibling;

      // Toggle .show on the answer
      answer.classList.toggle("show");

      // Rotate arrow
      button.classList.toggle("active");
    });
  });
});
