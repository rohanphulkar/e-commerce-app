from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import notfound,home,products,product_details,checkout,account,add_to_cart,remove_from_cart,success,failed

urlpatterns = [
    path("",home,name="home"),
    path("shop/",products,name="products"),
    path("product/<slug:slug>/",product_details,name="product_details"),
    path("checkout/",checkout,name="checkout"),
    path("add_to_cart/<str:id>/",add_to_cart,name="add_to_cart"),
    path("remove_from_cart/<str:id>/",remove_from_cart,name="remove_from_cart"),
    path("account/",account,name="account"),
    path("success/<str:id>/",success,name="success"),
    path("failed/",failed,name="failed"),
    path("*",notfound,name="notfound"),

]

urlpatterns += staticfiles_urlpatterns()

