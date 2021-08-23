from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

from account.views import (
    register_view,
    login_view,
    logout_view,
    account_view,
    search,
    update_view,
)

app_name = 'account'
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('account/<int:user_id>/', account_view, name='account'),
    path('search/', search, name='search'),
    path('update/<int:pk>/', update_view, name='update'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)