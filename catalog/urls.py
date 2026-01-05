from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (ContactsView, HomeView, ProductCreateView, ProductDeleteView, ProductDetailView,
                           ProductListView, ProductsListView, ProductUpdateView)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("home/", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/create/", ProductCreateView.as_view(), name="product_form"),
    path("product/update/<int:pk>", ProductUpdateView.as_view(), name="product_update"),
    path("product/delete/<int:pk>", ProductDeleteView.as_view(), name="product_delete"),
    path("products/", ProductsListView.as_view(), name="products_list"),
]
