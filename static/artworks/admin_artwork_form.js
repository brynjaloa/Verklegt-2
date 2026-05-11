document.addEventListener("DOMContentLoaded", function () {
    const categorySelect = document.getElementById("id_category");

    if (!categorySelect) {
        return;
    }

    const categoryFields = {
        Paintings: ["painting_medium", "painting_style"],
        Sculptures: ["sculpture_material", "sculpture_style"],
        Furniture: ["furniture_material", "furniture_style"],
        Photos: ["photo_technique", "photo_style"],
    };
    const allFieldNames = Object.values(categoryFields).flat();

    function getFieldRow(fieldName) {
        const field = document.getElementById(`id_${fieldName}`);

        if (!field) {
            return null;
        }

        return field.closest(".form-row") || field.closest(".fieldBox") || field.parentElement;
    }

    function setFieldState(fieldName, isVisible) {
        const field = document.getElementById(`id_${fieldName}`);
        const row = getFieldRow(fieldName);

        if (row) {
            row.style.display = isVisible ? "" : "none";
        }

        if (field) {
            field.disabled = !isVisible;
        }
    }

    function updateCategoryFields() {
        const visibleFieldNames = categoryFields[categorySelect.value] || [];

        allFieldNames.forEach(fieldName => {
            setFieldState(fieldName, visibleFieldNames.includes(fieldName));
        });
    }

    categorySelect.addEventListener("change", updateCategoryFields);
    updateCategoryFields();
});
