"""
Módulo de Sistema de Reservas de Hoteles.

Este módulo permite gestionar hoteles, clientes y reservas con persistencia
de datos en archivos JSON.
"""

import json
import os


class Hotel:
    """Clase que representa un hotel."""

    def __init__(self, hotel_id, name, location, rooms_available):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms_available = rooms_available

    def to_dict(self):
        """Convierte los datos del hotel a un diccionario."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "rooms_available": self.rooms_available,
        }

    @staticmethod
    def save_hotels(hotels, filename="hotels.json"):
        """Guarda los datos de hoteles en un archivo JSON."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [hotel.to_dict() for hotel in hotels],
                file,
                indent=4
            )

    @staticmethod
    def load_hotels(filename="hotels.json"):
        """Carga los datos de hoteles desde un archivo
        JSON con manejo de errores."""
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError(
                        "El contenido del JSON debe ser una lista de hoteles."
                        )
                return [Hotel(**hotel) for hotel in data]
        except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
            print(f"Error al cargar hoteles desde {filename}: {e}")
            return []

    @staticmethod
    def find_hotel(hotel_id, hotels):
        """Busca un hotel por su ID."""
        return next(
            (hotel for hotel in hotels if hotel.hotel_id == hotel_id), None
        )

    @staticmethod
    def delete_hotel(hotel_id, hotels):
        """Elimina un hotel de la lista."""
        updated_hotels = [hotel for hotel in hotels if hotel.hotel_id != hotel_id]
        Hotel.save_hotels(updated_hotels)
        return updated_hotels

    def modify_hotel(self, name=None, location=None, rooms_available=None):
        """Modifica los atributos de un hotel."""
        if name:
            self.name = name
        if location:
            self.location = location
        if rooms_available is not None:
            self.rooms_available = rooms_available


class Customer:
    """Clase que representa un cliente."""

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """Convierte los datos del cliente a un diccionario."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }

    @staticmethod
    def save_customers(customers, filename="customers.json"):
        """Guarda los datos de clientes en un archivo JSON."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [customer.to_dict() for customer in customers],
                file,
                indent=4
            )

    @staticmethod
    def load_customers(filename="customers.json"):
        """Carga los datos de clientes desde un
        archivo JSON con manejo de errores."""
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError(
                        "El contenido del JSON debe ser una lista de clientes."
                        )
                return [Customer(**customer) for customer in data]
        except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
            print(f"Error al cargar clientes desde {filename}: {e}")
            return []

    @staticmethod
    def find_customer(customer_id, customers):
        """Busca un cliente por su ID."""
        return next(
            (customer for customer in customers if customer.customer_id == customer_id), None
        )

    @staticmethod
    def delete_customer(customer_id, customers):
        """Elimina un cliente de la lista."""
        updated_customers = [c for c in customers if c.customer_id != customer_id]
        Customer.save_customers(updated_customers)
        return updated_customers


class Reservation:
    """Clase que representa una reserva."""

    def __init__(self, reservation_id, customer_id, hotel_id):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Convierte los datos de la reserva a un diccionario."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
        }

    @staticmethod
    def save_reservations(reservations, filename="reservations.json"):
        """Guarda los datos de reservas en un archivo JSON."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [r.to_dict() for r in reservations],
                file,
                indent=4
            )

    @staticmethod
    def load_reservations(filename="reservations.json"):
        """Carga los datos de reservas desde
        un archivo JSON con manejo de errores."""
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError(
                        "El contenido del JSON debe ser una lista de reservas."
                        )
                return [Reservation(**reservation) for reservation in data]
        except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
            print(f"Error al cargar reservas desde {filename}: {e}")
            return []

    @staticmethod
    def cancel_reservation(reservation_id, reservations, hotels):
        """Cancela una reserva y
        devuelve la habitación al hotel."""
        reservation = next((r for r in reservations if r.reservation_id == reservation_id), None)
        if reservation:
            hotel = next((h for h in hotels if h.hotel_id == reservation.hotel_id), None)
            if hotel:
                hotel.rooms_available += 1  # Aumentar la disponibilidad
                updated_reservations = [r for r in reservations if r.reservation_id != reservation_id]
                Hotel.save_hotels(hotels)
                Reservation.save_reservations(updated_reservations)
                return updated_reservations
        return reservations


# Ejemplo de uso
def main():
    """Función principal para demostrar funcionalidad."""
    hotels = Hotel.load_hotels()
    customers = Customer.load_customers()
    reservations = Reservation.load_reservations()

    # Crear hotel
    new_hotel = Hotel("H1", "Grand Hotel", "New York", 10)
    hotels.append(new_hotel)
    Hotel.save_hotels(hotels)

    # Crear cliente
    new_customer = Customer("C1", "Alice", "alice@example.com")
    customers.append(new_customer)
    Customer.save_customers(customers)

    # Crear reserva
    new_reservation = Reservation("R1", "C1", "H1")
    reservations.append(new_reservation)
    Reservation.save_reservations(reservations)

    print("Reserva creada exitosamente.")

    # Cancelar reserva
    reservations = Reservation.cancel_reservation("R1", reservations, hotels)
    print("Reserva cancelada.")


if __name__ == "__main__":
    main()
