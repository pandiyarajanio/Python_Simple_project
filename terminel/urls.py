from django.urls import path
from . import views


urlpatterns = [
    path('index',views.index,name='index'),
    path('',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('delete/<int:pk>/',views.delete,name='delete'),
    path('block/<int:pk>/',views.block,name='block'),
    path('unblock/<int:pk>/',views.unblock,name='unblock'),
    path('update/<int:pk>/',views.update,name='update'),
    path('adduser/',views.adduser,name='adduser'),
    path('adminlogout/',views.adminlogout,name='adminlogout')

]
