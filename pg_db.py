import psycopg2
from config_db import config
from time import gmtime, strftime


def connect():
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        with conn.cursor() as cursor:
            conn.autocommit = True
            insert = cursor.execute("INSERT INTO users (id, nikname, firstname, lastname, email, psw, time) VALUES  ('8', 'ALA3', 'Almaty2', 'Kazakhstan2', 'ALA2', 'Almaty2', '2015')")
            print(insert)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def create_tables(Conference,
                  BridgeUniqueid,
                  BridgeName,
                  state_conference = "temp",
                  TimeEnd = "no infofmation"):
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)

    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        with conn.cursor() as cursor:
            conn.autocommit = True

            create = cursor.execute(f"""CREATE TABLE IF NOT EXISTS conf_{BridgeName} (
                                        id_number serial PRIMARY KEY,
                                        Channel text NOT NULL UNIQUE,
                                        CallerIDNum text NOT NULL,
                                        CallerIDName text,
                                        ConfbridgeTalking text,
                                        TimeStart text,
                                        TimeEnd text,
                                        Admin text
                                    )""")
            create_all = cursor.execute(f"""CREATE TABLE IF NOT EXISTS conf_list (
                                                    id_number serial PRIMARY KEY,
                                                    BridgeUniqueid text NOT NULL,
                                                    BridgeName text NOT NULL UNIQUE,
                                                    Conference text,
                                                    TimeCreate text,
                                                    TimeEnd text,
                                                    state_conference text
                                                )""")
            print(create)
            print(create_all)
            print('Database created!')
            postgres_insert_query = (f"INSERT INTO conf_list (BridgeUniqueid, BridgeName, Conference,"
                                     f" TimeCreate, TimeEnd, state_conference)"
                                     f" VALUES (%s,%s,%s,%s,%s,%s) "
                                     f"ON CONFLICT (BridgeName) DO UPDATE SET "
                                     f"BridgeUniqueid = excluded.BridgeUniqueid, "
                                     f"Conference = excluded.Conference, "
                                     f"TimeCreate = excluded.TimeCreate, "
                                     f"TimeEnd = excluded.TimeEnd")

            # print(postgres_insert_query)
            record_to_insert = (BridgeUniqueid, BridgeName, Conference, timenow, TimeEnd, state_conference)
            # print(record_to_insert)
            cursor.execute(postgres_insert_query, record_to_insert)


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def join_participants(BridgeUniqueid,
                      BridgeName,
                      Channel,
                      CallerIDNum,
                      CallerIDName,
                      ConfbridgeTalking = "no information",
                      TimeStart = "no information",
                      TimeEnd = "no information",
                      Admin = "no information"):

    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)
    print(BridgeUniqueid, BridgeName, Channel, CallerIDNum, CallerIDName, Admin)
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            postgres_insert_query = (f"INSERT INTO conf_{BridgeName} (Channel, CallerIDNum, CallerIDName, ConfbridgeTalking, TimeStart, TimeEnd, Admin) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (Channel) DO UPDATE SET ConfbridgeTalking = excluded.ConfbridgeTalking, TimeEnd = excluded.TimeEnd, Admin = excluded.Admin")
            record_to_insert = (Channel, CallerIDNum, CallerIDName, ConfbridgeTalking, TimeStart, TimeEnd, Admin)
            cursor.execute(postgres_insert_query, record_to_insert)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def delete_participants(BridgeUniqueid,
                        BridgeName,
                        Channel,
                        CallerIDNum,
                        CallerIDName,
                        TimeStart = "no information",
                        TimeEnd = "no information",
                        Admin = "no information"):
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            postgres_delete_query = (f"DELETE FROM conf_{BridgeName} WHERE Channel = %s")
            record_to_delete = (Channel,)
            cursor.execute(postgres_delete_query, record_to_delete)
            print(cursor.execute(postgres_delete_query, record_to_delete))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def delete_conference(BridgeUniqueid, BridgeName):
    print(BridgeName)
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    TimeEnd = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            print("START DROP TABLE")
            postgres_insert_query = (f"DROP TABLE conf_{BridgeName}")
            record_to_insert = (BridgeName,)
            cursor.execute(postgres_insert_query, record_to_insert)
            print("DROP TABLE")

            postgres_insert_query = "UPDATE conf_list SET TimeEnd = (%s) WHERE BridgeUniqueid = (%s)"
            record_to_insert = (TimeEnd, BridgeUniqueid)
            cursor.execute(postgres_insert_query, record_to_insert)
            print("UPDATE conf_list")
            delete_conference_record = cursor.execute(f"DELETE FROM conf_list WHERE BridgeUniqueid = '{BridgeUniqueid}' AND state_conference = 'temp' ")
            print("DELETE FROM conf_list")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')





