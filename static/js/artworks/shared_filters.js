/* global noUiSlider */

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

const priceFormatter = new Intl.NumberFormat("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
});

function parseRangeValue(value, fallbackValue) {
    const parsedValue = parseFloat(String(value).replace(/,/g, ""));

    return Number.isFinite(parsedValue) ? parsedValue : fallbackValue;
}

function formatPlainRangeValue(value) {
    return String(Math.round(value));
}

function formatPriceRangeValue(value) {
    return priceFormatter.format(value);
}

function formatPriceInputWhileEditing(value) {
    const cleanedValue = String(value).replace(/,/g, "");
    const [integerPart, decimalPart] = cleanedValue.split(".");
    const digitsOnlyInteger = integerPart.replace(/\D/g, "");

    if (!digitsOnlyInteger) {
        return "";
    }

    const formattedInteger = new Intl.NumberFormat("en-US", {
        maximumFractionDigits: 0,
    }).format(parseInt(digitsOnlyInteger, 10));

    if (decimalPart === undefined) {
        return formattedInteger;
    }

    return `${formattedInteger}.${decimalPart.replace(/\D/g, "").slice(0, 2)}`;
}

function createRangeSlider(sliderId, fromInputId, toInputId, options = {}) {
    const slider = document.getElementById(sliderId);
    const fromInput = document.getElementById(fromInputId);
    const toInput = document.getElementById(toInputId);

    if (!slider || !fromInput || !toInput || typeof noUiSlider === "undefined") {
        return;
    }

    const minValue = parseInt(fromInput.min, 10) || 0;
    const maxValue = parseInt(toInput.max, 10) || 100;
    const formatValue = options.formatValue || formatPlainRangeValue;

    noUiSlider.create(slider, {
        start: [
            parseRangeValue(fromInput.value, minValue),
            parseRangeValue(toInput.value, maxValue),
        ],
        connect: true,
        range: { min: minValue, max: maxValue },
        step: 1,
        tooltips: true,
        format: {
            to: value => formatValue(value),
            from: value => parseRangeValue(value, minValue),
        },
    });

    slider.noUiSlider.on("update", values => {
        fromInput.value = values[0];
        toInput.value = values[1];
    });

    if (options.formatWhileEditing) {
        fromInput.addEventListener("input", () => {
            fromInput.value = formatPriceInputWhileEditing(fromInput.value);
        });

        toInput.addEventListener("input", () => {
            toInput.value = formatPriceInputWhileEditing(toInput.value);
        });
    }

    fromInput.addEventListener("change", () => {
        slider.noUiSlider.set([parseRangeValue(fromInput.value, minValue), null]);
    });

    toInput.addEventListener("change", () => {
        slider.noUiSlider.set([null, parseRangeValue(toInput.value, maxValue)]);
    });
}

function isDefaultRangeInputValue(input) {
    const value = parseRangeValue(input.value, null);

    if (input.min && value === parseRangeValue(input.min, null)) {
        return true;
    }

    if (input.max && value === parseRangeValue(input.max, null)) {
        return true;
    }

    return false;
}

function openActiveFilterDropdowns() {
    document.querySelectorAll(".filter-dropdown").forEach(dropdown => {
        const hasCheckedInput = dropdown.querySelector("input[type='checkbox']:checked");
        const hasChangedNumberInput = Array.from(dropdown.querySelectorAll("input[type='number'], [data-range-input]")).some(input => {
            if (isDefaultRangeInputValue(input)) {
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
}

function sanitizeFormattedPriceInputs(form) {
    form.querySelectorAll("[data-format='price']").forEach(input => {
        const parsedValue = parseRangeValue(input.value, "");

        if (parsedValue !== "") {
            input.value = parsedValue;
        }
    });
}

function initializeFormattedPriceSubmits() {
    document.querySelectorAll(".filter-sidebar form, .see-all-filter-sidebar form").forEach(form => {
        form.addEventListener("submit", () => sanitizeFormattedPriceInputs(form));
    });
}

function initializeFilterControls() {
    createRangeSlider("year-slider", "year-from-input", "year-to-input");
    createRangeSlider("price-slider", "price-from-input", "price-to-input", {
        formatValue: formatPriceRangeValue,
        formatWhileEditing: true,
    });
    openActiveFilterDropdowns();
    initializeFormattedPriceSubmits();
}
