from django import views
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhooks/', views.webhooks),
    path('chat/', views.chat, name = 'chat'),
    path('res-count', views.ResponseCoutListView.as_view(), name='response_count'),
    path('66d2b8f4a09cd35cb23076a1da5d51529136a3373fd570b122/', views.TelegramChatbot.as_view(), name='webhook'),
    path('signin/', views.SigninView.as_view(), name = 'signin'),
    path('signup/', views.SignupView.as_view(), name = 'signup'),
    path('', views.root_route, name = 'root'),
]
