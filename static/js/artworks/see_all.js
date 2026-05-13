document.addEventListener("DOMContentLoaded", function () {
    const slider = document.getElementById("year-slider");
    const fromInput = document.getElementById("year-from-input");
    const toInput = document.getElementById("year-to-input");

    if (!slider || !fromInput || !toInput || typeof noUiSlider === "undefined") {
        return;
    }

    const minYear = parseInt(fromInput.min, 10) || 1300;
    const maxYear = parseInt(toInput.max, 10) || 2026;

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
});
