import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
        return None
    else:
        return conn
        
def create_test_db():
    conn = create_connection('tess_orders.db')  
    c = conn.cursor()
    sql = []
    
    with open('test_schema.sql', 'r') as r:
        for line in r:
            if len(sql) == 0:
                sql.append(line)
            else:
                if sql[-1].rstrip()[-1] == ';':
                    sql.append(line)
                else:
                    sql[-1] = sql[-1] + line

    for i, string in enumerate(sql):
        try:
            #print(i, string)
            c.execute(string)
        except Error as e:
            print(e)
        finally:
            conn.close()
    

if __name__ == '__main__':
    create_test_db()

