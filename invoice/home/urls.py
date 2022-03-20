"""invoice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from pydoc import visiblename
from django.urls import path,include
from home import views

urlpatterns = [
    path('index',views.index,name='index'),
    path('input',views.user_input),
    path('invoice_list',views.invoice_list),
    path('pdf',views.get_pdf,name="pdf"),
    path('invoice/<int:id>',views.get_invoice_detail),
    # auth
    path('logout/', views.logout, name='logout'),
    path('', views.loginuser, name='loginuser'),
]
