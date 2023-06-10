const input = document.querySelector("#input")
const output = document.querySelector("#output")
let imagesArray = []

input.addEventListener("change", () => {
    const files = input.files
    imagesArray = []

    for (let i = 0; i < files.length; i++) {
        imagesArray.push(files[i])
    }

    displayImages()
})

function displayImages() {
    let images = ""

    imagesArray.forEach((image, index) => {
        images += `<div class="p-1 d-flex flex-column">
                <img src="${URL.createObjectURL(image)}" alt="image ${index}" height="200px">
              </div>`
    })

    if (images) {
        images = `<div class="d-flex flex-row overflow-x-auto form-control my-2">${images}</div>`
    }

    output.innerHTML = images
}
