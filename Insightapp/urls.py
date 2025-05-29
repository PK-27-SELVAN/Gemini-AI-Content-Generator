from django.urls import path
from .views import SearchView,HistoryView
urlpatterns = [
    path('search/',SearchView.as_view(),name='search'),
    path('history/',HistoryView.as_view(),name='history'),
]