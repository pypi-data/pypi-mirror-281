from typing import List, Tuple, Optional
import psycopg2
from datetime import datetime
from python_http_client.client import Response
from sendgrid import SendGridAPIClient, Mail

log_level = 'info'  #str(os.getenv('log_level'))


class LogLine:
    def __init__(self, time: str, level: str, comment: str):
        self.time = time
        self.level = level
        self.comment = comment


def adsPgConnect(database: str, user: str, password: str, port: str, host: str, logs: List[LogLine]) -> (
        Optional['psycopg2.connection'], List[LogLine]):
    try:
        conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            port=port,
            host=host
        )
        logs = log(logs, "info", "Connection success")
        return conn, logs
    except Exception as e:
        logs = log(logs, "error", f"Connection failed: {str(e)}")
        return None, logs


def adsPgRead(query: str, connection: 'psycopg2.connection', logs: List[LogLine]) -> (
        Optional[List[Tuple]], List[LogLine]):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        logs = log(logs, "info", f"Read success")
        return data, logs
    except psycopg2.Error as e:
        logs = log(logs, "error", f"Read failed: {str(e)}")
        return None, logs
    except Exception as e:
        logs = log(logs, "error", f"Unexpected error: {str(e)}")
        return None, logs


def adsPgExec(query: str, connection: 'psycopg2.connection', logs: List[LogLine]) -> List[LogLine]:
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return logs
    except psycopg2.Error as e:
        logs = log(logs, "error", f"Execute failed: {str(e)}")
        return logs
    except Exception as e:
        logs = log(logs, "error", f"Unexpected error: {str(e)}")
        return logs


def log(logs: List[LogLine], level: str, comment: str) -> List[LogLine]:
    now = datetime.now().strftime("%H:%M:%S")
    if log_level == "debug":
        print(f"{now} : {log_level} - {comment}")
    if log_level == "info" or (log_level == "error" and level == "error"):
        logs.append(LogLine(now, level, comment))
    return logs


def print_logs(logs: List[LogLine]) -> None:
    txt = ""
    for log_iter in logs:
        txt += f"{log_iter.time} : {log_iter.level} - {log_iter.comment}\r\n"
    print(txt)


def raise_error(logs: List[LogLine]) -> List[Exception]:
    return [Exception(log_iter.comment) for log_iter in logs if log_iter.level == "error"]


def send_mail(sgApiClient: str, destinataire: List[str], msg: str, from_email: str, subject: str,
              logs: List[LogLine]) -> (Response, List[LogLine]):
    sg = SendGridAPIClient(sgApiClient)
    mail = Mail(
        from_email=from_email,
        to_emails=destinataire,
        subject=subject,
        html_content=msg
    )
    logs = log(logs, "info", f"Mail sent to {destinataire}")
    return sg.send(mail), logs
