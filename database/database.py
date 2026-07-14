import sqlite3
from functools import reduce

def create_chat_room(name, members):
    try:
        with sqlite3.connect('my.db') as conn:
            # create a cursor
            cursor = conn.cursor()

            # execute statements
            statement = f"INSERT INTO ChatRooms (name, content) VALUES ({name}, {reduce(lambda x: x, members)});"#TOTO - finish
            cursor.execute(statement)

            # commit the changes
            conn.commit()

            print("Created chat room succesfully.")
    except sqlite3.OperationalError as e:
        print("Failed to create chat room:", e)

def add_member(room_id, user_id):
    pass

def chat_room_info(room_id):
    pass

