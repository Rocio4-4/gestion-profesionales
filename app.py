import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --------------------------------
# CONFIGURACION
# --------------------------------

st.set_page_config(
    page_title="Lic. María López",
    page_icon="🥗",
    layout="centered"
)

USUARIO_ADMIN = "admin"
CLAVE_ADMIN = "1234"

# --------------------------------
# SELECTOR DE PERFIL
# --------------------------------

tipo_usuario = st.sidebar.selectbox(
    "Ingresar como",
    ["Cliente", "Profesional"]
)

# --------------------------------
# PROFESIONAL
# --------------------------------

if tipo_usuario == "Profesional":

    st.title("🔒 Panel Profesional")

    usuario = st.text_input("Usuario")

    password = st.text_input(
        "Contraseña",
        type="password"
    )

    if usuario == USUARIO_ADMIN and password == CLAVE_ADMIN:

        st.success("Bienvenido")

        menu_admin = st.selectbox(
            "Menú",
            [
                "Mis Turnos",
                "Mis Ventas",
                "Dashboard"
            ]
        )

        if menu_admin == "Mis Turnos":

            st.header("📅 Mis Turnos")

            if os.path.exists("reservas.xlsx"):

                reservas = pd.read_excel(
                    "reservas.xlsx"
                )

                st.dataframe(reservas)

            else:
                st.info("No hay reservas registradas.")

        if menu_admin == "Mis Ventas":

            st.header("💰 Mis Ventas")

            if os.path.exists("ventas.xlsx"):

                ventas = pd.read_excel(
                    "ventas.xlsx"
                )

                st.dataframe(ventas)

            else:
                st.info("No hay ventas registradas.")

        if menu_admin == "Dashboard":

            st.header("📊 Dashboard")

            total_turnos = 0
            total_ventas = 0
            facturacion = 0

            if os.path.exists("reservas.xlsx"):
                reservas = pd.read_excel("reservas.xlsx")
                total_turnos = len(reservas)

            if os.path.exists("ventas.xlsx"):
                ventas = pd.read_excel("ventas.xlsx")
                total_ventas = len(ventas)

                if "Total" in ventas.columns:
                    facturacion = ventas["Total"].sum()

            st.metric(
                "Turnos",
                total_turnos
            )

            st.metric(
                "Ventas",
                total_ventas
            )

            st.metric(
                "Facturación",
                f"${facturacion:,.0f}"
            )

# --------------------------------
# CLIENTE
# --------------------------------

if tipo_usuario == "Cliente":

    st.title("🥗 Lic. María López")

    st.subheader("Nutrición Personalizada")

    st.write("""
    Te acompaño a mejorar tus hábitos alimenticios
    con un enfoque práctico y sostenible.
    """)

    menu = st.sidebar.selectbox(
        "Seleccionar",
        [
            "Reservar Turno",
            "Servicios"
        ]
    )

    # -----------------------------
    # RESERVAS
    # -----------------------------

    if menu == "Reservar Turno":

        st.header("📅 Reservar Turno")

        nombre = st.text_input(
            "Nombre y Apellido"
        )

        telefono = st.text_input(
            "Teléfono"
        )

        email = st.text_input(
            "Email"
        )

        servicio = st.selectbox(
            "Tipo de Consulta",
            [
                "Consulta Inicial",
                "Control Nutricional",
                "Plan Premium"
            ]
        )

        fecha = st.selectbox(
            "Fecha Disponible",
            [
                "01/10/2026",
                "03/10/2026",
                "05/10/2026",
                "07/10/2026"
            ]
        )

        horario = st.selectbox(
            "Horario Disponible",
            [
                "09:00",
                "10:00",
                "11:00",
                "15:00",
                "16:00",
                "17:00",
                "18:00"
            ]
        )

        if st.button("Confirmar Reserva"):

            nueva_reserva = pd.DataFrame([{
                "Nombre": nombre,
                "Telefono": telefono,
                "Email": email,
                "Servicio": servicio,
                "Fecha": fecha,
                "Horario": horario,
                "FechaRegistro": datetime.now()
            }])

            archivo = "reservas.xlsx"

            if os.path.exists(archivo):

                reservas = pd.read_excel(
                    archivo
                )

                reservas = pd.concat(
                    [reservas, nueva_reserva],
                    ignore_index=True
                )

            else:

                reservas = nueva_reserva

            reservas.to_excel(
                archivo,
                index=False
            )

            st.success(
                "✅ Reserva realizada correctamente"
            )

    # -----------------------------
    # SERVICIOS
    # -----------------------------

    if menu == "Servicios":

        st.header("💰 Servicios")

        st.markdown("""
### Consulta Inicial

$25.000

Evaluación completa y plan personalizado.
""")

        st.markdown("""
### Control Nutricional

$18.000

Seguimiento y ajustes.
""")

        st.markdown("""
### Plan Premium

$40.000

Seguimiento intensivo.
""")

        st.info(
            "Para contratar un servicio comunicate por WhatsApp."
        )

    st.divider()

    st.subheader("📱 Contacto")

    st.write(
        "WhatsApp: +54 11 9999-9999"
    )

    st.write(
        "Instagram: @nutrimarialopez"
    )

    st.write(
        "Email: contacto@nutrimarialopez.com"
    )