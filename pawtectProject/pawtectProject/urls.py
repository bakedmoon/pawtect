
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from pawtectProject  import settings
from django.views.static import serve
from pawtectApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.home,name='home'),
    url(r'^contact/',views.contact,name='contact'),
    url(r'^register/',views.signup,name='register'),
    url(r'^login/',views.login,name='login'),
    url(r'^forgot_password/',views.forgot_password,name='forgot_password'),
    url(r'^reset_password/',views.reset_password,name='reset_password'),
    url(r'^change_password/',views.change_password,name='change_password'),
    url(r'^plans/',views.plans,name='plans'),
    url(r'^otp/',views.otp,name='otp'),
    url(r'^review/',views.review,name='review'),
    url(r'^quotation/$',views.quotation,name='quotation'),
    url(r'^user_profile/$',views.user_profile,name='user_profile'),
    url(r'^account/my-pets/$',views.my_pets,name='my-pets'),
    url(r'^account/my-pets/new/$',views.my_pets_new,name='my_pets_new'),
    url(r'^account/my-pets/(?P<petId>[0-9]+)/edit/$',views.my_pets_edit,name='my-pets-edit'),
    url(r'^my_proposal/(?P<petId>[0-9]+)/$',views.my_pets_delete,name='my_pets_delete'),
    url(r'^my_vetcoins/',views.my_vetcoins,name='my_vetcoins'),
    url(r'^my_proposal/$',views.my_proposal,name='my_proposal'),
    url(r'^get-filter-quote-data/$',views.get_filter_quote_data,name="get-filter-quote-data"),
    url(r'^get-country-data/$',views.get_country_data,name="get-country-data"),
    url(r'^aboutUs/$',views.aboutUs,name='aboutUs'),
    url(r'^saveAnswer/$',views.saveAnswer,name='saveAnswer'),
    url(r'^planFees/$',views.planFees, name="planFees"),
    url(r'^terms/$',views.ter_of_use,name='terms'),
    url(r'^pawtect_terms/$',views.pawtect_terms,name='pawtect_terms'),
    url(r'^privacy/',views.privacy_policy,name='privacy'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^page_not_found/$',views.page_not_found,name='page_not_found'),
    url(r'^assets/(?P<path>.*)$', serve,{'document_root': settings.ASSETS}),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)