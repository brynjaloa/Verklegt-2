window.addEventListener("pageshow", function (event) {
    const navigationEntry = performance.getEntriesByType("navigation")[0];
    const restoredFromBackButton = event.persisted || (
        navigationEntry && navigationEntry.type === "back_forward"
    );

    if (restoredFromBackButton) {
        window.location.reload();
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("profile-notification-popup");
    const closeButton = document.getElementById("close-profile-notification");

    if (popup && closeButton) {
        closeButton.addEventListener("click", function () {
            popup.classList.add("hidden");
        });
    }
});
