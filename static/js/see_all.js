function toggleFilter(id) {
    const el = document.getElementById(id);
    if (el) {
        el.style.display = el.style.display === 'none' || el.style.display === '' ? 'block' : 'none';
    }
}

function createRangeSlider(sliderId, fromInputId, toInputId, fallbackMin, fallbackMax) {
    const slider = document.getElementById(sliderId);
    const fromInput = document.getElementById(fromInputId);
    const toInput = document.getElementById(toInputId);

    if (!slider || !fromInput || !toInput || typeof noUiSlider === 'undefined') {
        return;
    }

    const min = parseInt(fromInput.min, 10) || fallbackMin;
    const max = parseInt(toInput.max, 10) || fallbackMax;

    noUiSlider.create(slider, {
        start: [parseInt(fromInput.value, 10) || min, parseInt(toInput.value, 10) || max],
        connect: true,
        range: { min, max },
        step: 1,
        tooltips: true,
        format: { to: value => Math.round(value), from: value => Math.round(value) }
    });

    slider.noUiSlider.on('update', (values) => {
        fromInput.value = values[0];
        toInput.value = values[1];
    });

    fromInput.addEventListener('change', () => { slider.noUiSlider.set([fromInput.value, null]); });
    toInput.addEventListener('change', () => { slider.noUiSlider.set([null, toInput.value]); });
}

createRangeSlider('year-slider', 'year-from-input', 'year-to-input', 1300, 2026);
createRangeSlider('price-slider', 'price-from-input', 'price-to-input', 0, 100000);

function handleSort(select) {
    const url = new URL(window.location.href);
    url.searchParams.set('sort', select.value);
    url.searchParams.delete('page');
    window.location.href = url.toString();
}
