# 🛒 Ecommerce con Django y PayPal Sandbox

Proyecto desarrollado con **Django** y **PayPal Sandbox**, desplegado en **Render**.  
Permite realizar pagos de prueba con PayPal en modo sandbox y visualizar el flujo completo de una tienda en línea funcional.

---
![Python](https://img.shields.io/badge/Python-3.13.7-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2.6-092E20?logo=django&logoColor=white)
![PayPal](https://img.shields.io/badge/PayPal-Sandbox-00457C?logo=paypal&logoColor=white)
![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ⚙️ Versiones utilizadas

| Herramienta | Versión |
|--------------|----------|
| **Python** | 3.13.7 |
| **Django** | 5.2.6 |
| **VS Code** | 1.104.2 |

---

## 🚀 Instalación y configuración en local

### 1 Instalar Python
Descarga e instala Python desde la página oficial:  
👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

> 💡 Asegúrate de marcar la opción **"Add Python to PATH"** durante la instalación.

### 2 Instala Django:
pip install django

### 3 Instala la librería PayPal:
pip install django-paypal


### 4 Instala el SDK de PayPal:
pip install paypalrestsdk

O simplemente instala todo con el archivo requirements.txt:
pip install -r requirements.txt

### 5 Migraciones de base de datos

Ejecuta los siguientes comandos desde la terminal en la carpeta del proyecto:
python ec/manage.py makemigrations
python ec/manage.py migrate

### 6 Ejecutar el servidor local
python ec/manage.py runserver

Luego abre en tu navegador:
👉 http://127.0.0.1:8000/
---------------------------------------------------------------------
💳 Integración con PayPal Sandbox

Este proyecto utiliza PayPal Sandbox para pruebas de pago.
Configura tus credenciales en el archivo settings.py o mediante variables de entorno:

PAYPAL_CLIENT_ID = 'TU_CLIENT_ID_SANDBOX'
PAYPAL_CLIENT_SECRET = 'TU_CLIENT_SECRET_SANDBOX'
PAYPAL_MODE = 'sandbox'


Puedes obtener tus credenciales desde:
👉 https://developer.paypal.com/dashboard/applications/sandbox

🌐 Proyecto en línea

Puedes ver el sistema desplegado en Render en el siguiente enlace:
🔗 https://minino-archives.onrender.com


🧑‍💻 Desarrollado por

Cristian Parada López
📧 (cristianparadalopez@gmail.com)
    (paradalopezcristianalexander@gmail.com

📜 Licencia

Este proyecto se publica bajo la licencia MIT, por lo que puedes modificarlo y usarlo libremente dando el crédito correspondiente.
