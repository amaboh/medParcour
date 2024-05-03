import sys
sys.path.append('/Volumes/AM/Desktop/Projects/medParcour/backend')

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from backend.app.services.conversation_service import ConversationService

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'health_journal_reminder',
    default_args=default_args,
    description='Send health journal reminder and initiate conversation',
    schedule_interval=timedelta(minutes=3),
)

def send_reminder_and_initiate_conversation():
    conversation_service = ConversationService()
    users = conversation_service.get_all_users()  

    for user in users:
        user_id = user.id
        conversation_service.send_reminder_text_message(user_id)  
        conversation_service.initiate_conversation(user_id)

send_reminder_and_initiate_conversation_task = PythonOperator(
    task_id='send_reminder_and_initiate_conversation',
    python_callable=send_reminder_and_initiate_conversation,
    dag=dag,
)