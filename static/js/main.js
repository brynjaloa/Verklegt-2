document.addEventListener("DOMContentLoaded", function () {
    const queryPreservingForms = document.querySelectorAll("[data-preserve-query]");
    const filterFormSelectors = [
        ".filter-sidebar form",
        ".see-all-filter-sidebar form",
    ];

    function getFilterForm() {
        for (const selector of filterFormSelectors) {
            const filterForm = document.querySelector(selector);

            if (filterForm) {
                return filterForm;
            }
        }

        return null;
    }

    function appendFilterControl(parameters, control) {
        if (!control.name || control.disabled || control.type === "hidden") {
            return;
        }

        if (control.min && control.value === control.min) {
            return;
        }

        if (control.max && control.value === control.max) {
            return;
        }

        if ((control.type === "checkbox" || control.type === "radio") && !control.checked) {
            return;
        }

        if (control.value === "") {
            return;
        }

        parameters.append(control.name, control.value);
    }

    queryPreservingForms.forEach(form => {
        form.addEventListener("submit", function (event) {
            const filterForm = getFilterForm();

            if (!filterForm) {
                return;
            }

            event.preventDefault();

            const parameters = new URLSearchParams();
            const searchInput = form.querySelector("input[name='q']");
            const searchValue = searchInput ? searchInput.value.trim() : "";

            if (searchValue) {
                parameters.set("q", searchValue);
            }

            filterForm
                .querySelectorAll("input, select, textarea")
                .forEach(control => appendFilterControl(parameters, control));

            parameters.delete("page");

            const queryString = parameters.toString();
            window.location.href = `${window.location.pathname}${queryString ? `?${queryString}` : ""}`;
        });
    });
});
