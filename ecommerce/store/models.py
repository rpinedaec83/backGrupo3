from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Categoria(models.Model):
    """
    Modelo de Categoria
    """
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.nombre)


class Cupon(models.Model):
    """
    Modelo de Cupon
    """
    codigo = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=2000)
    descuento = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    fecha_expiracion = models.DateTimeField()
    es_general = models.BooleanField(default=False)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.codigo)


class EstadoPedido(models.Model):
    """
    Modelo de Estado de Pedido
    """
    ESTADOS = [
        ('CAN', 'Cancelado'),
        ('PEN', 'Pago Pendiente'),
        ('CON', 'Confirmado'),
        ('PRO', 'Procesando'),
        ('ENV', 'Enviando'),
        ('ENT', 'Entregado'),
    ]
    descripcion = models.CharField(max_length=15, choices=ESTADOS)

    def __str__(self):
        return str(self.descripcion)


class Cliente(models.Model):
    """
    Modelo de Cliente
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=8, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.user.email)


class Direccion(models.Model):
    """
    Modelo de Direccion de Cliente
    """
    cliente = models.ForeignKey(
        Cliente, related_name="direcciones", on_delete=models.CASCADE)
    pais = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=200)
    distrito = models.CharField(max_length=200)
    codigo_postal = models.CharField(max_length=10)
    avenida_calle_jiron = models.CharField(max_length=200)
    numero_calle = models.CharField(max_length=10)
    dpto_interior_piso_lote_bloque = models.CharField(
        max_length=200, blank=True)
    numero_contacto = models.CharField(max_length=20)


class Producto(models.Model):
    """
    Modelo de Producto
    """
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    igv = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.nombre)


class Pedido(models.Model):
    """
    Modelo de Pedido
    """
    fecha = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    igv = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoPedido, on_delete=models.CASCADE)
    cupones = models.ManyToManyField(Cupon, blank=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return str(self.id)  # pylint: disable=no-member


class DetallePedido(models.Model):
    """
    Modelo de Detalle de Pedido
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_final = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])


class Pago(models.Model):
    """
    Modelo de Pago
    """
    METODOS = [
        ('TAR', 'Tarjeta de crédito/débito'),
        ('TRA', 'Transferencia bancaria'),
        ('CON', 'Contraentrega'),
    ]
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    metodo = models.CharField(max_length=15, choices=METODOS)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)  # pylint: disable=no-member
