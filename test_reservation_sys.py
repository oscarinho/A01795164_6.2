import unittest
import os
import json
from reservation_sys import Hotel, Customer, Reservation


class TestHotel(unittest.TestCase):
    """Pruebas unitarias para la clase Hotel."""

    def setUp(self):
        self.hotel = Hotel("H1", "Grand Hotel", "New York", 10)

    def test_to_dict(self):
        self.assertEqual(self.hotel.to_dict(), {
            "hotel_id": "H1",
            "name": "Grand Hotel",
            "location": "New York",
            "rooms_available": 10
        })

    def test_save_and_load_hotels(self):
        hotels = [self.hotel]
        Hotel.save_hotels(hotels, "test_hotels.json")
        loaded_hotels = Hotel.load_hotels("test_hotels.json")
        self.assertEqual(len(loaded_hotels), 1)
        self.assertEqual(loaded_hotels[0].name, "Grand Hotel")
        os.remove("test_hotels.json")

    def test_find_hotel(self):
        hotels = [self.hotel]
        found_hotel = Hotel.find_hotel("H1", hotels)
        self.assertIsNotNone(found_hotel)
        self.assertEqual(found_hotel.name, "Grand Hotel")

    def test_delete_hotel(self):
        hotels = [self.hotel]
        hotels = Hotel.delete_hotel("H1", hotels)
        self.assertEqual(len(hotels), 0)

    def test_modify_hotel(self):
        self.hotel.modify_hotel(name="Updated Hotel", location="Paris", rooms_available=5)
        self.assertEqual(self.hotel.name, "Updated Hotel")
        self.assertEqual(self.hotel.location, "Paris")
        self.assertEqual(self.hotel.rooms_available, 5)


class TestCustomer(unittest.TestCase):
    """Pruebas unitarias para la clase Customer."""

    def setUp(self):
        self.customer = Customer("C1", "Alice", "alice@example.com")

    def test_to_dict(self):
        self.assertEqual(self.customer.to_dict(), {
            "customer_id": "C1",
            "name": "Alice",
            "email": "alice@example.com"
        })

    def test_find_customer(self):
        customers = [self.customer]
        found_customer = Customer.find_customer("C1", customers)
        self.assertIsNotNone(found_customer)
        self.assertEqual(found_customer.name, "Alice")

    def test_delete_customer(self):
        customers = [self.customer]
        customers = Customer.delete_customer("C1", customers)
        self.assertEqual(len(customers), 0)


class TestReservation(unittest.TestCase):
    """Pruebas unitarias para la clase Reservation."""

    def setUp(self):
        self.reservation = Reservation("R1", "C1", "H1")

    def test_to_dict(self):
        self.assertEqual(self.reservation.to_dict(), {
            "reservation_id": "R1",
            "customer_id": "C1",
            "hotel_id": "H1"
        })

    def test_save_and_load_reservations(self):
        reservations = [self.reservation]
        Reservation.save_reservations(reservations, "test_reservations.json")
        loaded_reservations = Reservation.load_reservations("test_reservations.json")
        self.assertEqual(len(loaded_reservations), 1)
        self.assertEqual(loaded_reservations[0].customer_id, "C1")
        os.remove("test_reservations.json")

    def test_cancel_reservation(self):
        reservations = [self.reservation]
        hotels = [Hotel("H1", "Grand Hotel", "New York", 10)]
        updated_reservations = Reservation.cancel_reservation("R1", reservations, hotels)
        self.assertEqual(len(updated_reservations), 0)


class TestErrorHandling(unittest.TestCase):
    """Pruebas para manejo de errores en archivos JSON."""

    def test_load_invalid_hotels(self):
        with open("invalid_hotels.json", "w", encoding="utf-8") as file:
            file.write("{invalid json}")
        hotels = Hotel.load_hotels("invalid_hotels.json")
        self.assertEqual(hotels, [])
        os.remove("invalid_hotels.json")

    def test_load_invalid_customers(self):
        with open("invalid_customers.json", "w", encoding="utf-8") as file:
            file.write("{invalid json}")
        customers = Customer.load_customers("invalid_customers.json")
        self.assertEqual(customers, [])
        os.remove("invalid_customers.json")

    def test_load_invalid_reservations(self):
        with open("invalid_reservations.json", "w", encoding="utf-8") as file:
            file.write("{invalid json}")
        reservations = Reservation.load_reservations("invalid_reservations.json")
        self.assertEqual(reservations, [])
        os.remove("invalid_reservations.json")

class TestAdditionalScenarios(unittest.TestCase):
    """Pruebas adicionales para mejorar la cobertura al 85%."""

    def test_load_empty_hotels(self):
        """Prueba cuando el archivo de hoteles está vacío."""
        with open("empty_hotels.json", "w", encoding="utf-8") as file:
            file.write("[]")  # Escribir una lista vacía
        hotels = Hotel.load_hotels("empty_hotels.json")
        self.assertEqual(hotels, [])
        os.remove("empty_hotels.json")

    def test_load_empty_customers(self):
        """Prueba cuando el archivo de clientes está vacío."""
        with open("empty_customers.json", "w", encoding="utf-8") as file:
            file.write("[]")
        customers = Customer.load_customers("empty_customers.json")
        self.assertEqual(customers, [])
        os.remove("empty_customers.json")

    def test_cancel_reservation_no_match(self):
        """Prueba al intentar cancelar una reserva inexistente."""
        reservations = [
            Reservation("R1", "C1", "H1"),
            Reservation("R2", "C2", "H2")
        ]
        hotels = [
            Hotel("H1", "Grand Hotel", "New York", 10),
            Hotel("H2", "Budget Inn", "Los Angeles", 5)
        ]
        updated_reservations = Reservation.cancel_reservation("R3", reservations, hotels)
        self.assertEqual(len(updated_reservations), 2)  # No se elimina ninguna reserva
    
    def test_find_non_existent_hotel(self):
        """Prueba buscar un hotel que no existe."""
        hotels = [Hotel("H1", "Grand Hotel", "New York", 10)]
        found_hotel = Hotel.find_hotel("H99", hotels)
        self.assertIsNone(found_hotel)

    def test_find_non_existent_customer(self):
        """Prueba buscar un cliente que no existe."""
        customers = [Customer("C1", "Alice", "alice@example.com")]
        found_customer = Customer.find_customer("C99", customers)
        self.assertIsNone(found_customer)

    def test_save_empty_reservations(self):
        """Prueba guardar una lista vacía de reservas."""
        empty_reservations = []
        Reservation.save_reservations(empty_reservations, "test_empty_reservations.json")
        loaded_reservations = Reservation.load_reservations("test_empty_reservations.json")
        self.assertEqual(loaded_reservations, [])
        os.remove("test_empty_reservations.json")
    def test_load_hotels_returns_empty_list(self):
        """Prueba cuando `load_hotels()` devuelve una lista vacía por archivo inexistente."""
        hotels = Hotel.load_hotels("non_existent_hotels.json")
        self.assertEqual(hotels, [])

    def test_load_customers_returns_empty_list(self):
        """Prueba cuando `load_customers()` devuelve una lista vacía por archivo inexistente."""
        customers = Customer.load_customers("non_existent_customers.json")
        self.assertEqual(customers, [])

    def test_cancel_reservation_when_no_reservations_exist(self):
        """Prueba cancelar una reserva cuando no hay reservas en la lista."""
        reservations = []
        hotels = [Hotel("H1", "Grand Hotel", "New York", 10)]
        updated_reservations = Reservation.cancel_reservation("R1", reservations, hotels)
        self.assertEqual(len(updated_reservations), 0)

    def test_save_and_load_empty_reservations(self):
        """Prueba guardar y cargar una lista vacía de reservas."""
        empty_reservations = []
        Reservation.save_reservations(empty_reservations, "test_empty_reservations.json")
        loaded_reservations = Reservation.load_reservations("test_empty_reservations.json")
        self.assertEqual(loaded_reservations, [])
        os.remove("test_empty_reservations.json")
    def test_load_hotels_empty_file(self):
        """Prueba cuando `load_hotels()` carga un archivo vacío."""
        with open("empty_hotels.json", "w", encoding="utf-8") as file:
            file.write("[]")  # Escribir lista vacía
        hotels = Hotel.load_hotels("empty_hotels.json")
        self.assertEqual(hotels, [])
        os.remove("empty_hotels.json")

    def test_load_customers_empty_file(self):
        """Prueba cuando `load_customers()` carga un archivo vacío."""
        with open("empty_customers.json", "w", encoding="utf-8") as file:
            file.write("[]")
        customers = Customer.load_customers("empty_customers.json")
        self.assertEqual(customers, [])
        os.remove("empty_customers.json")

    def test_cancel_reservation_no_match(self):
        """Prueba al intentar cancelar una reserva que no existe."""
        reservations = [Reservation("R1", "C1", "H1")]
        hotels = [Hotel("H1", "Grand Hotel", "New York", 10)]
        updated_reservations = Reservation.cancel_reservation("R99", reservations, hotels)
        self.assertEqual(len(updated_reservations), 1)  # No se elimina ninguna reserva

    def test_save_and_load_empty_reservations(self):
        """Prueba guardar y cargar una lista vacía de reservas."""
        empty_reservations = []
        Reservation.save_reservations(empty_reservations, "test_empty_reservations.json")
        loaded_reservations = Reservation.load_reservations("test_empty_reservations.json")
        self.assertEqual(loaded_reservations, [])
        os.remove("test_empty_reservations.json")

    def test_load_hotels_corrupt_file(self):
        """Prueba cuando `load_hotels()` intenta cargar un archivo JSON corrupto."""
        with open("corrupt_hotels.json", "w", encoding="utf-8") as file:
            file.write("{invalid json}")  # JSON mal formado
        hotels = Hotel.load_hotels("corrupt_hotels.json")
        self.assertEqual(hotels, [])  # Debe manejar el error y devolver una lista vacía
        os.remove("corrupt_hotels.json")

    def test_load_customers_corrupt_file(self):
        """Prueba cuando `load_customers()` intenta cargar un archivo JSON corrupto."""
        with open("corrupt_customers.json", "w", encoding="utf-8") as file:
            file.write("{invalid json}")  # JSON mal formado
        customers = Customer.load_customers("corrupt_customers.json")
        self.assertEqual(customers, [])
        os.remove("corrupt_customers.json")

    def test_cancel_reservation_no_effect(self):
        """Prueba que `cancel_reservation()` no elimina nada si la reserva no existe."""
        reservations = [Reservation("R1", "C1", "H1")]
        hotels = [Hotel("H1", "Grand Hotel", "New York", 10)]
        updated_reservations = Reservation.cancel_reservation("R99", reservations, hotels)
        self.assertEqual(len(updated_reservations), 1)  # La lista debe seguir igual

    def test_save_reservations_with_empty_list(self):
        """Prueba guardar y cargar una lista vacía de reservas."""
        Reservation.save_reservations([], "test_empty_reservations.json")
        loaded_reservations = Reservation.load_reservations("test_empty_reservations.json")
        self.assertEqual(loaded_reservations, [])
        os.remove("test_empty_reservations.json")
    def test_load_hotels_with_wrong_data(self):
        """Prueba cuando `load_hotels()` carga un archivo con datos incorrectos."""
        with open("wrong_hotels.json", "w", encoding="utf-8") as file:
            json.dump({"hotel_id": "H1", "name": "Bad Data"}, file)  # Estructura incorrecta
        hotels = Hotel.load_hotels("wrong_hotels.json")
        self.assertEqual(hotels, [])  # Debe manejar el error y devolver lista vacía
        os.remove("wrong_hotels.json")

    def test_load_customers_with_wrong_data(self):
        """Prueba cuando `load_customers()` carga un archivo con datos incorrectos."""
        with open("wrong_customers.json", "w", encoding="utf-8") as file:
            json.dump({"customer_id": "C1", "name": "Bad Data"}, file)  # Estructura incorrecta
        customers = Customer.load_customers("wrong_customers.json")
        self.assertEqual(customers, [])
        os.remove("wrong_customers.json")

    def test_cancel_reservation_empty_list(self):
        """Prueba que `cancel_reservation()` no falle cuando no hay reservas."""
        reservations = []  # Lista vacía
        hotels = [Hotel("H1", "Grand Hotel", "New York", 10)]
        updated_reservations = Reservation.cancel_reservation("R1", reservations, hotels)
        self.assertEqual(len(updated_reservations), 0)  # Debe seguir vacío

    def test_save_reservations_empty_file(self):
        """Prueba que `save_reservations()` pueda manejar archivos vacíos correctamente."""
        with open("empty_reservations.json", "w", encoding="utf-8") as file:
            file.write("")  # Archivo vacío
        loaded_reservations = Reservation.load_reservations("empty_reservations.json")
        self.assertEqual(loaded_reservations, [])  # Debe devolver lista vacía
        os.remove("empty_reservations.json")


if __name__ == '__main__':
    unittest.main()
