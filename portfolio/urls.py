from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stocks/', views.StockListView.as_view(), name='stocks'),
    path('stocks/<int:pk>', views.get_stock_data, name='stock-detail'),
    path('options/', views.get_all_options, name='options'),
]