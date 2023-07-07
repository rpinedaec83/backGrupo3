from rest_framework import viewsets, status
from .models import Categoria, Cupon, EstadoPedido, Direccion, Producto, Pedido, DetallePedido, Pago
from .serializers import CategoriaSerializer, CuponSerializer, EstadoPedidoSerializer, DireccionSerializer, ProductoSerializer, PedidoSerializer, DetallePedidoSerializer, PagoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from rest_framework import serializers

class UserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            account.password = make_password(account.password)
            account.save()
            data['response'] = 'User registered successfully'
            data['username'] = account.username
            data['email'] = account.email
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriaView(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]


class CuponView(viewsets.ModelViewSet):
    queryset = Cupon.objects.all()
    serializer_class = CuponSerializer
    permission_classes = [IsAuthenticated]


class EstadoPedidoView(viewsets.ModelViewSet):
    queryset = EstadoPedido.objects.all()
    serializer_class = EstadoPedidoSerializer
    permission_classes = [IsAuthenticated]

class DireccionView(viewsets.ModelViewSet):
    serializer_class = DireccionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Este view sólo debería mostrar las direcciones pertenecientes al usuario logueado.
        """
        user = self.request.user
        return Direccion.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        """
        Este método crea una nueva dirección relacionada al usuario logueado.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Este método actualiza una dirección existente que pertenezca al usuario logueado.
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Este método elimina una dirección existente que pertenezca al usuario logueado.
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductoView(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]


class PedidoView(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]


class DetallePedidoView(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    permission_classes = [IsAuthenticated]


class PagoView(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]
