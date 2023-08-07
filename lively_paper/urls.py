"""
URL configuration for lively_paper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path

import lively_paper.views.index
import lively_paper.views.chat
import lively_paper.views.file

urlpatterns = [
    path('', lively_paper.views.index.index),
    path('chat', lively_paper.views.chat.chat),
    path('chat/histories', lively_paper.views.chat.histories),
    path('chat/history/<str:session_id>', lively_paper.views.chat.history),
    path('chat/history/<str:session_id>/delete', lively_paper.views.chat.delete_history),
    path('chat/new', lively_paper.views.chat.new_chat),
    path('file', lively_paper.views.file.upload),
    path('admin', admin.site.urls),

    re_path(r'^component/.*', lively_paper.views.index.static),
    re_path(r'^page/.*', lively_paper.views.index.static)
]
