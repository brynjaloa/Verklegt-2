document.addEventListener("DOMContentLoaded", function () {
    const categorySelect = document.getElementById("id_category");

    const fields = {
        Paintings: document.querySelector(".painting-field"),
        Sculptures: document.querySelector(".sculpture-field"),
        Furniture: document.querySelector(".furniture-field"),
        Photos: document.querySelector(".photo-field"),
    };

    function hideAllFields() {
        Object.values(fields).forEach(field => {
            if (field) {
                field.style.display = "none";
            }
        });
    }

    function showCorrectField() {
        hideAllFields();

        const selectedCategory = categorySelect.value;

        if (fields[selectedCategory]) {
            fields[selectedCategory].style.display = "block";
        }
    }

    categorySelect.addEventListener("change", showCorrectField);
    showCorrectField();
});
