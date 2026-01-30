from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Product, Wishlist, WishlistItem
from orders.models import Cart, CartItem
from django.contrib import messages
from products.models import ProductSize, Product
# Create your views here.
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    sizes = []
    if product.has_sizes:
        sizes = product.sizes.all()  # ProductSize related_name="sizes"

    return render(request, "products/product_detail.html", {
        "product": product,
        "sizes": sizes,
    })


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )
    return redirect('products:wishlist')

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.select_related('product')

    return render(request, 'products/wishlist.html', {
        'wishlist': wishlist,
        'items': items
    })

@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
    item.delete()
    return redirect('products:wishlist')

@login_required
def move_to_cart(request, item_id):
    if request.method != "POST":
        messages.error(request, "Invalid request.")
        return redirect("products:wishlist")

    wishlist_item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
    product = wishlist_item.product

    selected_size = None

    # ✅ If product has sizes -> must choose size
    if product.has_sizes:
        selected_size = request.POST.get("size")
        if not selected_size:
            messages.error(request, "Please select a size.")
            return redirect("products:wishlist")

        # ✅ Validate stock
        ps = get_object_or_404(ProductSize, product=product, size=selected_size)
        if ps.stock <= 0:
            messages.error(request, "Selected size is out of stock.")
            return redirect("products:wishlist")

    cart, _ = Cart.objects.get_or_create(user=request.user)

    # ✅ IMPORTANT: cart items must be unique by (cart, product, size)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=selected_size,
        defaults={"quantity": 1},
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Optional: remove from wishlist after moving
    wishlist_item.delete()

    messages.success(request, "Moved to cart!")
    return redirect("orders:cart")

