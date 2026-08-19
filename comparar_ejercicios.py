def comparar(
    ejercicios_anteriores,
    ejercicios_actuales
):
    """
    Compara el estado anterior con el actual.

    Devuelve:

        nuevos
        eliminados
        movidos
        modificados
        sin_cambio
    """

    mapa_anterior = {
        ejercicio["id"]: ejercicio
        for ejercicio in ejercicios_anteriores
        if ejercicio["id"] is not None
    }

    mapa_actual = {
        ejercicio["id"]: ejercicio
        for ejercicio in ejercicios_actuales
        if ejercicio["id"] is not None
    }

    orden_anterior = [
        ejercicio["id"]
        for ejercicio in ejercicios_anteriores
        if ejercicio["id"] is not None
    ]

    orden_actual = [
        ejercicio["id"]
        for ejercicio in ejercicios_actuales
        if ejercicio["id"] is not None
    ]

    posiciones_anteriores = {
        id_: posicion + 1
        for posicion, id_
        in enumerate(orden_anterior)
    }

    posiciones_actuales = {
        id_: posicion + 1
        for posicion, id_
        in enumerate(orden_actual)
    }

    # --------------------------------------------------------
    # NUEVOS
    # --------------------------------------------------------

    nuevos = [
        id_
        for id_ in orden_actual
        if id_ not in mapa_anterior
    ]

    # --------------------------------------------------------
    # ELIMINADOS
    # --------------------------------------------------------

    eliminados = [
        id_
        for id_ in orden_anterior
        if id_ not in mapa_actual
    ]

    # --------------------------------------------------------
    # MOVIDOS
    # --------------------------------------------------------

    movidos = []

    for id_ in orden_actual:

        if id_ not in mapa_anterior:
            continue

        posicion_anterior = (
            posiciones_anteriores[id_]
        )

        posicion_actual = (
            posiciones_actuales[id_]
        )

        if (
            posicion_anterior
            != posicion_actual
        ):

            movidos.append(
                {
                    "id": id_,
                    "posicion_anterior":
                        posicion_anterior,
                    "posicion_actual":
                        posicion_actual,
                }
            )

    # --------------------------------------------------------
    # MODIFICADOS
    # --------------------------------------------------------

    modificados = []

    for id_ in orden_actual:

        if id_ not in mapa_anterior:
            continue

        contenido_anterior = (
            mapa_anterior[id_]["contenido"]
        )

        contenido_actual = (
            mapa_actual[id_]["contenido"]
        )

        if (
            contenido_anterior
            != contenido_actual
        ):

            modificados.append(
                {
                    "id": id_,
                    "posicion":
                        posiciones_actuales[id_],
                    "anterior":
                        contenido_anterior,
                    "actual":
                        contenido_actual,
                }
            )

    # --------------------------------------------------------
    # SIN CAMBIO
    # --------------------------------------------------------

    sin_cambio = []

    for id_ in orden_actual:

        if id_ not in mapa_anterior:
            continue

        if id_ in [
            item["id"]
            for item in movidos
        ]:
            continue

        if id_ in [
            item["id"]
            for item in modificados
        ]:
            continue

        sin_cambio.append(id_)

    return {
        "nuevos": nuevos,
        "eliminados": eliminados,
        "movidos": movidos,
        "modificados": modificados,
        "sin_cambio": sin_cambio,
    }


def imprimir_resultado(resultado):

    print()
    print("=" * 60)
    print("RESULTADO DE LA COMPARACIÓN")
    print("=" * 60)

    print()
    print("NUEVOS:")

    if resultado["nuevos"]:
        for id_ in resultado["nuevos"]:
            print(f"  ID {id_}")
    else:
        print("  Ninguno")

    print()
    print("ELIMINADOS:")

    if resultado["eliminados"]:
        for id_ in resultado["eliminados"]:
            print(f"  ID {id_}")
    else:
        print("  Ninguno")

    print()
    print("MOVIDOS:")

    if resultado["movidos"]:
        for item in resultado["movidos"]:
            print(
                f"  ID {item['id']}: "
                f"{item['posicion_anterior']} "
                f"→ "
                f"{item['posicion_actual']}"
            )
    else:
        print("  Ninguno")

    print()
    print("MODIFICADOS:")

    if resultado["modificados"]:
        for item in resultado["modificados"]:
            print(
                f"  ID {item['id']} "
                f"(posición "
                f"{item['posicion']})"
            )
    else:
        print("  Ninguno")

    print()
    print("SIN CAMBIO:")

    if resultado["sin_cambio"]:
        print(
            "  "
            + ", ".join(
                map(
                    str,
                    resultado["sin_cambio"]
                )
            )
        )
    else:
        print("  Ninguno")
        