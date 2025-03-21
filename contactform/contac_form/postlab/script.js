const products = [
    { id: 1, name: "Laptop", price: 999.99 },
    { id: 2, name: "Smartphone", price: 499.99 },
    { id: 3, name: "Tablet", price: 299.99 },
    { id: 4, name: "Smartwatch", price: 199.99 },
    { id: 5, name: "Headphones", price: 89.99 }
];

function displayProducts(productList) {
    const productListDiv = document.getElementById('productList');
    productListDiv.innerHTML = ''; 
    productList.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.className = 'product-item';
        productDiv.textContent = `ID: ${product.id}, Name: ${product.name}, Price: $${product.price.toFixed(2)}`;
        productListDiv.appendChild(productDiv);
    });
}

function filterProducts(minPrice) {
    return products.filter(product => product.price >= minPrice);
}

document.getElementById('filterButton').addEventListener('click', () => {
    const minPrice = parseFloat(document.getElementById('minPrice').value);
    if (!isNaN(minPrice)) {
        const filteredProducts = filterProducts(minPrice);
        displayProducts(filteredProducts);
    } else {
        alert("Please enter a valid number for minimum price.");
    }
});

displayProducts(products);