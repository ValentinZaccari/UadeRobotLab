from mi_tp02 import comando_es_valido, ejecutar_comando
from robot import ErrorDeSeguridad

# =====================================================================
# PRUEBAS PARA comando_es_valido
# =====================================================================

def test_comando_es_valido_camino_feliz():
    assert comando_es_valido(("avanzar", 0.2, 2.0)) == True
    assert comando_es_valido(("girar", -0.5, 3.14)) == True
    assert comando_es_valido(("detenerse",)) == True
    assert comando_es_valido(("saludar",)) == True

def test_comando_es_valido_errores_de_formato():
    assert comando_es_valido(()) == False  
    assert comando_es_valido(("volar", 0.2, 1.0)) == False  
    assert comando_es_valido(("avanzar", 0.2)) == False  
    assert comando_es_valido(("detenerse", 5.0)) == False  

def test_comando_es_valido_errores_de_tipo_y_valor():
    assert comando_es_valido(("avanzar", "rapido", 2.0)) == False  
    assert comando_es_valido(("girar", 0.5, "mucho")) == False  
    assert comando_es_valido(("avanzar", 0.2, -3.0)) == False  

# =====================================================================
# PRUEBAS PARA ejecutar_comando
# =====================================================================

class RobotSimulado:
    def avanzar(self, velocidad, tiempo):
        if velocidad > 0.8:
            raise ErrorDeSeguridad("Supera la velocidad permitida")
    
    def girar(self, velocidad, tiempo): pass
    def detenerse(self): pass
    def saludar(self): pass

def test_ejecutar_comando_exitoso():
    robot = RobotSimulado()
    resultado = ejecutar_comando(robot, ("avanzar", 0.2, 2.0))
    assert resultado == "Ejecutado: ('avanzar', 0.2, 2.0)"

def test_ejecutar_comando_rechazado_por_excepcion():
    robot = RobotSimulado()
    resultado = ejecutar_comando(robot, ("avanzar", 0.9, 2.0))
    assert resultado.startswith("Rechazado por el robot:")
# =====================================================================
# PRUEBAS DE LAS CUATRO MISIONES COMPLETAS Y EL REPORTE
# =====================================================================
from mi_tp02 import ejecutar_mision, generar_reporte
from misiones import MISION_BASICA, MISION_CUADRADO, MISION_CON_ERRORES, MISION_LARGA

class RobotParaMisiones:
    def avanzar(self, velocidad, tiempo):
        if abs(velocidad) > 0.2 or tiempo > 10:
            raise ErrorDeSeguridad("Limite de avance o tiempo superado")

    def girar(self, velocidad, tiempo):
        if abs(velocidad) > 0.5 or tiempo > 10:
            raise ErrorDeSeguridad("Limite de giro o tiempo superado")

    def detenerse(self):
        pass

    def saludar(self):
        pass


def probar_mision(mision, esperados_ok, esperados_rechazados, capsys):
    robot = RobotParaMisiones()
    historial = []
    ejecutar_mision(robot, mision, historial)

    assert len(historial) == len(mision)
    aceptados = 0
    rechazados = 0
    for resultado in historial:
        if resultado["ejecutado"]:
            aceptados += 1
        else:
            rechazados += 1
            assert resultado["detalle"] != ""

    assert aceptados == esperados_ok
    assert rechazados == esperados_rechazados

    generar_reporte(historial)
    salida = capsys.readouterr().out
    assert "Comandos Aceptados: " + str(esperados_ok) in salida
    assert "Comandos Rechazados: " + str(esperados_rechazados) in salida
    if esperados_rechazados > 0:
        assert "Motivo:" in salida


def test_mision_basica_completa(capsys):
    probar_mision(MISION_BASICA, 4, 0, capsys)


def test_mision_cuadrado_completa(capsys):
    probar_mision(MISION_CUADRADO, 9, 0, capsys)


def test_mision_con_errores_completa(capsys):
    probar_mision(MISION_CON_ERRORES, 4, 7, capsys)


def test_mision_larga_completa(capsys):
    probar_mision(MISION_LARGA, 9, 0, capsys)
