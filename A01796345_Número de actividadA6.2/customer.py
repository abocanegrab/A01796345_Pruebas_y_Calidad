"""Modulo de la clase Customer."""
from base_classes import EntityManager, PersistenceManager


class Customer(EntityManager, PersistenceManager):
    """Gestiona clientes con persistencia en JSON."""

    DATA_FILE = 'data/customers.json'

    def _get_filepath(self):
        return self.DATA_FILE

    def create(self, **kwargs):
        """Crea un nuevo cliente."""
        customer_id = kwargs.get('customer_id')
        name = kwargs.get('name')
        email = kwargs.get('email')

        if not all([customer_id, name, email]):
            raise ValueError("Todos los campos son requeridos: customer_id, name, email")

        customers = self.load_data()
        for c in customers:
            if c['customer_id'] == customer_id:
                raise ValueError(f"Cliente con id {customer_id} ya existe")

        customer = {
            'customer_id': customer_id,
            'name': name,
            'email': email
        }
        customers.append(customer)
        self.save_data(customers)
        return customer

    def delete(self, entity_id):
        """Elimina un cliente por su id."""
        customers = self.load_data()
        original_len = len(customers)
        customers = [c for c in customers if c['customer_id'] != entity_id]

        if len(customers) == original_len:
            raise ValueError(f"Cliente con id {entity_id} no encontrado")

        self.save_data(customers)
        return True

    def display(self, entity_id=None):
        """Muestra informacion de clientes."""
        customers = self.load_data()

        if entity_id is not None:
            for c in customers:
                if c['customer_id'] == entity_id:
                    return c
            raise ValueError(f"Cliente con id {entity_id} no encontrado")

        return customers

    def modify(self, entity_id, **kwargs):
        """Modifica un cliente existente."""
        customers = self.load_data()

        for i, c in enumerate(customers):
            if c['customer_id'] == entity_id:
                if 'name' in kwargs:
                    customers[i]['name'] = kwargs['name']
                if 'email' in kwargs:
                    customers[i]['email'] = kwargs['email']
                self.save_data(customers)
                return customers[i]

        raise ValueError(f"Cliente con id {entity_id} no encontrado")
