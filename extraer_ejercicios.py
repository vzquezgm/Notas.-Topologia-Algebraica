from pathlib import Path
import re

# Carpeta raíz del Proyecto A
PROYECTO = Path(".")

# Archivo que generaremos
SALIDA = PROYECTO / "ejercicios.tex"


def numero_archivo(archivo):
    """
    Obtiene el número inicial del nombre del archivo.

    Ejemplos:
        0.Introduccion.tex        -> 0
        1.Grupo-fundamental.tex   -> 1
        10.Homologia.tex          -> 10

    Los archivos que no comiencen con un número
    se colocan al final.
    """
    coincidencia = re.match(r"^\s*(\d+)", archivo.stem)

    if coincidencia:
        return int(coincidencia.group(1))

    return float("inf")


def extraer_ejercicios(archivo):
    """
    Extrae todos los entornos:

        \\begin{ejercicio}
        ...
        \\end{ejercicio}

    conservando íntegramente su contenido.
    """
    texto = archivo.read_text(encoding="utf-8")

    patron = re.compile(
        r"\\begin\{ejercicio\}.*?\\end\{ejercicio\}",
        re.DOTALL
    )

    return patron.findall(texto)


def main():

    ejercicios = []

    # Buscar todos los archivos .tex
    archivos = list(PROYECTO.rglob("*.tex"))

    # Ordenarlos por el número inicial del nombre
    archivos.sort(key=numero_archivo)

    for archivo in archivos:

        # No procesar el archivo de salida
        if archivo.resolve() == SALIDA.resolve():
            continue

        encontrados = extraer_ejercicios(archivo)

        if encontrados:
            print(
                f"{archivo}: "
                f"{len(encontrados)} ejercicio(s)"
            )

            ejercicios.extend(encontrados)

    # Crear el contenido final
    contenido = "\n\n".join(ejercicios)

    # Escribir ejercicios.tex
    SALIDA.write_text(
        contenido + "\n",
        encoding="utf-8"
    )

    print()
    print(
        f"Total de ejercicios encontrados: "
        f"{len(ejercicios)}"
    )
    print(f"Archivo generado: {SALIDA}")


if __name__ == "__main__":
    main()