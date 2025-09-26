from django.urls import path
from main.views import (show_main, create_product, show_product, 
                        show_xml, show_json, show_xml_by_id, show_json_by_id, 
                        register, login_user, logout_user, edit_product, delete_product)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product/', create_product, name='create_product'),
    path('product/<str:id>/', show_product, name='show_product'),

    # Akses xml data masing2 produk
    path('xml/', show_xml, name='show_xml'),

    # Akses json data masing2 produk
    path('json/', show_json, name='show_json'),

    # Akses xml data produk berdasarkan id
    path('xml/<str:product_id>/', show_xml_by_id, name='show_xml_by_id'),

    # Akses json data produk berdasarkan id
    path('json/<str:product_id>/', show_json_by_id, name='show_json_by_id'),

    # User Authentication Register
    path('register/', register, name='register'),

    # User Authentication Login
    path('login/', login_user, name='login'),

    # User Authentication Logout
    path('logout/', logout_user, name='logout'),

    # Edit Product
    path('product/<uuid:id>/edit', edit_product, name='edit_product'),

    # Delete Product
    path('product/<uuid:id>/delete', delete_product, name='delete_product'),

]