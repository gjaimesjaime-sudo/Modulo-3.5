
import requests

# Dirección de la API
URL = "http://127.0.0.1/gamezone_pro/api/probar_conexion.php"

try:
    respuesta = requests.get(URL, timeout=10)

    print("Código HTTP:", respuesta.status_code)

    datos = respuesta.json()

    if datos.get("success"):
        print("CONEXIÓN EXITOSA")
        print(datos["mensaje"])
    else:
        print("ERROR:", datos)

except requests.exceptions.ConnectionError:
    print("No se pudo conectar con el servidor XAMPP.")

except requests.exceptions.Timeout:
    print("El servidor tardó demasiado en responder.")

except Exception as error:
    print("Error:", error)
