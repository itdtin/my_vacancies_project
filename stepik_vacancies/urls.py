from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

from vacancies.views import MainView
from .views import MySignupView, MyLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    re_path(r'^', include('vacancies.urls')),
    path('login', MyLoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('signup', MySignupView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
