"""nogios URL Configuration

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
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api', views.checks_json, name='checks_json'),
    re_path(r'^create(/?|/(?P<item_id>\w+))?$', views.create, name='create'),
    path('api/update', views.update, name='update'),
    path('delete/<int:item_id>', views.delete, name='delete'),
    path('view/<str:item_id>', views.view, name='view'),
    path('location/<str:loc>', views.location, name='location'),
    path('api/view/<str:item_id>', views.view_json, name='view_json'),
    path('reload_config', views.reload_config, name='reload_config'),
    path('api/reload_config', views.reload_config_json, name='reload_config_json'),
    path('api/flow_items', views.get_flow_items, name='get_flow_items'),
]
