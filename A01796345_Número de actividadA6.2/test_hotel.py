"""Tests para la clase Hotel."""
import os
import json
import unittest
from hotel import Hotel


class TestHotel(unittest.TestCase):
    """Pruebas unitarias para Hotel."""

    def setUp(self):
        """Configuracion inicial para cada test."""
        self.hotel = Hotel()
        self.test_file = self.hotel.DATA_FILE
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Limpieza despues de cada test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_create_hotel(self):
        """Test crear un hotel exitosamente."""
        result = self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=50
        )
        self.assertEqual(result['hotel_id'], 'H001')
        self.assertEqual(result['name'], 'Hotel Plaza')
        self.assertEqual(result['rooms'], 50)
        self.assertEqual(result['reserved_rooms'], 0)

    def test_create_hotel_duplicate(self):
        """Test crear hotel duplicado lanza error."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=50
        )
        with self.assertRaises(ValueError):
            self.hotel.create(
                hotel_id='H001', name='Otro Hotel',
                location='GDL', rooms=30
            )

    def test_create_hotel_missing_fields(self):
        """Test crear hotel sin campos requeridos."""
        with self.assertRaises(ValueError):
            self.hotel.create(hotel_id='H001', name='Hotel Plaza')

    def test_create_hotel_invalid_rooms(self):
        """Test crear hotel con rooms invalido."""
        with self.assertRaises(ValueError):
            self.hotel.create(
                hotel_id='H001', name='Hotel Plaza',
                location='CDMX', rooms=-5
            )
        with self.assertRaises(ValueError):
            self.hotel.create(
                hotel_id='H002', name='Hotel Plaza',
                location='CDMX', rooms='abc'
            )

    def test_delete_hotel(self):
        """Test eliminar un hotel."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=50
        )
        result = self.hotel.delete('H001')
        self.assertTrue(result)
        hotels = self.hotel.load_data()
        self.assertEqual(len(hotels), 0)

    def test_delete_hotel_not_found(self):
        """Test eliminar hotel que no existe."""
        with self.assertRaises(ValueError):
            self.hotel.delete('H999')

    def test_display_all_hotels(self):
        """Test mostrar todos los hoteles."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=50
        )
        self.hotel.create(
            hotel_id='H002', name='Hotel Sol',
            location='CUN', rooms=100
        )
        result = self.hotel.display()
        self.assertEqual(len(result), 2)

    def test_display_single_hotel(self):
        """Test mostrar un hotel especifico."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=50
        )
        result = self.hotel.display('H001')
        self.assertEqual(result['name'], 'Hotel Plaza')

    def test_display_hotel_not_found(self):
        """Test mostrar hotel que no existe."""
        with self.assertRaises(ValueError):
            self.hotel.display('H999')

    def test_display_empty(self):
        """Test mostrar cuando no hay hoteles."""
        result = self.hotel.display()
        self.assertEqual(result, [])

    def test_modify_hotel(self):
        """Test modificar un hotel."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=50
        )
        result = self.hotel.modify('H001', name='Hotel Grand Plaza')
        self.assertEqual(result['name'], 'Hotel Grand Plaza')

    def test_modify_hotel_location(self):
        """Test modificar ubicacion de hotel."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=50
        )
        result = self.hotel.modify('H001', location='MTY')
        self.assertEqual(result['location'], 'MTY')

    def test_modify_hotel_rooms(self):
        """Test modificar numero de habitaciones."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=50
        )
        result = self.hotel.modify('H001', rooms=100)
        self.assertEqual(result['rooms'], 100)

    def test_modify_hotel_invalid_rooms(self):
        """Test modificar rooms con valor invalido."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=50
        )
        with self.assertRaises(ValueError):
            self.hotel.modify('H001', rooms=-10)

    def test_modify_hotel_not_found(self):
        """Test modificar hotel que no existe."""
        with self.assertRaises(ValueError):
            self.hotel.modify('H999', name='No existe')

    def test_reserve_room(self):
        """Test reservar una habitacion."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=2
        )
        result = self.hotel.reserve_room('H001')
        self.assertEqual(result['reserved_rooms'], 1)

    def test_reserve_room_full(self):
        """Test reservar cuando no hay habitaciones."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=1
        )
        self.hotel.reserve_room('H001')
        with self.assertRaises(ValueError):
            self.hotel.reserve_room('H001')

    def test_reserve_room_not_found(self):
        """Test reservar en hotel que no existe."""
        with self.assertRaises(ValueError):
            self.hotel.reserve_room('H999')

    def test_cancel_reservation(self):
        """Test cancelar una reservacion."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=5
        )
        self.hotel.reserve_room('H001')
        result = self.hotel.cancel_reservation('H001')
        self.assertEqual(result['reserved_rooms'], 0)

    def test_cancel_reservation_none(self):
        """Test cancelar cuando no hay reservaciones."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=5
        )
        with self.assertRaises(ValueError):
            self.hotel.cancel_reservation('H001')

    def test_cancel_reservation_not_found(self):
        """Test cancelar en hotel que no existe."""
        with self.assertRaises(ValueError):
            self.hotel.cancel_reservation('H999')

    def test_modify_rooms_below_reserved(self):
        """Test reducir rooms debajo de las reservadas."""
        self.hotel.create(
            hotel_id='H001', name='Hotel Plaza',
            location='CDMX', rooms=5
        )
        self.hotel.reserve_room('H001')
        self.hotel.reserve_room('H001')
        with self.assertRaises(ValueError):
            self.hotel.modify('H001', rooms=1)

    def test_load_corrupted_file(self):
        """Test cargar archivo JSON corrupto."""
        os.makedirs('data', exist_ok=True)
        with open(self.test_file, 'w') as f:
            f.write('not valid json{{{')
        with self.assertRaises(json.JSONDecodeError):
            self.hotel.load_data()


if __name__ == '__main__':
    unittest.main()
