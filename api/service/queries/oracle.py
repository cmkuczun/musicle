import cx_Oracle

# Create connection
try: 
    dsn_tns=cx_Oracle.makedsn('localhost','1521','xe')
    connection = cx_Oracle.connect("guest", "guest", dsn_tns)
    # time.sleep(1)
    print("\nSTATUS: Connected to Oracle database.")
except Exception as e:
    print(print("\nSTATUS: Failed to connect to Oracle database."))
    print("ERROR: ", e)

def execute(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        result = cursor.fetchall()
        return result
    except cx_Oracle.Error as error:
        print("ERROR:", error)
        connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
