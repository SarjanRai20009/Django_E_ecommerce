
from django.urls import path, include
from .views import *
# from . import views
# if all function of .views are actively running then * is need if not import only need function
urlpatterns = [
  
    path('get-product/',getProduct),
    path('add-product/',addProduct),
    path('single-product-detail/<int:product_id>',singleProductDetail),
    path('edit-product/<int:product_id>',editProduct),
    path('delete-product/<int:product_id>',deleteProduct),
    
   
    
]
