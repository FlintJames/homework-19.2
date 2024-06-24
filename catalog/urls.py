from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, contacts, BlogCreateView, BlogDetailView, BlogListView, \
    BlogUpdateView, BlogDeleteView, toggle_publication, ProductCreateView, ProductUpdateView, CategoryListView, \
    CategoryDetailView

app_name = CatalogConfig.name

urlpatterns = [
    # path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("", ProductListView.as_view(), name='products_list'),
    path("products/<int:pk>/", cache_page(60)(ProductDetailView.as_view()), name='products_detail'),
    path("product/create/", ProductCreateView.as_view(), name='product_create'),
    path("product/<int:pk>/update/", ProductUpdateView.as_view(), name='product_update'),
    path('catalog/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path("catalog/", BlogListView.as_view(), name='blog_list'),
    path("blog/<int:pk>/", BlogDetailView.as_view(), name='blog_detail'),
    path("blog/create/", BlogCreateView.as_view(), name='blog_create'),
    path("blog/<int:pk>/update/", BlogUpdateView.as_view(), name='blog_update'),
    path("blog/<int:pk>/delete/", BlogDeleteView.as_view(), name='blog_delete'),
    path("publication/<int:pk>/", toggle_publication, name='toggle_publication')
]
