"""Tests para la clase Customer."""
import os
import json
import unittest
from customer import Customer


class TestCustomer(unittest.TestCase):
    """Pruebas unitarias para Customer."""

    def setUp(self):
        """Configuracion inicial para cada test."""
        self.customer = Customer()
        self.test_file = self.customer.DATA_FILE
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Limpieza despues de cada test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_create_customer(self):
        """Test crear un cliente exitosamente."""
        result = self.customer.create(
            customer_id='C001', name='Juan Perez',
            email='juan@email.com'
        )
        self.assertEqual(result['customer_id'], 'C001')
        self.assertEqual(result['name'], 'Juan Perez')
        self.assertEqual(result['email'], 'juan@email.com')

    def test_create_customer_duplicate(self):
        """Test crear cliente duplicado lanza error."""
        self.customer.create(
            customer_id='C001', name='Juan Perez',
            email='juan@email.com'
        )
        with self.assertRaises(ValueError):
            self.customer.create(
                customer_id='C001', name='Otro',
                email='otro@email.com'
            )

    def test_create_customer_missing_fields(self):
        """Test crear cliente sin campos requeridos."""
        with self.assertRaises(ValueError):
            self.customer.create(customer_id='C001', name='Juan Perez')

    def test_delete_customer(self):
        """Test eliminar un cliente."""
        self.customer.create(
            customer_id='C001', name='Juan Perez',
            email='juan@email.com'
        )
        result = self.customer.delete('C001')
        self.assertTrue(result)
        customers = self.customer.load_data()
        self.assertEqual(len(customers), 0)

    def test_delete_customer_not_found(self):
        """Test eliminar cliente que no existe."""
        with self.assertRaises(ValueError):
            self.customer.delete('C999')

    def test_display_all_customers(self):
        """Test mostrar todos los clientes."""
        self.customer.create(
            customer_id='C001', name='Juan Perez',
            email='juan@email.com'
        )
        self.customer.create(
            customer_id='C002', name='Maria Lopez',
            email='maria@email.com'
        )
        result = self.customer.display()
        self.assertEqual(len(result), 2)

    def test_display_single_customer(self):
        """Test mostrar un cliente especifico."""
        self.customer.create(
            customer_id='C001', name='Juan Perez',
            email='juan@email.com'
        )
        result = self.customer.display('C001')
        self.assertEqual(result['name'], 'Juan Perez')

    def test_display_customer_not_found(self):
        """Test mostrar cliente que no existe."""
        with self.assertRaises(ValueError):
            self.customer.display('C999')

    def test_display_empty(self):
        """Test mostrar cuando no hay clientes."""
        result = self.customer.display()
        self.assertEqual(result, [])

    def test_modify_customer_name(self):
        """Test modificar nombre de cliente."""
        self.customer.create(
            customer_id='C001', name='Juan Perez',
            email='juan@email.com'
        )
        result = self.customer.modify('C001', name='Juan P. Garcia')
        self.assertEqual(result['name'], 'Juan P. Garcia')

    def test_modify_customer_email(self):
        """Test modificar email de cliente."""
        self.customer.create(
            customer_id='C001', name='Juan Perez',
            email='juan@email.com'
        )
        result = self.customer.modify('C001', email='nuevo@email.com')
        self.assertEqual(result['email'], 'nuevo@email.com')

    def test_modify_customer_not_found(self):
        """Test modificar cliente que no existe."""
        with self.assertRaises(ValueError):
            self.customer.modify('C999', name='No existe')

    def test_load_corrupted_file(self):
        """Test cargar archivo JSON corrupto."""
        os.makedirs('data', exist_ok=True)
        with open(self.test_file, 'w') as f:
            f.write('corrupted data!!!')
        with self.assertRaises(json.JSONDecodeError):
            self.customer.load_data()

    def test_modify_multiple_fields(self):
        """Test modificar varios campos a la vez."""
        self.customer.create(
            customer_id='C001', name='Juan Perez',
            email='juan@email.com'
        )
        result = self.customer.modify(
            'C001', name='Pedro Lopez', email='pedro@email.com'
        )
        self.assertEqual(result['name'], 'Pedro Lopez')
        self.assertEqual(result['email'], 'pedro@email.com')


if __name__ == '__main__':
    unittest.main()
