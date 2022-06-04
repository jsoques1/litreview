"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import review.views

from authentication.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', review.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path("open_ticket/", review.views.open_ticket, name="open_ticket"),
    path('follow_users/', review.views.follow_users, name='follow_users'),
    path(
        "unfollow_user/<int:user_follows_id>/",
        review.views.unfollow_user,
        name="unfollow_user"),
    path("stream/", review.views.stream, name="stream"),
    path("my_posts/", review.views.my_posts, name="my_posts"),
    path("ticket/create/", review.views.create_ticket, name="create_ticket"),
    path("ticket_review/create/", review.views.create_ticket_review, name="create_ticket_review"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)