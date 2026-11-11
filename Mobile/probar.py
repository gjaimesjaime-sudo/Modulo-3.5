
import requests
import json

URL = "http://127.0.0.1/gamezone_pro/api/ranking/listar.php"

try:
    with open("token_prueba.txt", "r", encoding="utf-8") as archivo:
        token = archivo.read().strip()

    respuesta = requests.get(
        URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=10
    )

    print("Código HTTP:", respuesta.status_code)

    try:
        datos = respuesta.json()

        # Mostrar TODA la respuesta del servidor.
        print("\nRESPUESTA COMPLETA DEL SERVIDOR:")
        print(json.dumps(datos, indent=4, ensure_ascii=False))

        if datos.get("success"):
            print("\nRANKING DE GAMEZONE PRO")

            for jugador in datos.get("ranking", []):
                print(
                    f'{jugador.get("posicion")} - '
                    f'{jugador.get("nickname")} - '
                    f'ELO: {jugador.get("elo")}'
                )
        else:
            print("\nERROR REAL:", datos.get("error_real"))
            print("ARCHIVO:", datos.get("archivo"))
            print("LÍNEA:", datos.get("linea"))

    except ValueError:
        print("Respuesta no válida en JSON:")
        print(respuesta.text)

except FileNotFoundError:
    print("No se encontró token_prueba.txt. Inicia sesión primero.")

except requests.exceptions.RequestException as error:
    print("Error de conexión:", error)
