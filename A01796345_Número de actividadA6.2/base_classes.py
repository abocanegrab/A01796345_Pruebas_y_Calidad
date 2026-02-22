"""Clases abstractas base para el sistema de reservaciones."""
import json
import os
from abc import ABC, abstractmethod


class PersistenceManager(ABC):
    """Abstraccion para persistencia en archivos JSON."""

    @abstractmethod
    def _get_filepath(self):
        """Retorna la ruta del archivo de persistencia."""

    def load_data(self):
        """Carga datos desde el archivo JSON."""
        filepath = self._get_filepath()
        if not os.path.exists(filepath):
            return []
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data

    def save_data(self, data):
        """Guarda datos en el archivo JSON."""
        filepath = self._get_filepath()
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


class EntityManager(ABC):
    """Abstraccion para operaciones CRUD de entidades."""

    @abstractmethod
    def create(self, **kwargs):
        """Crea una nueva entidad."""

    @abstractmethod
    def delete(self, entity_id):
        """Elimina una entidad por su id."""

    @abstractmethod
    def display(self, entity_id=None):
        """Muestra informacion de entidades."""

    @abstractmethod
    def modify(self, entity_id, **kwargs):
        """Modifica una entidad existente."""
