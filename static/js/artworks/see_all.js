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

function createRangeSlider(sliderId, fromInputId, toInputId) {
    const slider = document.getElementById(sliderId);
    const fromInput = document.getElementById(fromInputId);
    const toInput = document.getElementById(toInputId);

    if (!slider || !fromInput || !toInput || typeof noUiSlider === "undefined") {
        return;
    }

    const minValue = parseInt(fromInput.min, 10) || 0;
    const maxValue = parseInt(toInput.max, 10) || 100;

    noUiSlider.create(slider, {
        start: [
            parseInt(fromInput.value, 10) || minValue,
            parseInt(toInput.value, 10) || maxValue,
        ],
        connect: true,
        range: { min: minValue, max: maxValue },
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

document.addEventListener("DOMContentLoaded", function () {
    createRangeSlider("year-slider", "year-from-input", "year-to-input");
    createRangeSlider("price-slider", "price-from-input", "price-to-input");

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
