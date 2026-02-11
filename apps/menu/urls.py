from django.urls import path
from .views import MenuListView, MenuDetailView, landing_page_view

app_name = "menu"

urlpatterns = [
    path('', landing_page_view, name='landing_page'),
    path('menu/', MenuListView.as_view(), name='menu_list'),
    path('<int:pk>', MenuDetailView.as_view(), name='detail'),
]