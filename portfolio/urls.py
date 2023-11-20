from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stocks/', views.StockListView.as_view(), name='stocks'),
    path('stocks/<int:pk>', views.get_stock_data, name='stock-detail'),
    #path('stocks/<int:pk>/options', views.OptionListView.as_view(), name='options'),
    #path('stocks/<str:ticker>/options/<str:symbol>', views.get_option_data, name='option-detail'),
    #path('options/<str:symbol>', views.get_option_data, name='option-detail'),
]