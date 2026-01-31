from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Wishlist, WishlistItem
from products.models import ProductSize
from orders.models import Cart, CartItem


# ==================================================
# PRODUCT LIST & DETAIL
# ==================================================

def product_list(request):
    """
    Displays all available products in the store.
    """
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products
    })


def product_detail(request, product_id):
    """
    Displays details of a single product.
    Loads available sizes only if the product has size variations.
    """
    product = get_object_or_404(Product, id=product_id)

    sizes = []
    if product.has_sizes:
        # Related sizes are ordered via ProductSize model meta
        sizes = product.sizes.all()

    return render(request, "products/product_detail.html", {
        "product": product,
        "sizes": sizes,
    })


# ==================================================
# WISHLIST
# ==================================================

@login_required
def add_to_wishlist(request, product_id):
    """
    Adds a product to the user's wishlist.
    Prevents duplicate wishlist items.
    """
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )

    return redirect('products:wishlist')


@login_required
def wishlist_view(request):
    """
    Displays the current user's wishlist items.
    """
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.select_related('product')

    return render(request, 'products/wishlist.html', {
        'wishlist': wishlist,
        'items': items
    })


@login_required
def remove_from_wishlist(request, item_id):
    """
    Removes a specific item from the wishlist.
    """
    item = get_object_or_404(
        WishlistItem,
        id=item_id,
        wishlist__user=request.user
    )
    item.delete()
    return redirect('products:wishlist')


# ==================================================
# MOVE WISHLIST ITEM TO CART
# ==================================================

@login_required
def move_to_cart(request, item_id):
    """
    Moves an item from wishlist to cart.
    If the product has sizes, size selection is required.
    """
    if request.method != "POST":
        messages.error(request, "Invalid request.")
        return redirect("products:wishlist")

    wishlist_item = get_object_or_404(
        WishlistItem,
        id=item_id,
        wishlist__user=request.user
    )
    product = wishlist_item.product
    selected_size = None

    # 🔹 Handle size-based products
    if product.has_sizes:
        selected_size = request.POST.get("size")

        if not selected_size:
            messages.error(request, "Please select a size.")
            return redirect("products:wishlist")

        # Validate selected size stock
        ps = get_object_or_404(
            ProductSize,
            product=product,
            size=selected_size
        )

        if ps.stock <= 0:
            messages.error(request, "Selected size is out of stock.")
            return redirect("products:wishlist")

    # Get or create user's cart
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Ensure uniqueness by (cart, product, size)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=selected_size,
        defaults={"quantity": 1},
    )

    # Increase quantity if item already exists
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Remove item from wishlist after moving to cart
    wishlist_item.delete()

    messages.success(request, "Moved to cart!")
    return redirect("orders:cart")
