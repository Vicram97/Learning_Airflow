from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.smtp.operators.smtp import EmailOperator
from datetime import datetime

# Definir los parámetros por defecto para el DAG
default_args = {
    'owner': 'Victor',
    'start_date': datetime(2025, 1, 20),  # Ajusta la fecha a tu necesidad
    "email_on_success": True,  # Esta opción también enviará un correo en caso de éxito
    "email": "ramosfuentesvictor@example.com",  # Este es el correo al cual se enviarán las notificaciones (opcional)
}

# Crear el objeto DAG
dag = DAG(
    'send_email_dag',  # Nombre del DAG
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
    task_id='send_email',
    to='ramosfuentesvictor@gmail.com',  # Aquí coloca el correo del destinatario
    subject='Mail del dia de Airflow',
    html_content='Buenos dias',
    dag=dag,
)

# Establecer las dependencias
start_task >> send_email_task  # El correo se enviará después de la tarea 'start'
