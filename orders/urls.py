from django.urls import path
from . import views
app_name = 'orders'
urlpatterns = [
    path('', views.cart_detail, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path("update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
    path('success/', views.order_success, name='order_success'),
]




