from django.urls import path
from mmorpg import views


urlpatterns = [
    path('', views.AdList.as_view(), name='ads_list'),
    path('ads/<int:pk>/', views.AdDetail.as_view(), name='ads_detail'),  # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('create/', views.AdCreateView.as_view(), name='ads_create'),

    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),

    # path('edit/<int:pk>/', views.AdUpdateView.as_view(), name='ads_edit'),
    # path('delete/<int:pk>/', views.AdDeleteView.as_view(), name='ads_delete'),
    # path('comment_create/<int:pk>/', views.RespondCreateView.as_view(), name='comment_create'),
    # path('comments/', views.RespondListView.as_view(), name='comment_list'),
    # path('comments/approved/<int:pk>/', views.comment_approved, name='comment_approved'),
    # path('comments/delete/<int:pk>/', views.RespondDeleteView.as_view(), name='comment_delete'),
    # path('search/', views.SearchResultsListView.as_view(), name='search_results'),
    # path('comments/search/', views.SearchRespondResultsListView.as_view(), name='search_comments_results'),
]
