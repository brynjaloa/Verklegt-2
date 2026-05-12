document.addEventListener("DOMContentLoaded", function () {
    const paymentOptions = document.querySelectorAll("input[name='payment_option']");
    const paymentSections = document.querySelectorAll("[data-payment-fields]");

    function updatePaymentSections() {
        const selectedOption = document.querySelector("input[name='payment_option']:checked");

        if (!selectedOption) {
            return;
        }

        paymentSections.forEach(section => {
            section.hidden = section.dataset.paymentFields !== selectedOption.value;
        });
    }

    paymentOptions.forEach(option => {
        option.addEventListener("change", updatePaymentSections);
    });

    updatePaymentSections();
});
