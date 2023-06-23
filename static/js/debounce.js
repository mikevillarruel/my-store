const debounce = (func, timeout = 500) => {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            func(...args)
        }, timeout);

    };
}

const submitForm = (input) => {
    if (input.checkValidity()) {
        input.form.submit();
    }
}

const handleChange = debounce(submitForm);
const handleBlur = (input) => {
    input.reportValidity();
}
