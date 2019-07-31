
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls import url,include
from pawtectProject  import settings
from django.views.static import serve
from pawtectApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^contact/',views.contact,name='contact'),
    url(r'^register/',views.register,name='register'),
    url(r'^login/',views.user_login,name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^assets/(?P<path>.*)$', serve,{'document_root': settings.ASSETS}),
]
