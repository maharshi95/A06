"""A06 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework import routers
import app.views as views

router = routers.DefaultRouter()
router.register(r'api/products', views.ProductViewSet,base_name="ProductViewSet")
router.register(r'api/orders', views.OrderViewSet,base_name="OrderViewSet")
router.register(r'api/orders/(?P<order_id>[0-9]+)/orderlineitem', views.OrderItemViewSet,base_name="OrderItemViewSet")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api/products/summary',views.get_products_summary),
    url(r'^api/orders/summary',views.get_orders_summary),
    url(r'^api/health',views.health),
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
