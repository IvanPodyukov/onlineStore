from django.urls import path

from .views import ProductListView, CreateProductView, ProductDetailsView, ProductDeleteView, CartDetailsView, \
    AddProductToCartView, DeleteProductFromCartView, CartClearView, BuyView, ProductEditView

app_name = 'shop'
urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('products/product/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/product/<int:pk>/edit/', ProductEditView.as_view(), name='product_edit'),
    path('products/product/<int:pk>/add_to_cart/', AddProductToCartView.as_view(), name='add_product_to_cart'),
    path('products/product/<int:pk>/delete_from_cart/', DeleteProductFromCartView.as_view(),
         name='delete_product_from_cart'),
    path('products/product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('create/', CreateProductView.as_view(), name='create_product'),
    path('cart/', CartDetailsView.as_view(), name='cart'),
    path('cart/clear/', CartClearView.as_view(), name='cart_clear'),
    path('buy/', BuyView.as_view(), name='buy')
]
