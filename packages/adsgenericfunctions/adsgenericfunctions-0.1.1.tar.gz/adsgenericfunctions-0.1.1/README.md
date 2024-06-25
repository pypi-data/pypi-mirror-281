# Alchimie Data Solutions : Generic functions

The purpose of this Python package is to group together all the generic functions used in Onyx development.

## adsGenericFunctions

### LogLine class
#### def __init__(self, time: str, level: str, comment: str)

This class is used to keep track of the actions performed in a job. It takes 3 string arguments, the time, usually now(), the log level, 'error' or 'info' and the comment, which is the message.
This class currently has 3 functions.

#### def log(logs: List[LogLine], level: str, comment: str) -> List[LogLine]

This function adds a log to the list of logs, if the runtime log level is 'debug', all new logs will be printed immediately, if the log level is 'info', the logs will be added to a list to be displayed later. Finally, if the log level is 'error', only logs that has the same level will be added to the list.
The arguments are the list of logs, the level of the log to add and his comment. Returns the list of logs with the new log added.

#### def print_logs(logs: List[LogLine]) -> None

This function print the logs in the parameter logs.

#### def raise_error(logs: List[LogLine]) -> List[Exception]

This function is used to filter logs to find "error" level logs and raise an exception list with them.

#### def adsPgConnect(database: str, user: str, password: str, port: str, host: str, logs: List[LogLine]) -> (Optional['psycopg2.connection'], List[LogLine])

This function connects to a postgres database using the database name, user, password, port and host. The function also needs the logs to add a new one indicating whether it was successful or not.
It returns the connection if successful, none if unsuccessful, and the list of logs.

#### def adsPgRead(query: str, connection: 'psycopg2.connection', logs: List[LogLine]) -> (Optional[List[Tuple]], List[LogLine])

This function reads the database to which the `connection` parameter allow it to connect. This function also needs the `query` to know what it should read, and the list of logs to add a new log indicating whether or not the read was successful.
It returns the data read if the read was successful, and none if the read was unsuccessful, as well as the list of logs.

#### def adsPgExec(query: str, connection: 'psycopg2.connection', logs: List[LogLine]) -> List[LogLine]

This function executes the `query` on the database to which the `connection` parameter allows it to connect. The query can be an insert, update or delete operation. This function needs the list of logs in order to add a new one indicating whether the execution was successful or not.
It returns the list of logs.

#### def send_mail(sgApiClient: str, destinataire: List[str], msg: str, from_email: str, subject: str, logs: List[LogLine]) -> (Response, List[LogLine])

This function sends an email to the `destinataire` from `from_email` with the subject `subject` and a message `msg`. It also needs the api key `sgApiClient` and the list of logs.
It returns the send response and the log list.
