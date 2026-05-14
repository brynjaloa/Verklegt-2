function toggleFilter(id) {
    const dropdown = document.getElementById(id);

    if (!dropdown) {
        return;
    }

    dropdown.classList.toggle("is-open");
    const toggle = document.querySelector(`[onclick="toggleFilter('${id}')"]`);

    if (toggle) {
        toggle.classList.toggle("is-open", dropdown.classList.contains("is-open"));
    }
}

function handleSort(select) {
    const url = new URL(window.location.href);
    url.searchParams.set("sort", select.value);
    url.searchParams.delete("page");
    window.location.href = url.toString();
}

document.addEventListener("DOMContentLoaded", function () {
    const slider = document.getElementById("year-slider");
    const fromInput = document.getElementById("year-from-input");
    const toInput = document.getElementById("year-to-input");

    if (slider && fromInput && toInput && typeof noUiSlider !== "undefined") {
        const minYear = parseInt(fromInput.min, 10) || 1300;
        const maxYear = parseInt(toInput.max, 10) || 2025;

        noUiSlider.create(slider, {
            start: [
                parseInt(fromInput.value, 10) || minYear,
                parseInt(toInput.value, 10) || maxYear,
            ],
            connect: true,
            range: { min: minYear, max: maxYear },
            step: 1,
            tooltips: true,
            format: {
                to: value => Math.round(value),
                from: value => Math.round(value),
            },
        });

        slider.noUiSlider.on("update", values => {
            fromInput.value = values[0];
            toInput.value = values[1];
        });

        fromInput.addEventListener("change", () => {
            slider.noUiSlider.set([fromInput.value, null]);
        });

        toInput.addEventListener("change", () => {
            slider.noUiSlider.set([null, toInput.value]);
        });
    }

    document.querySelectorAll(".filter-dropdown").forEach(dropdown => {
        const hasCheckedInput = dropdown.querySelector("input[type='checkbox']:checked");
        const hasChangedNumberInput = Array.from(dropdown.querySelectorAll("input[type='number']")).some(input => {
            if (input.min && input.value === input.min) {
                return false;
            }

            if (input.max && input.value === input.max) {
                return false;
            }

            return Boolean(input.value);
        });

        if (hasCheckedInput || hasChangedNumberInput) {
            dropdown.classList.add("is-open");
            const toggle = document.querySelector(`[onclick="toggleFilter('${dropdown.id}')"]`);

            if (toggle) {
                toggle.classList.add("is-open");
            }
        }
    });
});