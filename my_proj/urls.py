
from django.contrib import admin
from django.urls import include, path
from my_app.views import home_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home_redirect'),
    path('my_app/', include('my_app.urls')),
]

