from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user', views.edit_user, name='edit_user'),
    path('update_user/<str:id>/', views.update_user, name='update_user'),
    path('delete_user/<str:id>/', views.delete_user, name='delete_user'),
    path('search/', views.search, name='search'),

]
