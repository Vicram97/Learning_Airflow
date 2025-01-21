from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.smtp.operators.smtp import EmailOperator
from datetime import datetime
import random

# Definir los parámetros por defecto para el DAG
default_args = {
    'owner': 'Victor',
    'start_date': datetime(2025, 1, 22),  # Ajusta la fecha a tu necesidad
    "email_on_success": True,  # Esta opción también enviará un correo en caso de éxito
    "email": "ramosfuentesvictor@example.com",  # Este es el correo al cual se enviarán las notificaciones (opcional)
}

# Lista de refranes
refranes = [
    "Camarón que se duerme se lo lleva la corriente.",
    "Más vale tarde que nunca.",
    "A quien madruga, Dios le ayuda.",
    "No hay mal que por bien no venga.",
    "El que mucho abarca, poco aprieta.",
    "A caballo regalado no se le mira el diente.",
    "Dime con quién andas y te diré quién eres.",
    "En casa de herrero, cuchillo de palo."
]

# Función para obtener un refrán aleatorio
def obtener_refran():
    return random.choice(refranes)

# Crear el objeto DAG
dag = DAG(
    'send_email_to_Paula',  # Nombre del DAG
    default_args=default_args,
    schedule_interval="@daily",  # No se ejecutará de manera automática, puede ser programado según lo que necesites
    catchup=True,  # No se ejecutarán tareas pendientes desde fechas pasadas
)

# Definir la tarea DummyOperator (para indicar un punto de inicio)
start_task = EmptyOperator(
    task_id='start',
    dag=dag,
)

# Definir la tarea EmailOperator para enviar el correo electrónico

send_email_task = EmailOperator(
    task_id='send_email',#'pau.guijarroj@gmail.com'
    to=['ramosfuentesvictor@gmail.com', 'pau.guijarroj@gmail.com'],  # Aquí coloca el correo del destinatario
    subject='Aquello que nunca debes olvidar',
    html_content=f"<h1>¡Buenos días!</h1><p>Refrán del día: {obtener_refran()}</p><p>P.D. What are you most worried about? <b>Fernando Alonso<b> <p>",
    dag=dag,
)

# Establecer las dependencias
start_task >> send_email_task  # El correo se enviará después de la tarea 'start'
