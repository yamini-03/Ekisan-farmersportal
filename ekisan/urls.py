"""ekisan URL Configuration

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
from .import views

from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('buying/', views.buying, name='buying'),
    # path('selling/', views.selling, name='selling'),
    path('crop/', views.crop, name='crop'),
    path('seedfert/', views.seedfert, name='seed'),
    path('risk/', views.risk, name='risk'),
    path('risk2/', views.risk2, name='risk2'),
    path('risk3/', views.risk3, name='risk3'),
    path('risk4/', views.risk4, name='risk4'),
    path('animal/', views.animal, name='animal'),
    path('weather/', views.weather, name='weather'),
    path('program/', views.program, name='program'),
    path('contact/', views.contact, name='contact'),
    path('soil1/', views.soil1, name='soil1'),
    path('soil2/', views.soil2, name='soil2'),
    path('soil3/', views.soil3, name='soil3'),
    path('soil4/', views.soil4, name='soil4'),
    path('seed1/', views.seed1, name='seed1'),
    path('seed2/', views.seed2, name='seed2'),
    path('seed3/', views.seed3, name='seed3'),
    path('fert1/', views.fert1, name='fert1'),
    path('fert2/', views.fert2, name='fert2'),
    path('fert3/', views.fert3, name='fert3'),
    path('seedvar/', views.seedvar, name='seedvar'),
    path('animal/', views.animal, name='animal'),
    path('vert1/', views.vert1, name='vert1'),
    path('vert2/', views.vert2, name='vert2'),
    path('vert3/', views.vert3, name='vert3'),
    path('vert4/', views.vert4, name='vert4'),
    path('symdisease/', views.symdisease, name='symdiease'),
    path('sd2/', views.sd2, name='symdiease2'),
    path('sd3/', views.sd3, name='symdiease3'),
    path('sd4/', views.sd4, name='symdiease4'),
    path('farmsignUp/', views.farmsignUp, name='farmsignUp'),
    path('fsignin/', views.fsignin, name='fsignin'),
    path('logout/', views.logout, name='log'),
    # path('additem/', views.additem, name='additem'),
    # path('edititem/', views.edititem, name='edititem'),
    path('cart/', views.cart, name='cart'),
    path('pickup/', views.pickup, name='pickup'),
    path('about/', views.about, name='about'),
    path('weather/', views.weather, name='weather'),
    path('Clogin/', views.Clogin, name='Clogin'),
    path('Csignup/', views.Csignup, name='Csignup'),
    path('apples/', views.apples, name='apples'),
    path('bellpeper/', views.bellpeper, name='bellpeper'),
    path('carrot/', views.carrot, name='carrot'),
    path('cauliflower/', views.cauliflower, name='cauliflower'),
    path('cucumber/', views.cucumber, name='cucumber'),
    path('peas/', views.peas, name='peas'),
    path('potato/', views.potato, name='potato'),
    path('tomato/', views.tomato, name='tomato'),
    path('rice/', views.rice, name='rice'),
    path('wheat/', views.wheat, name='wheat'),
    path('mainpro/',views.mainpro,name='mainpro'),
    path('addtocart/',views.addtocart,name='addtocart'),
    path('displaycart/',views.displaycart,name='displaycart'),
    path('consumerlogin/', views.consumerlogin, name='consumerlogin'),
    path('removefromcart/', views.removefromcart, name='removefromcart'),
    path('myorders/', views.myorders, name='myorders'),
    path('razor/',views.razor,name='razor'),
    path('success/',views.success,name='success'),
    path('myprof/',views.myprof,name='myprof'),
    path('farmer/',views.farmer,name='farmer'),
    path('output/',views.output,name='output'),


    # url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

]
