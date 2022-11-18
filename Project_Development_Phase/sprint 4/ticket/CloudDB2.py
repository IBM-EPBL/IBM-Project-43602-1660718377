import ibm_db
import ibm_db_dbi
import pandas

dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "bludb"
dsn_hostname = "0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
dsn_port = "31198"
dsn_protocol = "TCPIP"
dsn_uid = "pvy33716"
dsn_pwd = "ENtNnDJRqHuQdJ7Q"
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY=SSL").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)


def run(query):
    conn = ibm_db.connect(dsn, "", "")
    print(query)
    create_table = ibm_db.exec_immediate(conn, query)
    return 1


def check(query):
    conn = ibm_db.connect(dsn, "", "")
    print(query)
    try:
        select = ibm_db.exec_immediate(conn, query)
        return ibm_db.num_rows(select)

    except:
        return 0


def view(query):
    conn = ibm_db.connect(dsn, "", "")
    pd_conn = ibm_db_dbi.Connection(conn)
    print(query)
    try:
        select = ibm_db.exec_immediate(conn, query)
        result = []
        dictionary = ibm_db.fetch_assoc(select)
        while dictionary != False:
            result.append(dictionary)
            dictionary = ibm_db.fetch_assoc(select)

        return result

    except:
        return ''
