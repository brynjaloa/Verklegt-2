document.addEventListener("DOMContentLoaded", function () {
    const mainImage = document.getElementById("artwork-main-image");
    const thumbnails = document.querySelectorAll(".artwork-thumbnail");
    const descriptionToggle = document.querySelector(".description-toggle");

    if (mainImage && thumbnails.length > 0) {
        thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener("click", function () {
                mainImage.src = thumbnail.dataset.imageUrl;
                mainImage.alt = thumbnail.dataset.imageAlt;

                thumbnails.forEach(item => item.classList.remove("is-active"));
                thumbnail.classList.add("is-active");
            });
        });
    }

    if (descriptionToggle) {
        descriptionToggle.addEventListener("click", function () {
            const description = descriptionToggle.closest(".artwork-short-description");
            const shortText = description.querySelector(".description-short");
            const fullText = description.querySelector(".description-full");
            const isExpanded = descriptionToggle.dataset.expanded === "true";

            shortText.hidden = !isExpanded;
            fullText.hidden = isExpanded;
            descriptionToggle.dataset.expanded = isExpanded ? "false" : "true";
            descriptionToggle.textContent = isExpanded ? "See more..." : "See less";
        });
    }
});
