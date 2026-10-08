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