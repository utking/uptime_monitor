"""monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('latest', views.latest, name='latest'),
    path('overview', views.overview, name='overview'),
    path('history', views.history, name='history'),
    path('view/<int:item_id>', views.view, name='view'),
    path('history/<str:item_id>', views.history, name='history'),
    path('run/<str:item_id>', views.run, name='run'),
]
