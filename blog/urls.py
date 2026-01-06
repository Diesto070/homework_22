from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogDeleteView, BlogDetailView, BlogListView, BlogUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog_form'),
    path('blogs/<int:pk>/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('blogs/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
]