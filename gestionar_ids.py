import re

from extraer_ejercicios import (
    obtener_archivos_tex,
    PATRON_EJERCICIO,
    PATRON_ID,
    extraer_ejercicios_de_archivo,
    obtener_id,
)


def obtener_ids_existentes():
    """
    Obtiene todos los IDs que ya existen en A.
    """

    ids = []

    for archivo in obtener_archivos_tex():

        ejercicios = (
            extraer_ejercicios_de_archivo(
                archivo
            )
        )

        for ejercicio in ejercicios:

            id_ = obtener_id(ejercicio)

            if id_ is not None:
                ids.append(id_)

    return ids


def comprobar_ids_unicos(ids):
    """
    Verifica que no existan IDs repetidos.
    """

    repetidos = {
        id_
        for id_ in ids
        if ids.count(id_) > 1
    }

    if repetidos:

        raise ValueError(
            "Hay IDs repetidos: "
            + ", ".join(
                map(str, sorted(repetidos))
            )
        )


def insertar_id_en_ejercicio(
    ejercicio,
    id_nuevo
):
    """
    Inserta:

        % ID: N

    inmediatamente después de
    \\begin{ejercicio}.
    """

    inicio = r"\begin{ejercicio}"

    reemplazo = (
        inicio
        + "\n    "
        + f"% ID: {id_nuevo}"
    )

    return ejercicio.replace(
        inicio,
        reemplazo,
        1
    )


def asignar_ids():
    """
    Encuentra ejercicios sin ID y les asigna
    el siguiente ID disponible.

    Los IDs existentes nunca se modifican.
    """

    archivos = obtener_archivos_tex()

    ids_existentes = (
        obtener_ids_existentes()
    )

    comprobar_ids_unicos(
        ids_existentes
    )

    if ids_existentes:
        siguiente_id = (
            max(ids_existentes) + 1
        )
    else:
        siguiente_id = 1

    total_nuevos = 0

    for archivo in archivos:

        texto = archivo.read_text(
            encoding="utf-8"
        )

        ejercicios = list(
            PATRON_EJERCICIO.finditer(
                texto
            )
        )

        if not ejercicios:
            continue

        partes = []
        posicion = 0
        hubo_cambios = False

        for match in ejercicios:

            inicio = match.start()
            fin = match.end()

            partes.append(
                texto[posicion:inicio]
            )

            bloque = match.group(0)

            id_actual = obtener_id(
                bloque
            )

            if id_actual is None:

                bloque = (
                    insertar_id_en_ejercicio(
                        bloque,
                        siguiente_id
                    )
                )

                print(
                    f"{archivo}: "
                    f"nuevo ejercicio → "
                    f"ID {siguiente_id}"
                )

                siguiente_id += 1
                total_nuevos += 1
                hubo_cambios = True

            partes.append(bloque)

            posicion = fin

        partes.append(
            texto[posicion:]
        )

        nuevo_texto = "".join(
            partes
        )

        if hubo_cambios:

            archivo.write_text(
                nuevo_texto,
                encoding="utf-8"
            )

    comprobar_ids_unicos(
        [
            id_
            for id_
            in obtener_ids_existentes()
        ]
    )

    return total_nuevos