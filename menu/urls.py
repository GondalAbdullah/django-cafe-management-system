from django.urls import path
from .views import MenuListView, MenuDetailView

app_name = "menu"

urlpatterns = [
    path('', MenuListView.as_view(), name='list'),
    path('<int:pk>', MenuDetailView.as_view(), name='detail'),
]