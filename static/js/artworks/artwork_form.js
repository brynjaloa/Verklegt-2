document.addEventListener("DOMContentLoaded", function () {
    const categorySelect = document.getElementById("id_category");
    const furnitureDepthField = document.querySelector(".furniture-depth-field");
    const artworkForm = document.querySelector(".artwork-form");

    if (!categorySelect) {
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

    if (artworkForm) {
        artworkForm.addEventListener("keydown", function (event) {
            if (event.key !== "Enter" || event.target.tagName === "TEXTAREA") {
                return;
            }

            event.preventDefault();
            focusNextField(event.target);
        });
    }

    const fields = {
        Paintings: document.querySelector(".painting-field"),
        Sculptures: document.querySelector(".sculpture-field"),
        Furniture: document.querySelector(".furniture-field"),
        Photos: document.querySelector(".photo-field"),
    };

    function setFieldGroupState(field, isVisible) {
        if (!field) {
            return;
        }

        const visibleDisplay = field.classList.contains("form-row") ? "flex" : "grid";
        field.style.display = isVisible ? visibleDisplay : "none";
        field.querySelectorAll("input, select, textarea").forEach(input => {
            input.disabled = !isVisible;
        });
    }

    function hideAllFields() {
        Object.values(fields).forEach(field => {
            setFieldGroupState(field, false);
        });
    }

    function showCorrectField() {
        hideAllFields();

        const selectedCategory = categorySelect.value;

        if (fields[selectedCategory]) {
            setFieldGroupState(fields[selectedCategory], true);
        }

        setFieldGroupState(furnitureDepthField, selectedCategory === "Furniture");
    }

    categorySelect.addEventListener("change", showCorrectField);
    showCorrectField();
});
