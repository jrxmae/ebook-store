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

# View funciton to remove a book from the shopping cart based on its ID
def remove_from_cart(request, book_id):
    cart = request.session.get('cart', {})

    # Decrease quantity of books in cart or remove if only one is left
    if str(book_id) in cart:
        if cart[str(book_id)] > 1:
            cart[str(book_id)] -= 1 
        else:
            cart.pop(str(book_id)) 

    request.session['cart'] = cart
    return redirect('view_cart')

# View to increase quantity of a book in the cart
def increase_quantity(request, book_id):
    cart = request.session.get('cart', {})
    if str(book_id) in cart:
        cart[str(book_id)] += 1
    request.session['cart'] = cart
    return redirect('view_cart')

# View to decrease quantity of a book in the cart
def decrease_quantity(request, book_id):
    cart = request.session.get('cart', {})
    if str(book_id) in cart:
        if cart[str(book_id)] > 1:
            cart[str(book_id)] -= 1
        else:
            cart.pop(str(book_id))
    request.session['cart'] = cart
    return redirect('view_cart')

from django.contrib import messages

def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    # Loop through cart dict
    for book_id, quantity in cart.items():
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            continue
        subtotal = book.price * quantity
        cart_items.append({
            'book': book,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal

    # A fake checkout - no payment, clears cart afterwards
    if request.method == 'POST':
        request.session['cart'] = {}
        messages.success(request, "Thank you for your purchase!")
        return redirect('book_list')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })