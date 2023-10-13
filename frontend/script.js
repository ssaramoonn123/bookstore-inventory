

// Add an event listener to the form submission
document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from submitting

    // Collect form data
    const formData = new FormData(this);

    // Send a POST request to add the book
    fetch('/add_book_route', {  // Update the route to '/add_book'
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Book added successfully!');
            clearForm(); // Clear the form
            updateBookList(data.book); // Add the book to the list
        } else {
            alert('Error adding the book.');
        }
    });
});

// Function to clear the form after submission
function clearForm() {
    document.querySelector('form').reset();
}

// Function to update the book list with a new book
function updateBookList(book) {
    const bookList = document.querySelector('#book-list');

    const bookItem = document.createElement('div');
    bookItem.classList.add('book-item');
    bookItem.innerHTML = `
        <div class="book-details">Title: ${book.Title}</div>
        <div class="book-details">Author: ${book.Author}</div>
        <div class="book-details">Genre: ${book.Genre}</div>
        <div class="book-details">Quantity: ${book.Quantity}</div>
        <div class="book-details">Price: $${book.Price.toFixed(2)}</div>
    `;

    bookList.appendChild(bookItem);
}
