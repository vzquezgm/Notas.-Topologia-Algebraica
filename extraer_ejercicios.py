from pathlib import Path
import re

PROYECTO = Path(".")
SALIDA = PROYECTO / "ejercicios.tex"

PATRON_EJERCICIO = re.compile(
    r"\\begin\{ejercicio\}.*?\\end\{ejercicio\}",
    re.DOTALL
)

PATRON_ID = re.compile(
    r"%\s*ID:\s*(\d+)"
)


def numero_archivo(archivo):
    """
    Ordena los archivos por el número inicial de su nombre.

    Ejemplo:
        0.Introduccion.tex  -> 0
        1.Grupo.tex         -> 1
        10.Homologia.tex    -> 10
    """

    coincidencia = re.match(
        r"^\s*(\d+)",
        archivo.stem
    )

    if coincidencia:
        return int(coincidencia.group(1))

    return float("inf")


def obtener_archivos_tex():
    """
    Obtiene todos los archivos .tex del proyecto,
    ordenados numéricamente.
    """

    archivos = list(
        PROYECTO.rglob("*.tex")
    )

    archivos = [
        archivo
        for archivo in archivos
        if archivo.resolve() != SALIDA.resolve()
    ]

    archivos.sort(
        key=numero_archivo
    )

    return archivos


def extraer_ejercicios_de_texto(texto):
    """
    Extrae los entornos ejercicio de un texto.
    """

    return PATRON_EJERCICIO.findall(texto)


def extraer_ejercicios_de_archivo(archivo):
    """
    Extrae los ejercicios de un archivo.
    """

    texto = archivo.read_text(
        encoding="utf-8"
    )

    return extraer_ejercicios_de_texto(texto)


def obtener_id(ejercicio):
    """
    Obtiene el ID contenido dentro de un ejercicio.

    Ejemplo:

        \\begin{ejercicio}
            % ID: 7
            ...
        \\end{ejercicio}
    """

    coincidencia = PATRON_ID.search(
        ejercicio
    )

    if coincidencia:
        return int(
            coincidencia.group(1)
        )

    return None


def obtener_ejercicios_actuales():
    """
    Devuelve todos los ejercicios actuales de A,
    en el orden en que aparecen en las notas.

    Cada elemento es un diccionario con:

        archivo
        contenido
        id
    """

    ejercicios = []

    for archivo in obtener_archivos_tex():

        encontrados = (
            extraer_ejercicios_de_archivo(
                archivo
            )
        )

        for ejercicio in encontrados:

            ejercicios.append(
                {
                    "archivo": archivo,
                    "contenido": ejercicio,
                    "id": obtener_id(ejercicio)
                }
            )

    return ejercicios


def leer_ejercicios_generados():
    """
    Lee el archivo ejercicios.tex anterior.

    Devuelve los ejercicios que tenía B/A
    en la ejecución anterior.
    """

    if not SALIDA.exists():
        return []

    texto = SALIDA.read_text(
        encoding="utf-8"
    )

    ejercicios = (
        extraer_ejercicios_de_texto(texto)
    )

    return [
        {
            "contenido": ejercicio,
            "id": obtener_id(ejercicio)
        }
        for ejercicio in ejercicios
    ]


def obtener_orden_anterior():
    """
    Devuelve únicamente los IDs del estado anterior.
    """

    ejercicios = leer_ejercicios_generados()

    return [
        ejercicio["id"]
        for ejercicio in ejercicios
        if ejercicio["id"] is not None
    ]


def generar_ejercicios_tex(ejercicios):
    """
    Genera ejercicios.tex usando el orden actual.
    """

    contenido = "\n\n".join(
        ejercicio["contenido"]
        for ejercicio in ejercicios
    )

    SALIDA.write_text(
        contenido + "\n",
        encoding="utf-8"
    )
    