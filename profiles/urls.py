from django.urls import path
from . import views
from .views import export_filter_page
urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('export-profiles/', export_filter_page, name='export_filter_page'),
]
