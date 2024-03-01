
from django.urls import path, include
from .views import *
from . import views
# if all function of .views are actively running then * is need if not import only need function
urlpatterns = [
    path('', index),
    path('login/', signIn),
    path('register/', register),
    
    path('shop/', shop), #this
    path('cart/', cart), #this
    path('product/<int:id>', productDetails),
    path('logout/', user_logout),
    path('add-to-cart/<int:product_id>', addToCart),
    path('remove-from-cart/<int:product_id>', removeFromCart), 
    # path('remove-from-cart/<int:id>', removeFromCart), 
    path('checkout/', checkout),
    path('my-order/', myOrder),
    path('add_to_wishlist/<int:product_id>', addToWishlist), 
    path('remove_from_wishlist/<int:wishlist_id>', removeFromWishlist), 
    path('wishlist/', wishList),
    path('my-profile/', profile),
    
    # api urls
    # path('get-products/', getProducts),

    
]
