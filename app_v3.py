import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import date

# ==================================
# CONFIGURACIÓN
# ==================================

st.set_page_config(
    page_title="App Profesional",
    layout="wide"
)

USUARIO = "admin"
CLAVE = "1234"

# ==================================
# GOOGLE SHEETS
# ==================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credenciales = Credentials.from_service_account_file(
    "credenciales.json",
    scopes=SCOPES
)

cliente = gspread.authorize(credenciales)

planilla = cliente.open_by_key(
    "1kqloWYKGFGgk7xCwXEKxgRv_boaLNzfMGP9sumzV_m8"
)

hoja_reservas = planilla.worksheet("Reservas")
hoja_productos = planilla.worksheet("Productos")
hoja_ventas = planilla.worksheet("Ventas")

# ==================================
# LOGIN
# ==================================

if "login" not in st.session_state:
    st.session_state.login = False

# ==================================
# MENÚ
# ==================================

modo = st.sidebar.radio(
    "Acceso",
    [
        "📅 Reservar Turno",
        "🔐 Acceso Profesional"
    ]
)

# ==================================
# RESERVAS CLIENTE
# ==================================

if modo == "📅 Reservar Turno":

    st.title("📅 Reserva de Turnos")

    nombre = st.text_input("Nombre y Apellido")
    telefono = st.text_input("Teléfono")
    servicio = st.text_input("Servicio")

    fecha = st.date_input(
        "Fecha",
        min_value=date.today()
    )

    dias_permitidos = [0, 2, 4]

    if fecha.weekday() not in dias_permitidos:

        st.warning(
            "Solo se permiten reservas los lunes, miércoles y viernes."
        )

    else:

        horarios = [
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00"
        ]

        reservas = pd.DataFrame(
            hoja_reservas.get_all_records()
        )

        fecha_seleccionada = str(fecha)

        horarios_libres = horarios.copy()

        if not reservas.empty:

            ocupados = reservas.loc[
                reservas["Fecha"] == fecha_seleccionada,
                "Hora"
            ].tolist()

            horarios_libres = [
                h for h in horarios
                if h not in ocupados
            ]

        if len(horarios_libres) == 0:

            st.error(
                "No hay horarios disponibles para esta fecha."
            )

        else:

            hora = st.selectbox(
                "Horario",
                horarios_libres
            )

            if st.button("Reservar Turno"):

                hoja_reservas.append_row([
                    str(fecha),
                    hora,
                    nombre,
                    telefono,
                    servicio
                ])

                st.success(
                    "✅ Reserva registrada correctamente."
                )

# ==================================
# PANEL PROFESIONAL
# ==================================

else:

    if not st.session_state.login:

        st.title("🔐 Acceso Profesional")

        usuario = st.text_input("Usuario")

        clave = st.text_input(
            "Contraseña",
            type="password"
        )

        if st.button("Ingresar"):

            if usuario == USUARIO and clave == CLAVE:

                st.session_state.login = True
                st.rerun()

            else:

                st.error(
                    "Usuario o contraseña incorrectos."
                )

        st.stop()

    menu = st.sidebar.selectbox(
        "Panel Profesional",
        [
            "Dashboard",
            "Reservas",
            "Productos",
            "Ventas"
        ]
    )

    # ------------------------
    # DASHBOARD
    # ------------------------

    if menu == "Dashboard":

        st.title("📊 Dashboard")

        reservas = pd.DataFrame(
            hoja_reservas.get_all_records()
        )

        ventas = pd.DataFrame(
            hoja_ventas.get_all_records()
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Reservas",
                len(reservas)
            )

        with col2:
            st.metric(
                "Total Ventas",
                len(ventas)
            )

    # ------------------------
    # RESERVAS
    # ------------------------

    elif menu == "Reservas":

        st.title("📅 Reservas")

        reservas = pd.DataFrame(
            hoja_reservas.get_all_records()
        )

        st.dataframe(
            reservas,
            use_container_width=True
        )

    # ------------------------
    # PRODUCTOS
    # ------------------------

    elif menu == "Productos":

        st.title("📦 Productos")

        producto = st.text_input(
            "Producto"
        )

        precio = st.number_input(
            "Precio",
            min_value=0.0
        )

        stock = st.number_input(
            "Stock",
            min_value=0
        )

        if st.button("Guardar Producto"):

            hoja_productos.append_row([
                producto,
                precio,
                stock
            ])

            st.success(
                "✅ Producto guardado."
            )

        productos = pd.DataFrame(
            hoja_productos.get_all_records()
        )

        st.dataframe(
            productos,
            use_container_width=True
        )

    # ------------------------
    # VENTAS
    # ------------------------

    elif menu == "Ventas":

        st.title("💰 Ventas")

        fecha_venta = st.date_input(
            "Fecha de venta"
        )

        producto = st.text_input(
            "Producto vendido"
        )

        cantidad = st.number_input(
            "Cantidad",
            min_value=1
        )

        importe = st.number_input(
            "Importe",
            min_value=0.0
        )

        if st.button("Registrar Venta"):

            hoja_ventas.append_row([
                str(fecha_venta),
                producto,
                cantidad,
                importe
            ])

            st.success(
                "✅ Venta registrada."
            )

        ventas = pd.DataFrame(
            hoja_ventas.get_all_records()
        )

        st.dataframe(
            ventas,
            use_container_width=True
        )