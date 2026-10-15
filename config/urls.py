from django.contrib import admin
from django.urls import path, include
from apps.login import views as login_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('apps.login.urls')),
    path('logout/', login_views.logout, name='logout'),
    path('', include('apps.laboratorio.urls')),
]
