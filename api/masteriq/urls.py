"""
URL configuration for masteriq project.

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
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from masteriqapp import views as masteriq_views
from rest_framework.authtoken import views


router = DefaultRouter()

router.register("category", masteriq_views.IQView, basename="category")
router.register("question", masteriq_views.QuestionView, basename="question")
router.register("rank", masteriq_views.RankView, basename="rank")
router.register("user", masteriq_views.AuthenticationView, basename="user")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
]
