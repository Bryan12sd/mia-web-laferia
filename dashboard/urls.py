from django.urls import path
from .views.login.index import login_view, logout_view
from .views.dashboard.index import dashboard_view


urlpatterns = [
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]