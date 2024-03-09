'''
    Populating db with banner messages
'''
import hashlib
from firestore.database import db_manager

db = db_manager.db
bm_col = db.collection("banner_messages")

def generate_messages(cm_messages):
    '''
        sets a list of messages.
        takes in list of 3 tuple 
        author, message, list of tags
    '''
    for message in cm_messages:
        message_bytes = message[1].encode('utf-8')
        sha1_hash = hashlib.sha1(message_bytes).hexdigest()
        key = f"{sha1_hash}-{message[0].replace(" ", "_")}"
        doc = bm_col.document(key)

        info = {
            "author": message[0],
            "message": message[1],
            "tags": message[2]
        }
        doc.set(info)
        print(f"key: {key}\ninfo: {info}")


def generate_message(author, message, tags):
    '''
        sets a single message
    '''
    message_bytes = message.encode('utf-8')
    sha1_hash = hashlib.sha1(message_bytes).hexdigest()
    key = f"{sha1_hash}-{author.replace(" ", "_")}"
    doc = bm_col.document(key)
    info = {"author": author, "message": message, "tags": tags}
    doc.set(info)
    print(f"key: {key}\ninfo: {info}")
