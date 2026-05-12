document.addEventListener("DOMContentLoaded", function () {
    const mainImage = document.getElementById("artwork-main-image");
    const thumbnails = document.querySelectorAll(".artwork-thumbnail");
    const descriptionToggle = document.querySelector(".description-toggle");
    const bidPriceInput = document.querySelector(".bid-price-input");
    const closePopupButton = document.querySelector("[data-close-popup]");

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
            descriptionToggle.textContent = isExpanded ? "See more" : "See less";
        });
    }

    if (closePopupButton) {
        closePopupButton.addEventListener("click", function () {
            const popup = document.getElementById("bid-popup");

            if (popup) {
                popup.classList.add("hidden");
            }
        });
    }

    if (bidPriceInput) {
        function cleanMoneyValue(value) {
            let cleanedValue = "";
            let hasDecimalPoint = false;

            for (const character of value) {
                if (/\d/.test(character)) {
                    cleanedValue += character;
                } else if (character === "." && !hasDecimalPoint) {
                    cleanedValue += character;
                    hasDecimalPoint = true;
                }
            }

            return cleanedValue;
        }

        function countMoneyCharacters(value) {
            return cleanMoneyValue(value).length;
        }

        function formatBidValue(value, shouldPadDecimals = false) {
            const cleanedValue = cleanMoneyValue(value);

            if (!cleanedValue || cleanedValue === ".") {
                return "";
            }

            const hasDecimalPoint = cleanedValue.includes(".");
            const parts = cleanedValue.split(".");
            const wholePart = parts[0] || "0";
            let decimalPart = hasDecimalPoint ? (parts[1] || "").slice(0, 2) : "";
            const formattedWholePart = wholePart.replace(/\B(?=(\d{3})+(?!\d))/g, ",");

            if (shouldPadDecimals) {
                decimalPart = decimalPart.padEnd(2, "0");
            }

            if (hasDecimalPoint || shouldPadDecimals) {
                return `${formattedWholePart}.${decimalPart}`;
            }

            return formattedWholePart;
        }

        function getCursorPositionForMoneyCharacterCount(value, characterCount) {
            if (characterCount <= 0) {
                return 0;
            }

            let seenCharacters = 0;

            for (let index = 0; index < value.length; index += 1) {
                if (/[\d.]/.test(value[index])) {
                    seenCharacters += 1;
                }

                if (seenCharacters >= characterCount) {
                    return index + 1;
                }
            }

            return value.length;
        }

        bidPriceInput.value = formatBidValue(bidPriceInput.value, true);

        bidPriceInput.addEventListener("input", function () {
            const cursorPosition = bidPriceInput.selectionStart || 0;
            const moneyCharactersBeforeCursor = countMoneyCharacters(
                bidPriceInput.value.slice(0, cursorPosition)
            );

            bidPriceInput.value = formatBidValue(bidPriceInput.value);
            bidPriceInput.setSelectionRange(
                getCursorPositionForMoneyCharacterCount(
                    bidPriceInput.value,
                    moneyCharactersBeforeCursor
                ),
                getCursorPositionForMoneyCharacterCount(
                    bidPriceInput.value,
                    moneyCharactersBeforeCursor
                )
            );
        });

        bidPriceInput.addEventListener("blur", function () {
            bidPriceInput.value = formatBidValue(bidPriceInput.value, true);
        });

        if (bidPriceInput.form) {
            bidPriceInput.form.addEventListener("submit", function () {
                bidPriceInput.value = bidPriceInput.value.replace(/,/g, "");
            });
        }
    }
});
