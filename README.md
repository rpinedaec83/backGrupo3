# Backend Grupo 3

Este repositorio contiene el código del backend desarrollado por el Grupo 3 para un proyecto de ecommerce de venta de cursos online.

## Instalación

Para instalar el proyecto, sigue estos pasos:

1. Clona este repositorio en tu máquina local.

2. Abre una terminal y navega hasta el directorio raíz del proyecto.

3. Crea un entorno virtual para el proyecto. Si no tienes instalado `virtualenv`, ejecuta el siguiente comando para instalarlo:
   ```bash
   pip install virtualenv
   ```

   Luego, crea el entorno virtual utilizando uno de los siguientes comandos según tu sistema operativo:

   Linux/Mac:
   ```bash
   virtualenv venv
   ```

   Windows:
   ```bash
   python -m venv venv
   ```

4. Activa el entorno virtual:
   - En Linux/Mac, ejecuta:
     ```bash
     source venv/bin/activate
     ```
   - En Windows, ejecuta:
     ```bash
     venv\Scripts\activate
     ```

5. Instala las dependencias del proyecto ejecutando el siguiente comando:
   ```bash
   pip install -r requirements.txt
   ```

6. Configura la conexión a la base de datos en el archivo `settings.py`. Abre el archivo y busca la sección `DATABASES`. Reemplaza los valores en blanco con la información de tu base de datos PostgreSQL.

7. Crea la base de datos en PostgreSQL con el nombre especificado en la configuración.

8. Ejecuta las migraciones para crear las tablas necesarias en la base de datos:
   ```bash
   python manage.py migrate
   ```

## Uso

Una vez completada la instalación, sigue estos pasos para ejecutar el proyecto:

1. Crea un superusuario para acceder al panel de administración:
   ```bash
   python manage.py createsuperuser
   ```

2. Inicia el servidor de desarrollo con el siguiente comando:
   ```bash
   python manage.py runserver
   ```

3. Abre tu navegador web y accede a `http://localhost:8000/` para ver la aplicación en funcionamiento.

4. Para acceder al panel de administración, visita `http://localhost:8000/admin` e inicia sesión con las credenciales del superusuario que creaste.

