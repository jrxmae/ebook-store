from django.shortcuts import render, get_object_or_404, redirect
from .models import Book

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    return render(request, 'store/book_list.html', {'books': books})

# View to display the user's shopping cart
def view_cart(request):
    # Get the current cart data from the session (or an empty dict if none exists)
    cart = request.session.get('cart', {})
    cart_items = [] # Will hold detailed book info for each item in the cart
    total = 0 # Will track the overall cart total

    # Loop through each book ID and quantity in the session cart
    for book_id, quantity in cart.items():
        try:
            book = Book.objects.get(id=book_id) # Get the Book instance from the database
        except Book.DoesNotExist:
            continue # Skip if book was deleted
        subtotal = book.price * quantity # Calculate subtotal for this item

        # Append a dictionary with book info, quantity and subtotal to the cart_items list
        cart_items.append({
            'book': book,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        total += subtotal # Add to the overall total

    # Render the cart page and pass the cart items and total as context
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

# View to handle adding a book to the shopping cart
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = request.session.get('cart', {})

    if str(book_id) in cart:
        cart[str(book_id)] += 1
    else:
        cart[str(book_id)] = 1

    request.session['cart'] = cart
    return redirect('book_list')
