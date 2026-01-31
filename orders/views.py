from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from products.models import Product, ProductSize
from .models import Cart, CartItem, Order, OrderItem


# ==================================================
# CART VIEWS
# ==================================================

@login_required
def cart_detail(request):
    """
    Displays the current user's cart and all cart items.
    Creates a cart automatically if one does not exist.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related("product")

    return render(request, "orders/cart.html", {
        "cart": cart,
        "cart_items": cart_items,
    })


@login_required
def add_to_cart(request, product_id):
    """
    Adds a product to the cart.
    Handles both size-based and non-size-based products.
    """
    if request.method != "POST":
        return redirect("products:product_detail", product_id=product_id)

    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    selected_size = request.POST.get("size")

    # 🔹 Products that have size variants
    if product.has_sizes:
        if not selected_size:
            messages.error(request, "Please select a size.")
            return redirect("products:product_detail", product_id=product.id)

        ps = get_object_or_404(ProductSize, product=product, size=selected_size)

        if ps.stock <= 0:
            messages.error(request, f"{selected_size} is out of stock.")
            return redirect("products:product_detail", product_id=product.id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=selected_size,
            defaults={"quantity": 1},
        )

        # Prevent exceeding available stock
        if not created:
            if item.quantity + 1 > ps.stock:
                messages.error(
                    request,
                    f"Only {ps.stock} available for size {selected_size}."
                )
                return redirect("orders:cart")
            item.quantity += 1
            item.save()

    # 🔹 Products without sizes (e.g. sarees)
    else:
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=None,
            defaults={"quantity": 1},
        )

        if not created:
            item.quantity += 1
            item.save()

    messages.success(request, "Added to cart.")
    return redirect("orders:cart")


@login_required
def update_cart_item(request, item_id):
    """
    Updates cart item quantity via AJAX (increase / decrease).
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    action = request.POST.get("action")

    if action == "increase":
        item.quantity += 1
        item.save()

    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
            return JsonResponse({
                "removed": True,
                "cart_total": f"{cart.total_price():.2f}",
            })

    return JsonResponse({
        "removed": False,
        "quantity": item.quantity,
        "item_total": f"{item.total_price():.2f}",
        "cart_total": f"{cart.total_price():.2f}",
    })


@login_required
def remove_from_cart(request, item_id):
    """
    Removes a single item from the cart.
    """
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("orders:cart")


# ==================================================
# PLACE ORDER
# ==================================================

@login_required
def place_order(request):
    """
    Handles order placement, stock validation,
    order creation, cart clearing, and email notifications.
    """
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("orders:cart")

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        if not full_name or not phone or not address:
            messages.error(request, "Please fill in all delivery details.")
            return redirect("orders:place_order")

        with transaction.atomic():

            # 🔹 Stock validation before creating order
            for item in cart.items.select_related("product"):
                if item.product.has_sizes:
                    ps = get_object_or_404(
                        ProductSize,
                        product=item.product,
                        size=item.size
                    )
                    if ps.stock < item.quantity:
                        messages.error(
                            request,
                            f"Not enough stock for {item.product.name} (Size {item.size})."
                        )
                        return redirect("orders:cart")

            # 🔹 Create order
            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                address=address,
            )

            # 🔹 Create order items and reduce stock
            for item in cart.items.select_related("product"):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    size=item.size if item.product.has_sizes else None,
                )

                if item.product.has_sizes:
                    ps = ProductSize.objects.select_for_update().get(
                        product=item.product,
                        size=item.size,
                    )
                    ps.stock -= item.quantity
                    ps.save()

            # 🔹 Clear cart after successful order
            cart.items.all().delete()

        # 🔹 Email notifications
        send_admin_order_email(order)
        send_customer_order_email(order)

        messages.success(request, "Order placed successfully!")
        return redirect("orders:order_success")

    return render(request, "orders/place_order.html")


# ==================================================
# ADMIN EMAIL (HTML)
# ==================================================

def send_admin_order_email(order):
    """
    Sends an HTML email notification to admin when a new order is placed.
    """
    items = order.items.select_related("product")

    subject = f"New Order Placed - Order #{order.id}"

    text_body = (
        f"New order placed.\n\n"
        f"Order ID: {order.id}\n"
        f"Customer: {order.full_name}\n"
        f"Email: {order.user.email}\n"
        f"Phone: {order.phone}\n"
        f"Address: {order.address}\n\n"
        f"Items:\n" +
        "\n".join([
            f"- {i.product.name} | Qty: {i.quantity}" +
            (f" | Size: {i.size}" if i.size else "")
            for i in items
        ])
    )

    html_body = render_to_string("emails/admin_new_order.html", {
        "order": order,
        "items": items,
        "now": timezone.now(),
    })

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=None,  # Uses DEFAULT_FROM_EMAIL
        to=settings.ADMIN_NOTIFICATION_EMAILS,
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)


# ==================================================
# CUSTOMER CONFIRMATION EMAIL
# ==================================================

def send_customer_order_email(order):
    """
    Sends an order confirmation email to the customer.
    """
    customer_email = (order.user.email or "").strip()
    if not customer_email:
        return

    items = order.items.select_related("product")

    subject = f"Order Confirmed ✅ A&M Signature - Order #{order.id}"

    text_body = (
        f"Hi {order.full_name},\n\n"
        f"Thank you for your order! Your order has been received.\n\n"
        f"Order ID: {order.id}\n"
        f"Placed on: {timezone.now().strftime('%d %b %Y, %H:%M')}\n\n"
        f"Delivery Address:\n{order.address}\n\n"
        f"Items:\n" +
        "\n".join([
            f"- {i.product.name} | Qty: {i.quantity}" +
            (f" | Size: {i.size}" if i.size else "")
            for i in items
        ]) +
        "\n\nWe’ll contact you when it’s out for delivery.\n"
        "A&M Signature — Wear Your Story"
    )

    html_body = render_to_string("emails/customer_order_confirmation.html", {
        "order": order,
        "items": items,
        "now": timezone.now(),
        "brand_name": "A&M Signature",
        "support_email": settings.DEFAULT_FROM_EMAIL,
    })

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=None,
        to=[customer_email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)


@login_required
def order_success(request):
    """
    Displays order success confirmation page.
    """
    return render(request, "orders/order_success.html")
