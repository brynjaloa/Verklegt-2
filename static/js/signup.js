document.addEventListener("DOMContentLoaded", function () {
    const usernameInput = document.getElementById("id_username");
    const usernameMessage = document.getElementById("username-message");
    const emailInput = document.getElementById("id_email");
    const emailMessage = document.getElementById("email-message");
    const script = document.querySelector("script[data-check-username-url]");

    if (!usernameInput || !usernameMessage || !emailInput || !emailMessage || !script) {
        return;
    }

    const checkUsernameUrl = script.dataset.checkUsernameUrl;
    const checkEmailUrl = script.dataset.checkEmailUrl;
    let usernameTimeoutId = null;
    let emailTimeoutId = null;

    function setMessage(messageElement, text, className) {
        messageElement.textContent = text;
        messageElement.className = `field-message ${className}`;
    }

    function checkValue(input, messageElement, url, queryName, takenText, availableText) {
        const value = input.value.trim();

        if (!value) {
            setMessage(messageElement, "", "");
            return;
        }

        fetch(`${url}?${queryName}=${encodeURIComponent(value)}`)
            .then(response => response.json())
            .then(data => {
                if (value !== input.value.trim()) {
                    return;
                }

                if (data.exists) {
                    setMessage(messageElement, takenText, "field-message-error");
                } else {
                    setMessage(messageElement, availableText, "field-message-success");
                }
            })
            .catch(() => {
                setMessage(messageElement, "", "");
            });
    }

    usernameInput.addEventListener("input", function () {
        clearTimeout(usernameTimeoutId);
        usernameTimeoutId = setTimeout(function () {
            checkValue(
                usernameInput,
                usernameMessage,
                checkUsernameUrl,
                "username",
                "This username is already in use.",
                "This username is available."
            );
        }, 300);
    });

    emailInput.addEventListener("input", function () {
        clearTimeout(emailTimeoutId);
        emailTimeoutId = setTimeout(function () {
            checkValue(
                emailInput,
                emailMessage,
                checkEmailUrl,
                "email",
                "This email is already in use.",
                "This email is available."
            );
        }, 300);
    });
});
