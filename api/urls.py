from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

urlpatterns = [
    path('partite/', views.PartitaViewSet.as_view({'post': 'create', 'get': 'list'}), name='partite'),
    path('mosse/', views.MossaViewSet.as_view({'post': 'create'}), name='mosse'),
    path('giocatori/', views.GiocatoreViewSet.as_view({'post': 'create', 'get': 'list'}), name='giocatori'),
    path('tabellone/<int:id_partita>/', views.PartitaListAPIView.as_view(), name='tabellone'),
]

