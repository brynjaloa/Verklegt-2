document.addEventListener("DOMContentLoaded", function () {
    const questions = document.querySelectorAll(".faq-question");

    questions.forEach(question => {
        question.addEventListener("click", function () {
            const answer = question.nextElementSibling;
            const icon = question.querySelector(".faq-icon");
            const videoPanel = document.getElementById(question.dataset.videoId);
            const isOpen = !answer.hidden;

            document.querySelectorAll(".faq-answer").forEach(item => {
                item.hidden = true;
            });

            document.querySelectorAll(".faq-question .faq-icon").forEach(item => {
                item.textContent = "+";
            });

            document.querySelectorAll(".video-panel").forEach(panel => {
                panel.hidden = true;

                const video = panel.querySelector("video");
                if (video) {
                    video.pause();
                }
            });

            if (!isOpen) {
                answer.hidden = false;
                icon.textContent = "-";

                if (videoPanel) {
                    videoPanel.hidden = false;
                }
            }
        });
    });
});
