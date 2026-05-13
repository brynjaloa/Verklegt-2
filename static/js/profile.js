document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("profile-notification-popup");
    const closeButton = document.getElementById("close-profile-notification");

    if (popup && closeButton) {
        closeButton.addEventListener("click", function () {
            popup.classList.add("hidden");
        });
    }
});
