"""
URL configuration for ats project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]


# from .views import signup, CustomLoginView
from . import views
from django.contrib import admin
from django.urls import path, include
# from .views import signup


urlpatterns = [
    # path('upload/', views.upload_resume, name='upload_resume'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('rules/', views.rules, name='rules'),
    path('mainpage/', views.mainpage, name='mainpage'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('calculate-ats/', views.calculate_ats_score, name='calculate_ats'),
    path('hihello/', views.hihello, name='hihello')
    # path('calculate-ats', views.calculate_ats, name='calculate_ats'),

]

