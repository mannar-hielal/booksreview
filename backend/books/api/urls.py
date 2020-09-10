from django.urls import path

from books.api.views import (
    # ArticleListCreateAPIView,
    # ArticleDetailAPIView,
    # JournalistCreateAPIView,
    BookList,
    BookDetail,
    ReviewList,
    ReviewDetail,
    ApiRoot
)

urlpatterns = [
    # path('articles/', article_list_create_api_view, name='article_list'),
    # path('articles/<int:pk>/', article_detail_api_view, name='article_detail')
    # path('articles/', ArticleListCreateAPIView.as_view(),
    #      name='article_list'),
    # path('articles/<int:pk>/', ArticleDetailAPIView.as_view(),
    #      name='article_detail'),
    # path('journalists/', JournalistCreateAPIView.as_view(),
    #      name='journalist_list'),
    path('books/', BookList.as_view(),
         name=BookList.name),
    path('book/<int:pk>/', BookDetail.as_view(),
         name=BookDetail.name),
    path('book/<int:pk>/review/', ReviewList.as_view(),
         name=ReviewList.name),
    path('reviews/<int:pk>/', ReviewDetail.as_view(),
         name=ReviewDetail.name),
    path('', ApiRoot.as_view(), name=ApiRoot.name)
]
