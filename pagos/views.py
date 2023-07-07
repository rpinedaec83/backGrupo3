import culqipy
from django.conf import settings
from django.shortcuts import render

def procesar_pago(request):
    if request.method == 'POST':
        monto = request.POST['monto']  # Obtén el monto del formulario

        # Configura las credenciales de Culqi
        culqi = culqipy.Culqi(settings.CULQI_API_KEY)

        # Crea un objeto de carga con los detalles del pago
        carga = {
            'amount': int(monto) * 100,  # Multiplica el monto por 100 (en céntimos)
            'currency_code': 'PEN',  
        }

        try:
            # Realiza el cargo utilizando culqipy
            respuesta = culqi.charge.create(carga)

            if respuesta['object'] == 'charge' and respuesta['status'] == 'paid':

                return render(request, 'pago_exitoso.html')
            else:
                # El pago falló
                return render(request, 'pago_fallido.html')

        except culqipy.CulqiError as e:
            # Ocurrió un error durante el proceso de pago
            # Maneja el error según tus necesidades
            return render(request, 'error.html', {'mensaje': str(e)})

    return render(request, 'realizar_pago.html')