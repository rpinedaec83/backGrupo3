"""
URL configuration for pachacursos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter
from cursos import views

router = DefaultRouter()
router.register(r'categorias', views.CategoriaView)
router.register(r'cupones', views.CuponView)
router.register(r'estados_pedido', views.EstadoPedidoView)
router.register(r'productos', views.ProductoView)
router.register(r'pedidos', views.PedidoView)
router.register(r'detalles_pedido', views.DetallePedidoView)
router.register(r'pagos', views.PagoView)
router.register(r'direcciones', views.DireccionView, basename='direccion')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
    path('register/', views.UserView.as_view(), name='register'),
    path('api/category/', include('category.urls')),
    path('api/product/', include('product.urls')),
    path('api/cart/', include('cart.urls')),
]