from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/<str:aliment_searched>/<int:page_id>/', views.results, name='results'),
    path('registration/', views.registration, name='registration'),
    path('connection/', views.connection, name='connection'),
    path('disconnection/', views.disconnection, name='disconnection'),
    path('account/', views.account, name='account'),
   	path('add_favorite/', views.add_favorite, name='add_favorite'),
   	path('favorites/<int:page_id>/', views.show_favorites, name='favorites' ),
   	path('aliment/<str:code>/', views.show_aliment, name='aliment')
]