# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Integrantes:
#  - Valentin Zaccari
#  - Valentino Sarniguette
#  - Franco Garcia Lesme
#  - Sanchez De Ignacio Tomas
#  - Albornoz Thiago Agustin
#  - Trezeguet Gaston
#
#  Comision: 9480
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO, MISION_LARGA


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Verifica si un comando tiene el formato correcto.

    Los comandos avanzar y girar reciben una velocidad y un tiempo.
    Los comandos detenerse y saludar no reciben parametros.
    Para avanzar y girar, comprueba que los valores sean numericos
    y que el tiempo no sea negativo.

    Devuelve True si el comando es valido y False en caso contrario.
    """
    try:
        if len(comando) == 0:
            return False
    except TypeError:
        return False

    nombre = comando[0]

    if nombre == "detenerse" or nombre == "saludar":
        return len(comando) == 1

    if nombre == "avanzar" or nombre == "girar":
        if len(comando) != 3:
            return False

        velocidad = comando[1]
        tiempo = comando[2]

        try:
            velocidad + 0
            tiempo + 0
        except TypeError:
            return False

        if tiempo < 0:
            return False

        return True

    return False


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """ Ejecuta un comando del robot y devuelve un mensaje con el resultado.

    Segun el nombre del comando, el robot avanza, gira, se detiene
    o saluda. Si el robot produce un ErrorDeSeguridad, devuelve
    un mensaje de rechazo con el motivo.
    """
    nombre = comando[0]

    try:

        if nombre == "avanzar":

            robot.avanzar(velocidad=comando[1], tiempo=comando[2])

        elif nombre == "girar":

            robot.girar(velocidad=comando[1], tiempo=comando[2])

        elif nombre == "detenerse":

            robot.detenerse()

        elif nombre == "saludar":

            robot.saludar()

    except ErrorDeSeguridad as error:

        return f"Rechazado por el robot: {comando} -> {error}"

    return f"Ejecutado: {comando}"


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================

def ejecutar_mision(robot, mision, historial):
    """Ejecuta los comandos de una mision y registra sus resultados.

    Valida cada comando antes de ejecutarlo. Los comandos invalidos
    o rechazados se registran sin interrumpir la mision.
    Guarda en historial el comando, si se ejecuto y su detalle.
    """
    for comando in mision:
        if comando_es_valido(comando):
            detalle = ejecutar_comando(robot, comando)
            ejecutado = not detalle.startswith("Rechazado")
        else:
            detalle = "Comando invalido"
            ejecutado = False

        print(comando, "->", detalle)
        historial.append({"comando": comando, "ejecutado": ejecutado, "detalle": detalle})


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra un resumen de los comandos ejecutados en la mision.

    Cuenta los comandos aceptados y rechazados del historial.
    Si hubo rechazos, muestra cada comando y su motivo.
    """
    com_aceptados = 0
    com_rechazados = 0
    motivos = []

     #historial es una lista de diccionarios con 3 pares clave-valor
    for dic in historial:
        if dic["ejecutado"]:
            com_aceptados += 1
        else:
            com_rechazados += 1
            motivos.append((dic["comando"], dic["detalle"]))

    print("\n===REPORTE===\n")
    print(f"Comandos Aceptados: {com_aceptados}, Comandos Rechazados: {com_rechazados}")
    if motivos:
        print("\n[i] Motivos Rechazo:")
        for x, y in motivos:
            print(f"Comando: {x} --> Motivo: {y} ")


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    try:
        ejecutar_mision(robot, MISION_CON_ERRORES, historial)
            
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
