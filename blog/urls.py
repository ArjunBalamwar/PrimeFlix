from django.conf.urls.static import static
from django.urls import path
# from .views import PostDetailView
from . import views
from django.conf import settings
from users import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name="blog-home"),
    path('about/', views.about, name="blog-about"),
    path('post/new/', views.PostCreateView, name='post-create'),
    path('post/<int:pk>/', views.PostDetailView, name='post-detail'),
    path('post/<int:pk>/update', views.update_view, name='post-update'),
    path('post/<int:pk>/delete/', views.delete_view, name='post-delete'),
    path('dashboard/', views.watchLater, name='dash-view'),
    path('dashboard/<str:cats>/', views.GenreWatchLater, name='dash-genre-view'),
    path('category1/<str:cats>/', views.FilteredGenreView, name='category1'),
    path('category2/<str:cats>/', views.FilteredTypeView, name='category2'),
    path('search/<str:cats>/', views.home_search, name="home-search"),
    # path('category1/<str:cats>/<str:cat>/', views.cat_search_genre, name="cat-search-genre"),
    # path('category2/<str:cats>/<str:cat>/', views.home_search, name="cat-search2"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
