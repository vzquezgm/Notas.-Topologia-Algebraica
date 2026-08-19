from extraer_ejercicios import (
    obtener_ejercicios_actuales,
    leer_ejercicios_generados,
    generar_ejercicios_tex,
)

from gestionar_ids import (
    asignar_ids,
)

from comparar_ejercicios import (
    comparar,
    imprimir_resultado,
)

from gestionar_proyecto_b import (
    sincronizar_proyecto_b,
)


def main():

    print("=" * 60)
    print("SINCRONIZADOR DE EJERCICIOS")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Guardar estado anterior
    # --------------------------------------------------------

    ejercicios_anteriores = (
        leer_ejercicios_generados()
    )

    # --------------------------------------------------------
    # 2. Asignar IDs nuevos
    # --------------------------------------------------------

    nuevos_ids = asignar_ids()

    print()
    print(
        f"IDs nuevos asignados: "
        f"{nuevos_ids}"
    )

    # --------------------------------------------------------
    # 3. Leer A actual
    # --------------------------------------------------------

    ejercicios_actuales = (
        obtener_ejercicios_actuales()
    )

    # --------------------------------------------------------
    # 4. Comparar
    # --------------------------------------------------------

    resultado = comparar(
        ejercicios_anteriores,
        ejercicios_actuales,
    )

    imprimir_resultado(
        resultado
    )

    # --------------------------------------------------------
    # 5. Generar ejercicios.tex
    # --------------------------------------------------------

    generar_ejercicios_tex(
        ejercicios_actuales
    )

    # --------------------------------------------------------
    # 6. Sincronizar Proyecto B
    # --------------------------------------------------------

    sincronizar_proyecto_b(
        ejercicios_actuales,
        resultado
    )

    print()
    print("=" * 60)
    print("PROCESO TERMINADO")
    print("=" * 60)


if __name__ == "__main__":
    main()