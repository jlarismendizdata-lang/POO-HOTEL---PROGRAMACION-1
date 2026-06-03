"""
Sistema de gestión hotelera.
Arquitectura orientada a objetos con principios SOLID.
"""

from abc import ABC, abstractmethod
from datetime import date
from itertools import count


class EstadoHabitacion:
    DISPONIBLE = "disponible"
    OCUPADA    = "ocupada"


class EstadoReserva:
    ACTIVA    = "activa"
    CANCELADA = "cancelada"


class EstadoPago:
    PENDIENTE = "pendiente"
    PAGADA    = "pagada"


class Persona(ABC):
    """Entidad base para cualquier persona registrada en el sistema."""

    def __init__(
        self,
        nombre: str,
        cedula: str,
        contacto: str,
        fecha_nacimiento: date,
        direccion: str,
        rol: str,
    ) -> None:
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if not cedula.strip():
            raise ValueError("La cédula no puede estar vacía.")

        self._nombre           = nombre
        self._cedula           = cedula
        self._contacto         = contacto
        self._fecha_nacimiento = fecha_nacimiento
        self._direccion        = direccion
        self._rol              = rol

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def cedula(self) -> str:
        return self._cedula

    @property
    def contacto(self) -> str:
        return self._contacto

    @property
    def fecha_nacimiento(self) -> date:
        return self._fecha_nacimiento

    @property
    def direccion(self) -> str:
        return self._direccion

    @property
    def rol(self) -> str:
        return self._rol

    def calcular_edad(self) -> int:
        hoy  = date.today()
        edad = hoy.year - self._fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self._fecha_nacimiento.month, self._fecha_nacimiento.day):
            edad -= 1
        return edad

    @abstractmethod
    def consultar_informacion(self) -> None:
        pass


class Huesped(Persona):
    """Huésped que realiza reservas en el hotel."""

    def __init__(
        self,
        nombre: str,
        cedula: str,
        contacto: str,
        fecha_nacimiento: date,
        direccion: str,
        nacionalidad: str,
        idioma: str,
    ) -> None:
        super().__init__(nombre, cedula, contacto, fecha_nacimiento, direccion, "Huésped")
        self._nacionalidad = nacionalidad
        self._idioma       = idioma

    @property
    def nacionalidad(self) -> str:
        return self._nacionalidad

    @property
    def idioma(self) -> str:
        return self._idioma

    def consultar_informacion(self) -> None:
        print(
            f"[HUÉSPED]\n"
            f"  Nombre        : {self.nombre}\n"
            f"  Cédula        : {self.cedula}\n"
            f"  Contacto      : {self.contacto}\n"
            f"  Edad          : {self.calcular_edad()} años\n"
            f"  Dirección     : {self.direccion}\n"
            f"  Nacionalidad  : {self.nacionalidad}\n"
            f"  Idioma        : {self.idioma}"
        )


class EmpleadoHotel(Persona):
    """Empleado responsable de gestionar reservas y servicios."""

    def __init__(
        self,
        nombre: str,
        cedula: str,
        contacto: str,
        fecha_nacimiento: date,
        direccion: str,
        cargo: str,
        idiomas: list[str],
    ) -> None:
        super().__init__(nombre, cedula, contacto, fecha_nacimiento, direccion, "Empleado")
        if not idiomas:
            raise ValueError("El empleado debe hablar al menos un idioma.")
        self._cargo   = cargo
        self._idiomas = idiomas

    @property
    def cargo(self) -> str:
        return self._cargo

    @property
    def idiomas(self) -> list[str]:
        return list(self._idiomas)  # copia defensiva para no exponer el estado interno

    def consultar_informacion(self) -> None:
        print(
            f"[EMPLEADO]\n"
            f"  Nombre   : {self.nombre}\n"
            f"  Cédula   : {self.cedula}\n"
            f"  Contacto : {self.contacto}\n"
            f"  Edad     : {self.calcular_edad()} años\n"
            f"  Cargo    : {self.cargo}\n"
            f"  Idiomas  : {', '.join(self.idiomas)}"
        )


class Habitacion(ABC):
    """Habitación base. Gestiona disponibilidad y expone atributos físicos."""

    def __init__(
        self,
        numero: int,
        precio_noche: float,
        estado: str,
        aforo_maximo: int,
        cantidad_camas: int,
        cantidad_banos: int,
        aire_acondicionado: bool,
    ) -> None:
        if precio_noche <= 0:
            raise ValueError("El precio por noche debe ser positivo.")
        if aforo_maximo <= 0:
            raise ValueError("El aforo máximo debe ser al menos 1.")

        self._numero             = numero
        self._precio_noche       = precio_noche
        self._estado             = estado
        self._aforo_maximo       = aforo_maximo
        self._cantidad_camas     = cantidad_camas
        self._cantidad_banos     = cantidad_banos
        self._aire_acondicionado = aire_acondicionado

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def precio_noche(self) -> float:
        return self._precio_noche

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def aforo_maximo(self) -> int:
        return self._aforo_maximo

    @property
    def cantidad_camas(self) -> int:
        return self._cantidad_camas

    @property
    def cantidad_banos(self) -> int:
        return self._cantidad_banos

    @property
    def aire_acondicionado(self) -> bool:
        return self._aire_acondicionado

    @property
    def esta_disponible(self) -> bool:
        return self._estado == EstadoHabitacion.DISPONIBLE

    def marcar_ocupada(self) -> None:
        self._estado = EstadoHabitacion.OCUPADA

    def marcar_disponible(self) -> None:
        self._estado = EstadoHabitacion.DISPONIBLE

    @abstractmethod
    def consultar_informacion(self) -> None:
        pass


class HabitacionIndividual(Habitacion):
    """Habitación para un único huésped."""

    def __init__(
        self,
        numero: int,
        precio_noche: float,
        estado: str,
        cantidad_camas: int,
        cantidad_banos: int,
        aire_acondicionado: bool,
        espacio_abierto: bool,
        tiene_televisor: bool,
    ) -> None:
        super().__init__(
            numero, precio_noche, estado,
            aforo_maximo=1,
            cantidad_camas=cantidad_camas,
            cantidad_banos=cantidad_banos,
            aire_acondicionado=aire_acondicionado,
        )
        self._espacio_abierto = espacio_abierto
        self._tiene_televisor = tiene_televisor

    def consultar_informacion(self) -> None:
        yn = lambda v: "Sí" if v else "No"
        print(
            f"[HABITACIÓN INDIVIDUAL #{self.numero}]\n"
            f"  Estado          : {self.estado}\n"
            f"  Camas           : {self.cantidad_camas}\n"
            f"  Baños           : {self.cantidad_banos}\n"
            f"  Aire acondic.   : {yn(self.aire_acondicionado)}\n"
            f"  Espacio abierto : {yn(self._espacio_abierto)}\n"
            f"  Televisor       : {yn(self._tiene_televisor)}\n"
            f"  Precio/noche    : ${self.precio_noche:,.0f}"
        )


class HabitacionMultiple(Habitacion):
    """Habitación para múltiples huéspedes."""

    def __init__(
        self,
        numero: int,
        precio_noche: float,
        estado: str,
        aforo_maximo: int,
        cantidad_camas: int,
        cantidad_banos: int,
        aire_acondicionado: bool,
        cantidad_televisores: int,
        cantidad_espacios_abiertos: int,
    ) -> None:
        super().__init__(
            numero, precio_noche, estado, aforo_maximo,
            cantidad_camas, cantidad_banos, aire_acondicionado,
        )
        self._cantidad_televisores       = cantidad_televisores
        self._cantidad_espacios_abiertos = cantidad_espacios_abiertos

    def consultar_informacion(self) -> None:
        yn = lambda v: "Sí" if v else "No"
        print(
            f"[HABITACIÓN MÚLTIPLE #{self.numero}]\n"
            f"  Estado            : {self.estado}\n"
            f"  Aforo máximo      : {self.aforo_maximo} personas\n"
            f"  Camas             : {self.cantidad_camas}\n"
            f"  Baños             : {self.cantidad_banos}\n"
            f"  Aire acondic.     : {yn(self.aire_acondicionado)}\n"
            f"  Televisores       : {self._cantidad_televisores}\n"
            f"  Espacios abiertos : {self._cantidad_espacios_abiertos}\n"
            f"  Precio/noche      : ${self.precio_noche:,.0f}"
        )


class Hotel(ABC):
    """Hotel base. Controla el inventario de habitaciones disponibles."""

    def __init__(
        self,
        nombre: str,
        lider: str,
        ubicacion: str,
        num_habitaciones: int,
        contacto: str,
    ) -> None:
        if num_habitaciones <= 0:
            raise ValueError("El número de habitaciones debe ser positivo.")

        self._nombre                   = nombre
        self._lider                    = lider
        self._ubicacion                = ubicacion
        self._num_habitaciones         = num_habitaciones
        self._habitaciones_disponibles = num_habitaciones
        self._contacto                 = contacto

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def lider(self) -> str:
        return self._lider

    @property
    def ubicacion(self) -> str:
        return self._ubicacion

    @property
    def num_habitaciones(self) -> int:
        return self._num_habitaciones

    @property
    def habitaciones_disponibles(self) -> int:
        return self._habitaciones_disponibles

    @property
    def contacto(self) -> str:
        return self._contacto

    def reducir_disponibilidad(self) -> None:
        if self._habitaciones_disponibles <= 0:
            raise RuntimeError(f"El hotel '{self.nombre}' no tiene habitaciones disponibles.")
        self._habitaciones_disponibles -= 1

    def aumentar_disponibilidad(self) -> None:
        if self._habitaciones_disponibles >= self._num_habitaciones:
            raise RuntimeError(f"El hotel '{self.nombre}' ya tiene todas las habitaciones libres.")
        self._habitaciones_disponibles += 1

    @abstractmethod
    def consultar_informacion(self) -> None:
        pass


class HotelUrbano(Hotel):
    """Hotel en zona urbana con transporte público y opción de alimentación."""

    def __init__(
        self,
        nombre: str,
        lider: str,
        ubicacion: str,
        num_habitaciones: int,
        contacto: str,
        acceso_transporte_publico: bool,
        alimentacion_incluida: bool,
    ) -> None:
        super().__init__(nombre, lider, ubicacion, num_habitaciones, contacto)
        self._acceso_transporte_publico = acceso_transporte_publico
        self._alimentacion_incluida     = alimentacion_incluida

    @property
    def alimentacion_incluida(self) -> bool:
        return self._alimentacion_incluida

    def reservar_alimentacion(self) -> None:
        if self._alimentacion_incluida:
            print(f"  Alimentación reservada para el hotel {self.nombre}.")
        else:
            print(f"  La alimentación no está incluida en {self.nombre}.")

    def consultar_informacion(self) -> None:
        yn = lambda v: "Sí" if v else "No"
        print(
            f"[HOTEL URBANO: {self.nombre}]\n"
            f"  Líder                     : {self.lider}\n"
            f"  Ubicación                 : {self.ubicacion}\n"
            f"  Contacto                  : {self.contacto}\n"
            f"  Acceso transporte público : {yn(self._acceso_transporte_publico)}\n"
            f"  Alimentación              : {'Incluida' if self._alimentacion_incluida else 'No incluida'}\n"
            f"  Habitaciones disponibles  : {self.habitaciones_disponibles} / {self.num_habitaciones}"
        )


class HotelRural(Hotel):
    """Hotel en zona rural con traslados y recorridos incluidos."""

    def __init__(
        self,
        nombre: str,
        lider: str,
        ubicacion: str,
        num_habitaciones: int,
        contacto: str,
        tipo_traslado: str,
        recorridos_incluidos: list[str],
    ) -> None:
        super().__init__(nombre, lider, ubicacion, num_habitaciones, contacto)
        self._tipo_traslado        = tipo_traslado
        self._recorridos_incluidos = recorridos_incluidos

    def reservar_tipo_traslado(self) -> None:
        print(f"  Traslado en {self._tipo_traslado} reservado para {self.nombre}.")

    def reservar_recorrido(self, recorrido: str) -> None:
        if recorrido in self._recorridos_incluidos:
            print(f"  Recorrido '{recorrido}' reservado exitosamente.")
        else:
            print(f"  El recorrido '{recorrido}' no está disponible en este hotel.")

    def consultar_informacion(self) -> None:
        print(
            f"[HOTEL RURAL: {self.nombre}]\n"
            f"  Líder                    : {self.lider}\n"
            f"  Ubicación                : {self.ubicacion}\n"
            f"  Contacto                 : {self.contacto}\n"
            f"  Tipo de traslado         : {self._tipo_traslado}\n"
            f"  Recorridos incluidos     : {', '.join(self._recorridos_incluidos)}\n"
            f"  Habitaciones disponibles : {self.habitaciones_disponibles} / {self.num_habitaciones}"
        )


class Reserva:
    """
    Reserva de una habitación por parte de un huésped.

    Al crearse, ocupa la habitación y reduce el inventario del hotel.
    Al cancelarse, libera ambos recursos. La factura se emite por separado
    una vez confirmada la estadía.
    """

    _secuencia = count(1)

    def __init__(
        self,
        huesped: Huesped,
        habitacion: Habitacion,
        hotel: Hotel,
        empleado_responsable: EmpleadoHotel,
        fecha_entrada: date,
        fecha_salida: date,
    ) -> None:
        if fecha_salida <= fecha_entrada:
            raise ValueError("La fecha de salida debe ser posterior a la de entrada.")
        if not habitacion.esta_disponible:
            raise ValueError(f"La habitación #{habitacion.numero} no está disponible.")

        self._numero_reserva       = next(Reserva._secuencia)
        self._huesped              = huesped
        self._habitacion           = habitacion
        self._hotel                = hotel
        self._empleado_responsable = empleado_responsable
        self._fecha_entrada        = fecha_entrada
        self._fecha_salida         = fecha_salida
        self._num_noches           = (fecha_salida - fecha_entrada).days
        self._estado               = EstadoReserva.ACTIVA

        habitacion.marcar_ocupada()
        hotel.reducir_disponibilidad()

    @property
    def numero_reserva(self) -> int:
        return self._numero_reserva

    @property
    def huesped(self) -> Huesped:
        return self._huesped

    @property
    def habitacion(self) -> Habitacion:
        return self._habitacion

    @property
    def hotel(self) -> Hotel:
        return self._hotel

    @property
    def empleado_responsable(self) -> EmpleadoHotel:
        return self._empleado_responsable

    @property
    def fecha_entrada(self) -> date:
        return self._fecha_entrada

    @property
    def fecha_salida(self) -> date:
        return self._fecha_salida

    @property
    def num_noches(self) -> int:
        return self._num_noches

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def esta_activa(self) -> bool:
        return self._estado == EstadoReserva.ACTIVA

    def cancelar(self) -> None:
        if not self.esta_activa:
            raise RuntimeError(f"La reserva #{self._numero_reserva} ya está cancelada.")
        self._estado = EstadoReserva.CANCELADA
        self._habitacion.marcar_disponible()
        self._hotel.aumentar_disponibilidad()
        print(f"  Reserva #{self._numero_reserva} cancelada. Habitación liberada.")

    def consultar_informacion(self) -> None:
        print(
            f"[RESERVA #{self._numero_reserva}]\n"
            f"  Huésped              : {self._huesped.nombre}\n"
            f"  Hotel                : {self._hotel.nombre}\n"
            f"  Habitación           : #{self._habitacion.numero}\n"
            f"  Empleado responsable : {self._empleado_responsable.nombre}\n"
            f"  Fecha entrada        : {self._fecha_entrada}\n"
            f"  Fecha salida         : {self._fecha_salida}\n"
            f"  Noches               : {self._num_noches}\n"
            f"  Estado               : {self._estado}"
        )


class FacturaHotel:
    """
    Factura generada al finalizar una estadía.

    Calcula el total sobre la reserva activa y registra el check-out
    implícito marcando la habitación como disponible. No puede emitirse
    sobre reservas previamente canceladas.
    """

    _secuencia = count(1)

    def __init__(
        self,
        reserva: Reserva,
        servicios_adicionales: float = 0,
    ) -> None:
        if not reserva.esta_activa:
            raise ValueError("No se puede facturar una reserva cancelada.")
        if servicios_adicionales < 0:
            raise ValueError("Los servicios adicionales no pueden ser negativos.")

        self._numero_factura        = next(FacturaHotel._secuencia)
        self._reserva               = reserva
        self._servicios_adicionales = servicios_adicionales
        self._subtotal_habitacion   = reserva.habitacion.precio_noche * reserva.num_noches
        self._total                 = self._subtotal_habitacion + servicios_adicionales
        self._fecha_emision         = date.today()
        self._estado_pago           = EstadoPago.PENDIENTE

        reserva.habitacion.marcar_disponible()

    @property
    def total(self) -> float:
        return self._total

    @property
    def estado_pago(self) -> str:
        return self._estado_pago

    def registrar_pago(self) -> None:
        if self._estado_pago == EstadoPago.PAGADA:
            print(f"  La factura #{self._numero_factura} ya fue pagada.")
            return
        self._estado_pago = EstadoPago.PAGADA
        print(f"  Pago registrado. Factura #{self._numero_factura} pagada.")

    def consultar_informacion(self) -> None:
        print(
            f"[FACTURA HOTEL #{self._numero_factura}]\n"
            f"  Reserva #       : {self._reserva.numero_reserva}\n"
            f"  Huésped         : {self._reserva.huesped.nombre}\n"
            f"  Hotel           : {self._reserva.hotel.nombre}\n"
            f"  Noches          : {self._reserva.num_noches}\n"
            f"  Subtotal hab.   : ${self._subtotal_habitacion:,.0f}\n"
            f"  Servicios adic. : ${self._servicios_adicionales:,.0f}\n"
            f"  TOTAL           : ${self._total:,.0f}\n"
            f"  Fecha emisión   : {self._fecha_emision}\n"
            f"  Estado de pago  : {self._estado_pago}"
        )


if __name__ == "__main__":
    hotel_urbano = HotelUrbano(
        nombre="Hotel Manizales Centro",
        lider="Carlos Ramírez",
        ubicacion="Calle 23 #18-45, Manizales",
        num_habitaciones=20,
        contacto="3101234567",
        acceso_transporte_publico=True,
        alimentacion_incluida=True,
    )

    hotel_rural = HotelRural(
        nombre="Finca La Cabaña",
        lider="María López",
        ubicacion="Vereda El Rosario, km 12",
        num_habitaciones=8,
        contacto="3209876543",
        tipo_traslado="Jeep 4x4",
        recorridos_incluidos=["Avistamiento de aves", "Caminata al mirador", "Visita al cafetal"],
    )

    print("\n--- Información de los hoteles ---")
    hotel_urbano.consultar_informacion()
    print()
    hotel_rural.consultar_informacion()

    hab1 = HabitacionIndividual(
        numero=101, precio_noche=150_000, estado=EstadoHabitacion.DISPONIBLE,
        cantidad_camas=1, cantidad_banos=1, aire_acondicionado=True,
        espacio_abierto=False, tiene_televisor=True,
    )

    hab2 = HabitacionMultiple(
        numero=201, precio_noche=280_000, estado=EstadoHabitacion.DISPONIBLE,
        aforo_maximo=4, cantidad_camas=2, cantidad_banos=2,
        aire_acondicionado=True, cantidad_televisores=2, cantidad_espacios_abiertos=1,
    )

    print("\n--- Información de habitaciones ---")
    hab1.consultar_informacion()
    print()
    hab2.consultar_informacion()

    huesped1 = Huesped(
        nombre="Ana Sofía Torres", cedula="1234567890", contacto="3151112233",
        fecha_nacimiento=date(1995, 4, 12), direccion="Carrera 10 #5-20, Bogotá",
        nacionalidad="Colombiana", idioma="Español",
    )

    empleado1 = EmpleadoHotel(
        nombre="Juan Pérez", cedula="9876543210", contacto="3006667788",
        fecha_nacimiento=date(1988, 9, 3), direccion="Calle 50 #30-10, Manizales",
        cargo="Recepcionista", idiomas=["Español", "Inglés"],
    )

    print("\n--- Información de personas ---")
    huesped1.consultar_informacion()
    print()
    empleado1.consultar_informacion()

    reserva1 = Reserva(
        huesped=huesped1,
        habitacion=hab1,
        hotel=hotel_urbano,
        empleado_responsable=empleado1,
        fecha_entrada=date(2026, 6, 10),
        fecha_salida=date(2026, 6, 13),
    )

    print("\n--- Reserva creada ---")
    reserva1.consultar_informacion()

    print("\n--- Reservando servicios adicionales ---")
    hotel_urbano.reservar_alimentacion()

    factura1 = FacturaHotel(reserva=reserva1, servicios_adicionales=50_000)

    print("\n--- Factura generada ---")
    factura1.consultar_informacion()

    print("\n--- Registrando pago ---")
    factura1.registrar_pago()
    factura1.consultar_informacion()

    print("\n--- Demo hotel rural ---")
    hotel_rural.reservar_tipo_traslado()
    hotel_rural.reservar_recorrido("Caminata al mirador")
    hotel_rural.reservar_recorrido("Tour en barco")
