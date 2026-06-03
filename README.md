Hotel PMS — Sistema de Gestión Hotelera (Demo Interactiva)
Una demo web interactiva que traduce fielmente un sistema de gestión hotelera escrito en Python (POO) a una aplicación frontend funcional, permitiendo visualizar y operar la lógica del negocio directamente en el navegador.

GitHub PagesHTML5JavaScriptPython POO

🌐 Acceso en Vivo
El sistema está desplegado y listo para interactuar en GitHub Pages:

https://tu-usuario.github.io/hotel/ (Reemplaza con tu URL real)

📖 Contexto del Proyecto
Este proyecto nace de la necesidad de presentar un sistema de gestión hotelera desarrollado en Python utilizando Programación Orientada a Objetos (POO). En lugar de limitar la presentación a la ejecución en terminal, se ha creado una beta interactiva web que replica exactamente la misma lógica, estructuras de datos y efectos colaterales del código original, pero con una interfaz visual profesional.

La demo permite al profesor y a cualquier usuario:

Realizar el flujo completo de gestión hotelera (Check-in, Check-out, Reservas, Facturación).
Observar en tiempo real cómo los cambios de estado afectan a las entidades del sistema.
Visualizar la salida exacta del código Python por cada acción realizada, gracias a una consola integrada.
⚙️ Mapeo de Arquitectura: Python POO ↔ JavaScript
El núcleo de este proyecto es la fidelidad al modelo de dominio original. Cada clase abstracta, herencia, propiedad y método del código Python existe como un equivalente en JavaScript dentro del archivo index.html.

Clase Python (Original)	Clase JavaScript (Web)	Descripción
EstadoHabitacion, EstadoReserva, EstadoPago	Constantes EstadoHabitacion, etc.	Enums / Constantes de estado
Persona (ABC)	Persona	Clase base abstracta con validación de nombre y cédula
Huesped(Persona)	Huesped extends Persona	Añade nacionalidad e idioma
EmpleadoHotel(Persona)	EmpleadoHotel extends Persona	Añade cargo e idiomas (valida ≥1)
Habitacion(ABC)	Habitacion	Base con gestión de estado (marcarOcupada, marcarDisponible)
HabitacionIndividual(Habitacion)	HabitacionIndividual extends Habitacion	Aforo = 1, espacio abierto, televisor
HabitacionMultiple(Habitacion)	HabitacionMultiple extends Habitacion	Aforo > 1, múltiples televisores/espacios
Hotel(ABC)	Hotel	Control de inventario (reducirDisponibilidad, aumentarDisponibilidad)
HotelUrbano(Hotel)	HotelUrbano extends Hotel	Servicio de alimentación
HotelRural(Hotel)	HotelRural extends Hotel	Traslados y recorridos ecológicos
Reserva	Reserva	Ocupa habitación al crear, libera al cancelar
FacturaHotel	FacturaHotel	Check-out implícito al facturar, cálculo de totales
Efectos Colaterales Garantizados
Al igual que en el código Python:

Crear una Reserva → marca la Habitacion como ocupada y reduce el inventario del Hotel.
Cancelar una Reserva → marca la Habitacion como disponible y aumenta el inventario del Hotel.
Generar una FacturaHotel → realiza el check-out implícito (libera la habitación y el inventario).
Funcionalidades de la Interfaz
📊 Dashboard: Vista general con ocupación en tiempo real, reservas activas, ingresos y actividad reciente.
🏨 Hoteles: Gestión de hoteles urbanos y rurales, con sus servicios específicos (alimentación, traslados, recorridos).
🚪 Habitaciones: Mapa visual de habitaciones con filtros por estado y hotel.
👥 Huéspedes y Empleados: Registro y consulta del personal y visitantes.
📅 Reservas: Creación, cancelación y consulta. Refleja instantáneamente la disponibilidad.
💰 Facturación: Generación de facturas (check-out) y registro de pagos.
🖥️ Consola Integrada: Cada acción ejecuta los métodos equivalentes de Python y muestra la salida print() original en un panel inferior.
