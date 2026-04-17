from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', views.login_page, name='login'),

    path('sheet/', views.sheet, name='sheet'),

    path('login/', views.login_page, name='login'),

    path('register/', views.register, name='register'),

    path('logout/', views.logout_page, name='logout'),

    path('autosave/', views.autosave, name='autosave'),

    path('view-data/', views.view_data, name='view_data'),

    path('admin-data/', views.admin_data, name='admin_data'),

    path('admin-own-data/', views.admin_own_data, name='admin_own_data'),

    path('update-data/<int:id>/', views.update_data, name='update_data'),

    path('delete-data/<int:id>/', views.delete_data, name='delete_data'),

    path('manage-users/', views.manage_users, name='manage_users'),

    path('approve-user/<int:id>/', views.approve_user, name='approve_user'),

    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),

    path('toggle-staff/<int:id>/', views.toggle_staff, name='toggle_staff'),
    
    path('all-data/', views.all_data, name='all_data'),
    
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    
    path('create-admin/', views.create_admin),

]