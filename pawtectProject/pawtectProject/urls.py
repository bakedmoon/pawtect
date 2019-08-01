
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
    url(r'^login/',views.login,name='login'),
    url(r'^plans/',views.plans,name='plans'),
    url(r'^review/',views.review,name='review'),
    url(r'^quotation/',views.quotation,name='quotation'),
    url(r'^aboutUs/',views.aboutUs,name='aboutUs'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^assets/(?P<path>.*)$', serve,{'document_root': settings.ASSETS}),
]
