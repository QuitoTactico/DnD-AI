"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from DnD_AI import views as dnd

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dnd.home, name='home'),
    path('home', dnd.home, name='home'),
    path('about', dnd.about, name='about'),
    path('guide', dnd.guide, name='guide'),
    path('campaignselection', dnd.campaignSelection, name='campaignSelection'),
    path('campaigncreation', dnd.campaignCreation, name='campaignCreation'),
    path('playerselection', dnd.playerSelection, name='playerSelection'),
    path('playercreation', dnd.playerCreation, name='playerCreation'),
    path('game', dnd.game, name='game'),
]

urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
