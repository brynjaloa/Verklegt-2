document.addEventListener("DOMContentLoaded", function () {
    const carousels = document.querySelectorAll(".recent-carousel");

    if (!carousels.length) {
        return;
    }

    carousels.forEach(carousel => {
        const track = carousel.querySelector(".recent-carousel-track");
        const cards = carousel.querySelectorAll(".art-card");
        const previousButton = carousel.querySelector(".carousel-arrow-left");
        const nextButton = carousel.querySelector(".carousel-arrow-right");
        const visibleCount = parseInt(carousel.dataset.visibleCount, 10) || 4;
        let currentIndex = 0;

        if (!track || !previousButton || !nextButton) {
            return;
        }

        if (cards.length <= visibleCount) {
            previousButton.hidden = true;
            nextButton.hidden = true;
            return;
        }

        function getStepSize() {
            const firstCard = cards[0];
            const secondCard = cards[1];

            if (!firstCard || !secondCard) {
                return 0;
            }

            return secondCard.offsetLeft - firstCard.offsetLeft;
        }

        function updateCarousel() {
            const maxIndex = Math.max(cards.length - visibleCount, 0);
            if (currentIndex < 0) {
                currentIndex = maxIndex;
            } else if (currentIndex > maxIndex) {
                currentIndex = 0;
            }

            track.style.transform = `translateX(-${currentIndex * getStepSize()}px)`;
        }

        previousButton.addEventListener("click", function () {
            currentIndex -= visibleCount;
            updateCarousel();
        });

        nextButton.addEventListener("click", function () {
            currentIndex += visibleCount;
            updateCarousel();
        });

        window.addEventListener("resize", updateCarousel);
        updateCarousel();
    });
});
