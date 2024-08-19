from abc import ABC, abstractmethod
from modules.entidades import Reclamo, Usuario

# Fija la interfaz de interacción del Modelo de Dominio
class Repositorio(ABC):
    @abstractmethod
    def leer_reclamo(id: int) -> Reclamo:
        raise NotImplementedError
    
    @abstractmethod
    def guardar_reclamo(reclamo: Reclamo) -> None:
        raise NotImplementedError