from pathlib import Path
import os
import re


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Directorio del Proyecto A
PROYECTO = Path(__file__).resolve().parent

# Archivo generado
SALIDA = PROYECTO / "ejercicios.tex"


# ============================================================
# PATRONES
# ============================================================

PATRON_EJERCICIO = re.compile(
    r"\\begin\{ejercicio\}.*?"
    r"\\end\{ejercicio\}",
    re.DOTALL
)

PATRON_ID = re.compile(
    r"%\s*ID:\s*(\d+)"
)


# ============================================================
# EXCLUSIONES
# ============================================================

def obtener_directorios_excluidos():
    """
    Obtiene los directorios que no deben ser recorridos.

    En GitHub Actions, Proyecto B se clona dentro
    del mismo workspace que Proyecto A, por lo que
    debemos excluirlo explícitamente.
    """

    excluidos = []

    proyecto_b = os.environ.get(
        "PROYECTO_B"
    )

    if proyecto_b:

        ruta_b = Path(
            proyecto_b
        )

        if not ruta_b.is_absolute():
            ruta_b = (
                Path.cwd()
                / ruta_b
            )

        excluidos.append(
            ruta_b.resolve()
        )

    return excluidos


def esta_excluido(
    archivo,
    directorios_excluidos
):
    """
    Comprueba si un archivo está dentro
    de un directorio excluido.
    """

    archivo = archivo.resolve()

    for directorio in directorios_excluidos:

        try:
            archivo.relative_to(
                directorio
            )

            return True

        except ValueError:
            pass

    return False


# ============================================================
# ORDEN DE LOS ARCHIVOS
# ============================================================

def numero_archivo(archivo):

    coincidencia = re.match(
        r"^\s*(\d+)",
        archivo.stem
    )

    if coincidencia:
        return int(
            coincidencia.group(1)
        )

    return float("inf")


def obtener_archivos_tex():
    """
    Obtiene únicamente los .tex del Proyecto A.

    Excluye ejercicios.tex y, cuando corresponde,
    el Proyecto B.
    """

    directorios_excluidos = (
        obtener_directorios_excluidos()
    )

    archivos = []

    for archivo in PROYECTO.rglob("*.tex"):

        if archivo.resolve() == SALIDA.resolve():
            continue

        if esta_excluido(
            archivo,
            directorios_excluidos
        ):
            continue

        archivos.append(
            archivo
        )

    archivos.sort(
        key=numero_archivo
    )

    return archivos


# ============================================================
# EXTRAER EJERCICIOS
# ============================================================

def extraer_ejercicios_de_texto(
    texto
):

    return PATRON_EJERCICIO.findall(
        texto
    )


def extraer_ejercicios_de_archivo(
    archivo
):

    texto = archivo.read_text(
        encoding="utf-8"
    )

    return (
        extraer_ejercicios_de_texto(
            texto
        )
    )


# ============================================================
# OBTENER ID
# ============================================================

def obtener_id(
    ejercicio
):

    coincidencia = PATRON_ID.search(
        ejercicio
    )

    if coincidencia:

        return int(
            coincidencia.group(1)
        )

    return None


# ============================================================
# EJERCICIOS ACTUALES
# ============================================================

def obtener_ejercicios_actuales():

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
                    "id": obtener_id(
                        ejercicio
                    )
                }
            )

    return ejercicios


# ============================================================
# LEER ESTADO ANTERIOR
# ============================================================

def leer_ejercicios_generados():

    if not SALIDA.exists():
        return []

    texto = SALIDA.read_text(
        encoding="utf-8"
    )

    ejercicios = (
        extraer_ejercicios_de_texto(
            texto
        )
    )

    return [
        {
            "contenido": ejercicio,
            "id": obtener_id(
                ejercicio
            )
        }
        for ejercicio in ejercicios
    ]


def obtener_orden_anterior():

    ejercicios = (
        leer_ejercicios_generados()
    )

    return [
        ejercicio["id"]
        for ejercicio in ejercicios
        if ejercicio["id"] is not None
    ]


# ============================================================
# GENERAR ejercicios.tex
# ============================================================

def generar_ejercicios_tex(
    ejercicios
):

    contenido = "\n\n".join(
        ejercicio["contenido"]
        for ejercicio in ejercicios
    )

    SALIDA.write_text(
        contenido + "\n",
        encoding="utf-8"
    )