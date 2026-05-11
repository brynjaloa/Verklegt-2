document.addEventListener("DOMContentLoaded", function () {
    const categorySelect = document.getElementById("id_category");

    if (!categorySelect) {
        return;
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

        field.style.display = isVisible ? "block" : "none";
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
    }

    categorySelect.addEventListener("change", showCorrectField);
    showCorrectField();
});
