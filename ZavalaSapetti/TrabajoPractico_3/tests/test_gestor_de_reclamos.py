import datetime
import unittest
from modules.gestor_de_reclamos import GestorDeReclamos
from modules.entidades import Reclamo, Usuario
from modules.comparador_de_strings_en_español import ComparadorDeStrings
from modules.repositorio_falso import RepositorioFalso

class TestGestorDeReclamos(unittest.TestCase):

    def setUp(self):
        self.repositorio = RepositorioFalso()
        self.gestor_reclamos = GestorDeReclamos(self.repositorio)

    def test_crear_reclamo(self):
        usuario = Usuario({"id": 1, "nombre": "Juan", "apellido": "Perez", "usuario": "juanp", "email": "juan@example.com", "password": "1234", "rol": "usuario"})
        self.repositorio.guardar_usuario(usuario)

        reclamo = self.gestor_reclamos.crear_reclamo(
            usuario.id, "Problema con el servicio", "imagen.png", "No funciona el internet", 0
        )

        self.assertEqual(len(self.repositorio.get_lista_reclamos()), 1)
        self.assertEqual(self.repositorio.get_lista_reclamos()[0].asunto, "Problema con el servicio")

    def test_cambiar_estado_de_reclamo(self):
        usuario = Usuario({"id": 1, "nombre": "Juan", "apellido": "Perez", "usuario": "juanp", "email": "juan@example.com", "password": "1234", "rol": "usuario"})
        self.repositorio.guardar_usuario(usuario)

        reclamo = Reclamo({
            "id": 1,
            "usuario_id": usuario.id,
            "asunto": "Problema con el servicio",
            "contenido": "No funciona el internet",
            "imagen": "imagen.png",
            "departamento_correspondiente": "IT",
            "fecha": "2024-06-25",
            "estado": "Pendiente",
            "tiempo_de_resolucion": 0,
            "usuarios_adheridos": [],
            "fecha_inicio_proceso": None
        })
        self.repositorio.guardar_reclamo(reclamo)

        self.gestor_reclamos.cambiar_estado_de_reclamo(reclamo.id, "Resuelto")

        reclamo_actualizado = self.repositorio.leer_reclamo(reclamo.id)
        self.assertEqual(reclamo_actualizado.estado, "Resuelto")

    def test_cambiar_estado_de_reclamo_en_proceso(self):
        usuario = Usuario({"id": 1, "nombre": "Juan", "apellido": "Perez", "usuario": "juanp", "email": "juan@example.com", "password": "1234", "rol": "usuario"})
        self.repositorio.guardar_usuario(usuario)

        reclamo = Reclamo({
            "id": 1,
            "usuario_id": usuario.id,
            "asunto": "Problema con el servicio",
            "contenido": "No funciona el internet",
            "imagen": "imagen.png",
            "departamento_correspondiente": "IT",
            "fecha": "2024-06-25",
            "estado": "Pendiente",
            "tiempo_de_resolucion": 0,
            "usuarios_adheridos": [],
            "fecha_inicio_proceso": None
        })
        self.repositorio.guardar_reclamo(reclamo)

        # Cambiar estado a 'En Proceso'
        self.gestor_reclamos.cambiar_estado_de_reclamo(reclamo.id, "En Proceso", p_tiempo_resolucion=5)
        reclamo_actualizado = self.repositorio.leer_reclamo(reclamo.id)
        self.assertEqual(reclamo_actualizado.estado, "En Proceso")
        self.assertEqual(reclamo_actualizado.tiempo_de_resolucion, 5)
        self.assertIsNotNone(reclamo_actualizado.fecha_inicio_proceso)

        # Simular paso del tiempo
        reclamo_actualizado.set_fecha_inicio_proceso(datetime.datetime.now() - datetime.timedelta(days=3))

        # Cambiar estado a 'Resuelto'
        self.gestor_reclamos.cambiar_estado_de_reclamo(reclamo.id, "Resuelto")
        reclamo_actualizado = self.repositorio.leer_reclamo(reclamo.id)
        self.assertEqual(reclamo_actualizado.estado, "Resuelto")
        self.assertEqual(reclamo_actualizado.tiempo_de_resolucion, 3)

if __name__ == '__main__':
    unittest.main()
