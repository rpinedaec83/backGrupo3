# Backend Grupo 3

Este es el repositorio del backend del grupo 3. El proyecto consiste en una ecommerce de venta de cursos online.

## Instalación

Para instalar el proyecto, se debe clonar el repositorio y luego instalar las dependencias de python con el siguiente comando en un propio entorno virtual:

Si no tiene instalado virtualenv, debe instalarlo con el siguiente comando:

```bash
pip install virtualenv
```

Luego debe crear el entorno virtual con el siguiente comando:

Linux o Mac:
```bash
virtualenv venv
```

Windows:
```bash
python -m venv venv
```

Luego debe activar el entorno virtual con el siguiente comando:

Linux o Mac:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

Luego debe instalar las dependencias con el siguiente comando:

```bash
pip install -r requirements.txt
```

Despues debe moverse a la carpeta "pachacursos" con el siguiente comando:

```bash
cd pachacursos
```

La base de datos utilizada es PostgreSQL, por lo que se debe crear una base de datos con el nombre "pachacursos" y luego correr las migraciones con el siguiente comando:

```bash
python manage.py migrate
```

## Uso

Luego debe crearse un superusuario con el siguiente comando:

```bash
python manage.py createsuperuser
```

Para correr el proyecto, se debe ejecutar el siguiente comando:

```bash
python manage.py runserver
```