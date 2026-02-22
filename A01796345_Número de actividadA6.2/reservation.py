"""Modulo de la clase Reservation."""
import json
from base_classes import PersistenceManager
from hotel import Hotel
from customer import Customer


class Reservation(PersistenceManager):
    """Gestiona reservaciones con persistencia en JSON."""

    DATA_FILE = 'data/reservations.json'

    def _get_filepath(self):
        return self.DATA_FILE

    def create_reservation(self, reservation_id, customer_id, hotel_id,
                           check_in, check_out):
        """Crea una nueva reservacion."""
        if not all([reservation_id, customer_id, hotel_id, check_in, check_out]):
            raise ValueError("Todos los campos son requeridos")

        hotel_mgr = Hotel()
        try:
            hotel_mgr.display(hotel_id)
        except ValueError:
            raise ValueError(f"Hotel con id {hotel_id} no existe")

        customer_mgr = Customer()
        try:
            customer_mgr.display(customer_id)
        except ValueError:
            raise ValueError(f"Cliente con id {customer_id} no existe")

        reservations = self.load_data()
        for r in reservations:
            if r['reservation_id'] == reservation_id:
                raise ValueError(f"Reservacion con id {reservation_id} ya existe")

        hotel_mgr.reserve_room(hotel_id)

        reservation = {
            'reservation_id': reservation_id,
            'customer_id': customer_id,
            'hotel_id': hotel_id,
            'check_in': check_in,
            'check_out': check_out
        }
        reservations.append(reservation)
        self.save_data(reservations)
        return reservation

    def cancel_reservation(self, reservation_id):
        """Cancela una reservacion existente."""
        reservations = self.load_data()
        reservation = None

        for r in reservations:
            if r['reservation_id'] == reservation_id:
                reservation = r
                break

        if reservation is None:
            raise ValueError(f"Reservacion con id {reservation_id} no encontrada")

        hotel_mgr = Hotel()
        try:
            hotel_mgr.cancel_reservation(reservation['hotel_id'])
        except:
            pass

        reservations = [r for r in reservations if r['reservation_id'] != reservation_id]
        self.save_data(reservations)
        return True
