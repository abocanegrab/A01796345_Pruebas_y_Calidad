"""Clases abstractas base para el sistema de reservaciones."""
import json
import os
from abc import ABC, abstractmethod


class PersistenceManager(ABC):
    """Abstraccion para persistencia en archivos JSON."""

    @abstractmethod
    def _get_filepath(self):
        pass

    def load_data(self):
        filepath = self._get_filepath()
        if not os.path.exists(filepath):
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            d = json.load(f)
            return d

    def save_data(self, data):
        filepath = self._get_filepath()
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath,'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


class EntityManager(ABC):
    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass

    @abstractmethod
    def display(self, entity_id=None):
        pass

    @abstractmethod
    def modify(self, entity_id, **kwargs):
        pass
