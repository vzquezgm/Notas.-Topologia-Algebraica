from pathlib import Path
import os
import re
import shutil

# ============================================================
# CONFIGURACIÓN
# ============================================================

# Proyecto B real
PROYECTO_B = Path(
    os.environ.get(
        "PROYECTO_B",
        "../Ejercicios.-Topologia-Algebraica"
    )
)

CARPETA_EJERCICIOS = (
    PROYECTO_B / "ejercicios"
)

CARPETA_ELIMINADOS = (
    PROYECTO_B / "ejercicios_eliminados"
)


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
# OBTENER ID
# ============================================================

def obtener_id(ejercicio):
    """
    Obtiene el ID contenido dentro del ejercicio.
    """

    coincidencia = PATRON_ID.search(
        ejercicio
    )

    if coincidencia:
        return int(
            coincidencia.group(1)
        )

    return None


# ============================================================
# NOMBRE DEL ARCHIVO SEGÚN POSICIÓN
# ============================================================

def nombre_archivo(posicion):
    """
    Ejemplo:

        1 -> Ejercicio_1.tex
        2 -> Ejercicio_2.tex
    """

    return (
        CARPETA_EJERCICIOS
        / f"Ejercicio_{posicion}.tex"
    )


# ============================================================
# OBTENER ARCHIVOS DE B
# ============================================================

def obtener_archivos_b():

    if not CARPETA_EJERCICIOS.exists():
        return []

    return list(
        CARPETA_EJERCICIOS.glob(
            "Ejercicio_*.tex"
        )
    )


# ============================================================
# OBTENER ID DE UN ARCHIVO
# ============================================================

def obtener_id_archivo(archivo):

    texto = archivo.read_text(
        encoding="utf-8"
    )

    ejercicios = PATRON_EJERCICIO.findall(
        texto
    )

    if not ejercicios:
        return None

    return obtener_id(
        ejercicios[0]
    )


# ============================================================
# MAPA DE B
# ============================================================

def construir_mapa_b():
    """
    Construye:

        ID -> archivo

    Ejemplo:

        1 -> Ejercicio_1.tex
        4 -> Ejercicio_3.tex
    """

    mapa = {}

    for archivo in obtener_archivos_b():

        id_ = obtener_id_archivo(
            archivo
        )

        if id_ is None:

            print(
                f"ADVERTENCIA: "
                f"{archivo.name} "
                f"no contiene un ID."
            )

            continue

        if id_ in mapa:

            raise ValueError(
                f"El ID {id_} aparece en "
                f"más de un archivo:\n"
                f"  {mapa[id_]}\n"
                f"  {archivo}"
            )

        mapa[id_] = archivo

    return mapa


# ============================================================
# ACTUALIZAR SOLO EL ENUNCIADO
# ============================================================

def actualizar_enunciado(
    contenido_existente,
    nuevo_ejercicio
):
    """
    Reemplaza exclusivamente el bloque:

        \\begin{ejercicio}
        ...
        \\end{ejercicio}

    Todo lo demás permanece intacto.
    """

    coincidencia = PATRON_EJERCICIO.search(
        contenido_existente
    )

    if coincidencia is None:

        raise ValueError(
            "El archivo existente no contiene "
            "un entorno ejercicio."
        )

    inicio = coincidencia.start()
    fin = coincidencia.end()

    return (
        contenido_existente[:inicio]
        + nuevo_ejercicio
        + contenido_existente[fin:]
    )


# ============================================================
# CREAR EJERCICIO NUEVO
# ============================================================

def crear_ejercicio(
    posicion,
    ejercicio
):
    """
    Crea un archivo nuevo con demostración vacía.
    """

    archivo = nombre_archivo(
        posicion
    )

    contenido = (
        ejercicio
        + "\n\n"
        + "\\begin{demostracion}\n"
        + "\n"
        + "\\end{demostracion}\n"
    )

    archivo.write_text(
        contenido,
        encoding="utf-8"
    )

    print(
        f"CREADO: {archivo.name} "
        f"(ID {obtener_id(ejercicio)})"
    )


# ============================================================
# ARCHIVAR ELIMINADO
# ============================================================

def archivar_archivo(
    archivo,
    id_
):
    """
    Archiva un ejercicio eliminado en:

        ejercicios_eliminados/
    """

    CARPETA_ELIMINADOS.mkdir(
        parents=True,
        exist_ok=True
    )

    destino = (
        CARPETA_ELIMINADOS
        / f"Ejercicio_ID_{id_}.tex"
    )

    contador = 2

    while destino.exists():

        destino = (
            CARPETA_ELIMINADOS
            / f"Ejercicio_ID_{id_}_{contador}.tex"
        )

        contador += 1

    shutil.move(
        str(archivo),
        str(destino)
    )

    print(
        f"ARCHIVADO: ID {id_} "
        f"→ {destino.name}"
    )


# ============================================================
# LEER INFORMACIÓN ACTUAL DE A
# ============================================================

def construir_estado_actual(
    ejercicios_actuales
):
    """
    Construye:

        ID -> posición
        ID -> contenido
    """

    posiciones = {}
    contenidos = {}

    for posicion, ejercicio in enumerate(
        ejercicios_actuales,
        start=1
    ):

        id_ = ejercicio["id"]

        if id_ is None:
            raise ValueError(
                "Existe un ejercicio sin ID."
            )

        if id_ in posiciones:
            raise ValueError(
                f"El ID {id_} está repetido."
            )

        posiciones[id_] = posicion
        contenidos[id_] = (
            ejercicio["contenido"]
        )

    return posiciones, contenidos


# ============================================================
# SINCRONIZAR PROYECTO B
# ============================================================

def sincronizar_proyecto_b(
    ejercicios_actuales,
    resultado
):
    """
    Sincroniza B.

    Reglas:

    1. A controla los enunciados.
    2. B conserva las demostraciones.
    3. El ID identifica al ejercicio.
    4. El nombre del archivo indica la posición.
    5. Los eliminados se archivan.
    6. Los archivos sin cambios no se modifican.
    """

    CARPETA_EJERCICIOS.mkdir(
        parents=True,
        exist_ok=True
    )

    mapa_b = construir_mapa_b()

    posiciones_actuales, contenidos_actuales = (
        construir_estado_actual(
            ejercicios_actuales
        )
    )

    # ========================================================
    # 1. ARCHIVAR ELIMINADOS
    # ========================================================

    for id_ in resultado["eliminados"]:

        archivo = mapa_b.get(id_)

        if archivo is None:
            continue

        if archivo.exists():

            archivar_archivo(
                archivo,
                id_
            )

        del mapa_b[id_]

    # ========================================================
    # 2. DETERMINAR QUÉ EJERCICIOS REALMENTE CAMBIARON
    # ========================================================

    movidos = {
        item["id"]
        for item in resultado["movidos"]
    }

    modificados = {
        item["id"]
        for item in resultado["modificados"]
    }

    nuevos = set(
        resultado["nuevos"]
    )

    deben_moverse = (
        movidos
        | modificados
        | nuevos
    )

    # ========================================================
    # 3. SOLO LOS ARCHIVOS QUE CAMBIARÁN VAN A TEMPORALES
    # ========================================================

    temporales = {}

    for id_ in deben_moverse:

        if id_ not in mapa_b:
            continue

        archivo = mapa_b[id_]

        temporal = (
            CARPETA_EJERCICIOS
            / f".tmp_ID_{id_}.tex"
        )

        if temporal.exists():
            temporal.unlink()

        archivo.rename(
            temporal
        )

        temporales[id_] = temporal

        print(
            f"TEMPORAL: "
            f"{archivo.name} "
            f"→ {temporal.name}"
        )

    # ========================================================
    # 4. PROCESAR EJERCICIOS EN EL ORDEN ACTUAL
    # ========================================================

    for posicion, ejercicio in enumerate(
        ejercicios_actuales,
        start=1
    ):

        id_ = ejercicio["id"]

        nuevo_ejercicio = (
            ejercicio["contenido"]
        )

        destino = nombre_archivo(
            posicion
        )

        # ----------------------------------------------------
        # NUEVO
        # ----------------------------------------------------

        if id_ in nuevos:

            crear_ejercicio(
                posicion,
                nuevo_ejercicio
            )

            continue

        # ----------------------------------------------------
        # EXISTENTE SIN CAMBIOS
        # ----------------------------------------------------

        if id_ not in deben_moverse:

            # No hacemos absolutamente nada.
            continue

        # ----------------------------------------------------
        # EXISTENTE QUE DEBE ACTUALIZARSE/MOVERSE
        # ----------------------------------------------------

        archivo_temporal = (
            temporales.get(id_)
        )

        if archivo_temporal is None:

            raise RuntimeError(
                f"No se encontró archivo "
                f"temporal para el ID {id_}."
            )

        contenido_existente = (
            archivo_temporal.read_text(
                encoding="utf-8"
            )
        )

        contenido_nuevo = (
            actualizar_enunciado(
                contenido_existente,
                nuevo_ejercicio
            )
        )

        archivo_temporal.write_text(
            contenido_nuevo,
            encoding="utf-8"
        )

        archivo_temporal.rename(
            destino
        )

        print(
            f"ACTUALIZADO: "
            f"{destino.name} "
            f"(ID {id_})"
        )

        del temporales[id_]

    # ========================================================
    # 5. VERIFICAR TEMPORALES RESTANTES
    # ========================================================

    if temporales:

        raise RuntimeError(
            "Quedaron archivos temporales "
            "sin procesar:\n"
            + "\n".join(
                str(archivo)
                for archivo in temporales.values()
            )
        )

    temporales_restantes = list(
        CARPETA_EJERCICIOS.glob(
            ".tmp_ID_*.tex"
        )
    )

    if temporales_restantes:

        raise RuntimeError(
            "Se encontraron archivos "
            "temporales después de terminar:\n"
            + "\n".join(
                str(archivo)
                for archivo
                in temporales_restantes
            )
        )

    print()
    print(
        "Proyecto B actualizado correctamente."
    )
