document.addEventListener("DOMContentLoaded", function () {
    const categorySelect = document.getElementById("id_category");
    const categoryGroups = document.querySelectorAll("[data-category-field]");
    const furnitureDepthField = document.querySelector("[data-furniture-depth]");
    const artworkForm = document.querySelector(".artwork-form");

    if (!categorySelect || categoryGroups.length === 0) {
        return;
    }

    function getFocusableFields() {
        if (!artworkForm) {
            return [];
        }

        return Array.from(artworkForm.querySelectorAll("input, select, textarea, button"))
            .filter(field => !field.disabled && field.type !== "hidden" && field.offsetParent !== null);
    }

    function focusNextField(currentField) {
        const focusableFields = getFocusableFields();
        const currentIndex = focusableFields.indexOf(currentField);
        const nextField = focusableFields[currentIndex + 1];

        if (nextField) {
            nextField.focus();
        }
    }

    function setControlsEnabled(container, isEnabled) {
        container.querySelectorAll("input, select, textarea").forEach(control => {
            control.disabled = !isEnabled;

            if (!isEnabled) {
                control.value = "";
            }
        });
    }

    function updateCategoryFields() {
        const selectedCategory = categorySelect.value;

        categoryGroups.forEach(group => {
            const isSelected = group.dataset.categoryField === selectedCategory;

            group.classList.toggle("is-visible", isSelected);
            setControlsEnabled(group, isSelected);
        });

        if (furnitureDepthField) {
            const isFurniture = selectedCategory === "Furniture";

            furnitureDepthField.classList.toggle("is-hidden", !isFurniture);
            setControlsEnabled(furnitureDepthField, isFurniture);
        }
    }

    if (artworkForm) {
        artworkForm.addEventListener("keydown", function (event) {
            if (event.key !== "Enter" || event.target.tagName === "TEXTAREA") {
                return;
            }

            event.preventDefault();
            focusNextField(event.target);
        });
    }

    categorySelect.addEventListener("change", updateCategoryFields);
    updateCategoryFields();
});
