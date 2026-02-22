"""Modulo de la clase Reservation (version inicial)."""
import json
from hotel import Hotel
from base_classes import PersistenceManager


class Reservation(PersistenceManager):
    """Gestiona reservaciones guardandolas dentro del hotel."""

    DATA_FILE = 'data/hotels.json'

    def _get_filepath(self):
        return self.DATA_FILE

    def create_reservation(self, hotel_id, customer_id, check_in, check_out):
        """Crea una reservacion guardandola dentro del registro del hotel."""
        hotels = self.load_data()

        for i, h in enumerate(hotels):
            if h['hotel_id'] == hotel_id:
                if 'reservations' not in h:
                    hotels[i]['reservations'] = []
                r = {
                    'customer_id': customer_id,
                    'check_in': check_in,
                    'check_out': check_out
                }
                hotels[i]['reservations'].append(r)
                hotels[i]['reserved_rooms'] = h.get('reserved_rooms', 0) + 1
                self.save_data(hotels)
                return r

        raise ValueError(f"Hotel con id {hotel_id} no encontrado")

    def cancel_reservation(self, hotel_id, customer_id):
        """Cancela una reservacion del hotel."""
        hotels = self.load_data()

        for i, h in enumerate(hotels):
            if h['hotel_id'] == hotel_id:
                reservations = h.get('reservations', [])
                for j, r in enumerate(reservations):
                    if r['customer_id'] == customer_id:
                        hotels[i]['reservations'].pop(j)
                        hotels[i]['reserved_rooms'] = max(0, h.get('reserved_rooms', 0) - 1)
                        self.save_data(hotels)
                        return True
                raise ValueError("Reservacion no encontrada")

        raise ValueError(f"Hotel con id {hotel_id} no encontrado")
