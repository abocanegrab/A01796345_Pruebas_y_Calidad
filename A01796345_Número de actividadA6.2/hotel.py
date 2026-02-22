"""Modulo de la clase Hotel."""
from base_classes import EntityManager, PersistenceManager


class Hotel(EntityManager, PersistenceManager):
    """Gestiona hoteles con persistencia en JSON."""

    DATA_FILE = 'data/hotels.json'

    def _get_filepath(self):
        return self.DATA_FILE

    def create(self, **kwargs):
        """Crea un nuevo hotel."""
        hotel_id = kwargs.get('hotel_id')
        name = kwargs.get('name')
        location = kwargs.get('location')
        rooms = kwargs.get('rooms')

        if not all([hotel_id, name, location, rooms]):
            raise ValueError("Todos los campos son requeridos: hotel_id, name, location, rooms")

        if not isinstance(rooms, int) or rooms <= 0:
            raise ValueError("rooms debe ser un entero positivo")

        hotels = self.load_data()
        for h in hotels:
            if h['hotel_id'] == hotel_id:
                raise ValueError(f"Hotel con id {hotel_id} ya existe")

        hotel = {
            'hotel_id': hotel_id,
            'name': name,
            'location': location,
            'rooms': rooms,
            'reserved_rooms': 0
        }
        hotels.append(hotel)
        self.save_data(hotels)
        return hotel

    def delete(self, entity_id):
        """Elimina un hotel por su id."""
        hotels = self.load_data()
        original_len = len(hotels)
        hotels = [h for h in hotels if h['hotel_id'] != entity_id]

        if len(hotels) == original_len:
            raise ValueError(f"Hotel con id {entity_id} no encontrado")

        self.save_data(hotels)
        return True

    def display(self, entity_id=None):
        """Muestra informacion de hoteles."""
        hotels = self.load_data()

        if entity_id is not None:
            for h in hotels:
                if h['hotel_id'] == entity_id:
                    return h
            raise ValueError(f"Hotel con id {entity_id} no encontrado")

        return hotels

    def modify(self, entity_id, **kwargs):
        """Modifica un hotel existente."""
        hotels = self.load_data()

        for i, h in enumerate(hotels):
            if h['hotel_id'] == entity_id:
                if 'name' in kwargs:
                    hotels[i]['name'] = kwargs['name']
                if 'location' in kwargs:
                    hotels[i]['location'] = kwargs['location']
                if 'rooms' in kwargs:
                    new_rooms = kwargs['rooms']
                    if not isinstance(new_rooms, int) or new_rooms <= 0:
                        raise ValueError("rooms debe ser un entero positivo")
                    if new_rooms < hotels[i]['reserved_rooms']:
                        raise ValueError("No se puede reducir rooms por debajo de las reservadas")
                    hotels[i]['rooms'] = new_rooms
                self.save_data(hotels)
                return hotels[i]

        raise ValueError(f"Hotel con id {entity_id} no encontrado")

    def reserve_room(self, hotel_id):
        """Reserva una habitacion en el hotel."""
        hotels = self.load_data()

        for i, h in enumerate(hotels):
            if h['hotel_id'] == hotel_id:
                if h['reserved_rooms'] >= h['rooms']:
                    raise ValueError("No hay habitaciones disponibles")
                hotels[i]['reserved_rooms'] = h['reserved_rooms'] + 1
                self.save_data(hotels)
                return hotels[i]

        raise ValueError(f"Hotel con id {hotel_id} no encontrado")

    def cancel_reservation(self, hotel_id):
        """Cancela una reservacion en el hotel."""
        hotels = self.load_data()

        for i, h in enumerate(hotels):
            if h['hotel_id'] == hotel_id:
                if h['reserved_rooms'] <= 0:
                    raise ValueError("No hay reservaciones que cancelar")
                hotels[i]['reserved_rooms'] = h['reserved_rooms'] - 1
                self.save_data(hotels)
                return hotels[i]

        raise ValueError(f"Hotel con id {hotel_id} no encontrado")
