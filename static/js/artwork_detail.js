document.addEventListener("DOMContentLoaded", function () {
    const mainImage = document.getElementById("artwork-main-image");
    const thumbnails = document.querySelectorAll(".artwork-thumbnail");

    if (!mainImage || thumbnails.length === 0) {
        return;
    }

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener("click", function () {
            mainImage.src = thumbnail.dataset.imageUrl;
            mainImage.alt = thumbnail.dataset.imageAlt;

            thumbnails.forEach(item => item.classList.remove("is-active"));
            thumbnail.classList.add("is-active");
        });
    });
});
