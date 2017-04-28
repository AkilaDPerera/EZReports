"""{{ project_name }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/{{ docs_version }}/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

#Rest framework URL handling
from rest_framework import  routers
from Reports import  views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

router = routers.DefaultRouter()
router.register(r'student', views.StudentViewSet)
router.register(r'subject', views.SubjectViewSet)
router.register(r'classroom', views.ClassRoomViewSet)
router.register(r'exam', views.ExamViewSet)
router.register(r'mark', views.MarkViewSet)
router.register(r'performance', views.PerformanceViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'rowner', views.ROwnerViewSet)
router.register(r'message', views.MessageViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    url(r'^admin/', admin.site.urls),
    url(r'^', include('Reports.urls')),
]
