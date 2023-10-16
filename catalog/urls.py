from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductDetailView, ProductListView, BlogEntryCreateView, BlogEntryListView, \
    BlogEntryUpdateView, BlogEntryDetailView, BlogEntryDeleteView, ProductCreateView, ProductUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='view_product'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('blog/create/', BlogEntryCreateView.as_view(), name='create_blog'),
    path('blog/list/', BlogEntryListView.as_view(), name='blogentry_list'),
    path('blog/update/<int:pk>', BlogEntryUpdateView.as_view(), name='update_blog'),
    path('blog/view/<int:pk>', BlogEntryDetailView.as_view(), name='view_blog'),
    path('blog/delete/<int:pk>', BlogEntryDeleteView.as_view(), name='delete_blog'),
    path('product/edit/<int:pk>', ProductUpdateView.as_view(), name='update_product')
]
