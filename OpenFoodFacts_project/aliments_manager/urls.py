from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results', views.results, name='results'),
    path('registration', views.registration, name='registration'),
    path('connection', views.connection, name='connection'),
    path('disconnection', views.disconnection, name='disconnection'),
    path('account', views.account, name='account'),
   	path('favorite', views.add_favorite, name='favorite'),
]