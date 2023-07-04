let minPrice = document.querySelector('#min_price');
let maxPrice = document.querySelector('#max_price');
const filtersPanel = document.querySelector('#filters_panel');
const form = document.querySelector('#filters_form');

minPrice.addEventListener('change', () => {
    maxPrice.min = minPrice.value ? minPrice.value : 0;
});

filtersPanel.addEventListener('hidden.bs.offcanvas', function () {
    if (!form.checkValidity()) {
        bootstrap.Offcanvas.getInstance(filtersPanel).show();
        setTimeout(() => {
            form.reportValidity();
        }, 500);
    } else {
        form.submit();
    }
})
