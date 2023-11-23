from django.urls import path
from board.views import CategoryDetail, AdListView, AdDetailView

urlpatterns = [
    path('category/<int:pk>', CategoryDetail.as_view(), name='category_detail'),


    path('ads/', AdListView.as_view(), name='ads_list'),
    path('ads/<int:pk>/detail', AdDetailView.as_view(), name='ads_detail'),
    # path('create/', AdCreateView.as_view(), name='ads_create'),
    # path('<int:pk>/edit', AdUpdateView.as_view(), name='ads_edit'),
    # path('<int:pk>/delete', AdDeleteView.as_view(), name='ads_delete'),


]
