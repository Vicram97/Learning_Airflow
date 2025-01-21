from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
#from airflow.providers.smtp.operators.smtp import EmailOperator
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

# Definir los parámetros por defecto para el DAG
default_args = {
    'owner': 'Pepe',
    'start_date': datetime(2025, 1, 20),  # Ajusta la fecha a tu necesidad
    "email_on_success": False,  # Esta opción también enviará un correo en caso de éxito
    "email": "ramosfuentesvictor@example.com",  # Este es el correo al cual se enviarán las notificaciones (opcional)
}

# Crear el objeto DAG
dag = DAG(
    'send_email_dag_with_image',  # Nombre del DAG
    default_args=default_args,
    schedule_interval="@daily",  # No se ejecutará de manera automática, puede ser programado según lo que necesites
    catchup=True,  # No se ejecutarán tareas pendientes desde fechas pasadas
)

# Definir la tarea DummyOperator (para indicar un punto de inicio)
start_task = EmptyOperator(
    task_id='start',
    dag=dag,
)

# Función para enviar correo con imagen embebida
def send_email_with_image():
    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = 'ramosfuentesvictor@example.com'
    msg['To'] = 'ramosfuentesvictor@gmail.com'  # Correo del destinatario
    msg['Subject'] = 'Mail del día de Airflow'

    # Contenido HTML
    html_content = """
    <html>
      <body>
        <h3>Este es un correo con una imagen embebida:</h3>
        <img src="cid:image1">
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html'))

    # Adjuntar la imagen
    with open(r"C:\Users\Victor Ramos Fuentes\Documents\Docker_Files\images\ratas.jpeg", 'rb') as img_file:  # Ruta de tu imagen
        img = MIMEImage(img_file.read())
        img.add_header('Content-ID', '<image1>')  # Referencia de CID para usar en el HTML
        msg.attach(img)

    # Enviar el correo
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('ramosfuentesvictor@example.com', 'your_app_password')  # Autenticación de tu cuenta
        server.sendmail(msg['From'], msg['To'], msg.as_string())

# Definir la tarea PythonOperator para enviar el correo
send_email_task = PythonOperator(
    task_id='send_email_with_image',
    python_callable=send_email_with_image,
    dag=dag
)

# Establecer las dependencias
start_task >> send_email_task  # El correo con la imagen se enviará después de la tarea 'start'
