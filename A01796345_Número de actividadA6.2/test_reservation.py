"""Tests para la clase Reservation."""
import os
import json
import unittest
from reservation import Reservation
from hotel import Hotel
from customer import Customer


class TestReservation(unittest.TestCase):
    """Pruebas unitarias para Reservation."""

    def setUp(self):
        """Configuracion inicial para cada test."""
        self.reservation = Reservation()
        self.hotel = Hotel()
        self.customer = Customer()
        self.files = [
            self.reservation.DATA_FILE,
            self.hotel.DATA_FILE,
            self.customer.DATA_FILE
        ]
        for f in self.files:
            if os.path.exists(f):
                os.remove(f)
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=5
        )
        self.customer.create(
            customer_id='C001', name='Juan Perez',
            email='juan@email.com'
        )

    def tearDown(self):
        """Limpieza despues de cada test."""
        for f in self.files:
            if os.path.exists(f):
                os.remove(f)

    def test_create_reservation(self):
        """Test crear una reservacion exitosamente."""
        result = self.reservation.create_reservation(
            'R001', 'C001', 'H001', '2026-03-01', '2026-03-05'
        )
        self.assertEqual(result['reservation_id'], 'R001')
        self.assertEqual(result['customer_id'], 'C001')
        self.assertEqual(result['hotel_id'], 'H001')

    def test_create_reservation_updates_hotel(self):
        """Test que crear reservacion incrementa reserved_rooms."""
        self.reservation.create_reservation(
            'R001', 'C001', 'H001', '2026-03-01', '2026-03-05'
        )
        hotel = self.hotel.display('H001')
        self.assertEqual(hotel['reserved_rooms'], 1)

    def test_create_reservation_duplicate(self):
        """Test crear reservacion duplicada lanza error."""
        self.reservation.create_reservation(
            'R001', 'C001', 'H001', '2026-03-01', '2026-03-05'
        )
        with self.assertRaises(ValueError):
            self.reservation.create_reservation(
                'R001', 'C001', 'H001', '2026-04-01', '2026-04-05'
            )

    def test_create_reservation_missing_fields(self):
        """Test crear reservacion sin campos requeridos."""
        with self.assertRaises(ValueError):
            self.reservation.create_reservation(
                None, 'C001', 'H001', '2026-03-01', '2026-03-05'
            )

    def test_create_reservation_hotel_not_found(self):
        """Test crear reservacion con hotel inexistente."""
        with self.assertRaises(ValueError):
            self.reservation.create_reservation(
                'R001', 'C001', 'H999', '2026-03-01', '2026-03-05'
            )

    def test_create_reservation_customer_not_found(self):
        """Test crear reservacion con cliente inexistente."""
        with self.assertRaises(ValueError):
            self.reservation.create_reservation(
                'R001', 'C999', 'H001', '2026-03-01', '2026-03-05'
            )

    def test_cancel_reservation(self):
        """Test cancelar una reservacion exitosamente."""
        self.reservation.create_reservation(
            'R001', 'C001', 'H001', '2026-03-01', '2026-03-05'
        )
        result = self.reservation.cancel_reservation('R001')
        self.assertTrue(result)
        reservations = self.reservation.load_data()
        self.assertEqual(len(reservations), 0)

    def test_cancel_reservation_updates_hotel(self):
        """Test que cancelar reservacion decrementa reserved_rooms."""
        self.reservation.create_reservation(
            'R001', 'C001', 'H001', '2026-03-01', '2026-03-05'
        )
        self.reservation.cancel_reservation('R001')
        hotel = self.hotel.display('H001')
        self.assertEqual(hotel['reserved_rooms'], 0)

    def test_cancel_reservation_not_found(self):
        """Test cancelar reservacion que no existe."""
        with self.assertRaises(ValueError):
            self.reservation.cancel_reservation('R999')

    def test_create_multiple_reservations(self):
        """Test crear multiples reservaciones."""
        self.customer.create(
            customer_id='C002', name='Maria Lopez',
            email='maria@email.com'
        )
        self.reservation.create_reservation(
            'R001', 'C001', 'H001', '2026-03-01', '2026-03-05'
        )
        self.reservation.create_reservation(
            'R002', 'C002', 'H001', '2026-03-01', '2026-03-05'
        )
        reservations = self.reservation.load_data()
        self.assertEqual(len(reservations), 2)

    def test_create_reservation_hotel_full(self):
        """Test crear reservacion cuando hotel esta lleno."""
        self.hotel.create(
            hotel_id='H002', name='Hotel Chico',
            location='GDL', rooms=1
        )
        self.reservation.create_reservation(
            'R001', 'C001', 'H002', '2026-03-01', '2026-03-05'
        )
        with self.assertRaises(ValueError):
            self.reservation.create_reservation(
                'R002', 'C001', 'H002', '2026-04-01', '2026-04-05'
            )

    def test_load_corrupted_file(self):
        """Test cargar archivo JSON corrupto."""
        os.makedirs('data', exist_ok=True)
        with open(self.reservation.DATA_FILE, 'w', encoding='utf-8') as f:
            f.write('not valid json')
        with self.assertRaises(json.JSONDecodeError):
            self.reservation.load_data()


if __name__ == '__main__':
    unittest.main()
