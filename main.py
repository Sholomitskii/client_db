import psycopg2

def create_structure():
    cur.execute("""
    DROP TABLE phone_number;
    DROP TABLE client_info;
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS  client_info(
        id SERIAL PRIMARY KEY,
        name VARCHAR(20),
        surname VARCHAR(30),
        email VARCHAR(50)
    );
    """) 

    cur.execute("""
    CREATE TABLE IF NOT EXISTS  phone_number(
        id SERIAL PRIMARY KEY,
        ph_number VARCHAR(20),
        client_id INTEGER NOT NULL REFERENCES client_info(id)
    );
    """)

def add_client(name, surname, email, ph_number=None):
    cur.execute("""
    INSERT INTO client_info(name, surname, email) VALUES(%s,%s,%s) RETURNING id;
    """,(name, surname, email))
    client_id = cur.fetchone()
    cur.execute("""
    INSERT INTO phone_number(ph_number, client_id) VALUES(%s,%s);
    """, (ph_number, client_id))

def add_phone_number(ph_number, client_id):
    cur.execute("""
    INSERT INTO phone_number(ph_number, client_id) VALUES(%s,%s);
    """, (ph_number, client_id))

def change_data(id, new_name=None, new_surname=None, new_email=None):
    if new_name != None:
        cur.execute("""
        UPDATE client_info SET name=%s WHERE id=%s;
        """, (new_name, id))
    if new_surname != None:
        cur.execute("""
        UPDATE client_info SET surname=%s WHERE id=%s;
        """, (new_surname, id))
    if new_email != None:
        cur.execute("""
        UPDATE client_info SET email=%s WHERE id=%s;
        """, (new_email, id))
    
def delete_phone_number(client_id):
    cur.execute("""
    DELETE FROM phone_number WHERE client_id=%s; 
    """, (client_id))

def delete_client(id):
    cur.execute("""
    DELETE FROM phone_number WHERE client_id=%s; 
    """, (id))
    cur.execute("""
    DELETE FROM client_info WHERE id=%s; 
    """, (id))

def find_client(name=None, surname=None, email=None, ph_number=None):
    if name != None:
        cur.execute(f"""
        SELECT * FROM client_info WHERE name iLike '{name}'; 
        """)
        result = cur.fetchone()
        print(result) 
    if surname != None:
        cur.execute(f"""
        SELECT * FROM client_info WHERE surname iLike '{surname}'; 
        """)
        result = cur.fetchone()
        print(result)
    if email != None:
        cur.execute(f"""
        SELECT * FROM client_info WHERE email iLike '{email}'; 
        """)
        result = cur.fetchone()
        print(result)
    if ph_number != None:
        cur.execute(f"""
        SELECT client_id FROM phone_number WHERE ph_number iLike '{ph_number}'; 
        """)
        client_id = cur.fetchone()[0]
        cur.execute(f"""
        SELECT * FROM client_info WHERE id={client_id};
        """)
        result = cur.fetchone()
        print(result)
    
with psycopg2.connect(database='client_db', user='postgres') as conn:
    with conn.cursor() as cur:
        create_structure()
        add_client(name='Arkadii', surname='Karavanov', email='ark1234@mail.com')
        add_client(name='Vasilii',surname='Verevkin',email='vasvas1234@mail.com',ph_number='+79101012471')
        add_client(name='Gennadii',surname='Kon',email='gena1234@mail.com',ph_number='+79166012471')
        add_phone_number('+79057782121', 1)
        change_data(1, new_email='arkan1999@mail.com')
        delete_phone_number('2')
        delete_client('1')
        find_client(name='Vasilii')

        conn.commit()
