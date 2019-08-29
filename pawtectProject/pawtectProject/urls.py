
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
    url(r'^home/$',views.home,name='home'),
    url(r'^contact/',views.contact,name='contact'),
    url(r'^register/',views.signup,name='register'),
    url(r'^login/',views.login,name='login'),
    url(r'^plans/',views.plans,name='plans'),
    url(r'^otp/',views.otp,name='otp'),
    url(r'^review/',views.review,name='review'),
    url(r'^quotation/',views.quotation,name='quotation'),
    url(r'^pet_profile/',views.pet_profile,name='pet_profile'),
    url(r'^user_profile/',views.user_profile,name='user_profile'),
    url(r'^get-filter-quote-data/',views.get_filter_quote_data,name="get-filter-quote-data"),
    url(r'^aboutUs/',views.aboutUs,name='aboutUs'),
    url(r'^terms/',views.ter_of_use,name='terms'),
    url(r'^privacy/',views.privacy_policy,name='privacy'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^assets/(?P<path>.*)$', serve,{'document_root': settings.ASSETS}),
]
