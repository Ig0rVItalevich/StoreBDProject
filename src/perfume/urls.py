from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/<str:sort_name>', views.products, name="products"),
    path('product/<int:number>', views.product, name="product"),
    path('category/<str:category_name>', views.category, name="category"),
    path('bag/', views.bag, name="bag"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('settings/', views.settings, name="settings"),
    path('search/', views.search, name="search"),
    path('grade/', views.grade, name="grade"),
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('reduce_amount_cart/', views.reduce_amount_cart, name="reduce_amount_cart"),
    path('increase_amount_cart/', views.increase_amount_cart, name="increase_amount_cart"),
    path('order/<int:number>', views.order, name="order"),
    path('order_history/', views.order_history, name="order_history"),
    path('make_order/', views.make_order, name="make_order"),
    path('', views.index, name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
