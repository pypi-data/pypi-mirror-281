from python_http_client.client import Response
from sendgrid import SendGridAPIClient, Mail
import psycopg2

class PostgresInput:
    def __init__(self, database: str, user: str, password:str, port:str, host: str, batch_size=1000):
        try:
            self.__connection = psycopg2.connect(
                database=database,
                user=user,
                password=password,
                port=port,
                host=host
            )
        except Exception as e:
            print(f"Connection failed: {str(e)}")
        self.__cursor = self.__connection.cursor()
        self.__batch_size = batch_size

    def __del__(self):
        self.__connection.close()

    def read(self, query: str):
        with self.__connection.cursor() as cursor:
            cursor.execute(query)
            while True:
                rows = cursor.fetchmany(self.__batch_size)
                if not rows:
                    break
                yield from rows

    def write(self, query: str, params=None):
        try:
            if params:
                self.__cursor.execute(query, params)
            else:
                self.__cursor.execute(query)
            self.__connection.commit()
        except Exception as e:
            self.__connection.rollback()
            print(f"Write failed: {str(e)}")

def send_mail(sgApiClient: str, destinataire: str, msg: str, from_email: str, subject: str,) -> Response:
    sg = SendGridAPIClient(sgApiClient)
    mail = Mail(
        from_email=from_email,
        to_emails=destinataire,
        subject=subject,
        html_content=msg
    )
    return sg.send(mail)
