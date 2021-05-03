"""topic_forum URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import PasswordResetConfirmView, PasswordChangeView
from books import views as books
from forum import views as forum
from login import views as login
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', books.main, name='topics'),
    path('contact/', books.contact_page, name='connect'),
    path('support/', books.support, name='support'),
    path('forums/', forum.main, name='forum'),
    path('forums/<int:bk>/', forum.forum_book),
    path('forums/<int:bk>/<trd>/<int:pg>', forum.thread),
    path('forum/create/', login.user_page, name='create_user'),
    path('forum/login/', login.modal_login, name='login'),
    path('forum/logout/', login.logout_view, name='logout'),
    path('forum/profile/', login.user_profile, name='profile'),
    path('recovery/', login.pass_reset, name='recovery'),
    path('recovery/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(template_name='login/reset.html', success_url='../../'), name="password_reset_confirm"),
    path('admin/', admin.site.urls),
    path('forum/profile/send_DM', forum.send_DM, name='send_DM'),
    path('add_friend/', forum.new_friend, name='add_friend'),
    path('edit_comment/', login.edit_comment, name="edit_comment_api"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
