from flask_sqlalchemy import SQLAlchemy
import json
from twilio.rest import Client
db = SQLAlchemy()

class Queue:

    def __init__(self):
        self._queue = [{"name": "Julio", "phone": "+56945242853"}]
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'
        self.account_sid = "AC676c2a46f8f856c6e433a08017b78e1c"
        self.auth_token = "82442f073d973e9000acb7f782007599"
        self.client = Client(self.account_sid, self.auth_token)


    def enqueue(self, item):
        if self._mode == 'FIFO':
            self._queue.append(item)
            position = len(self._queue)
            msg = f"Added to queue, you are at position:  {position}"
            self.sentMsg(item["phone"], msg )
            return ({"msg": msg})
        if self._mode == 'LIFO':
            self._queue.insert(0,item)
            msg = "Added to queue, you are at position 1"
            self.sentMsg(item["phone"], msg )
            return ({"msg": msg}) 
        
    def dequeue(self):
        if len(self._queue) > 0:
            items = self._queue
            item_removed = items[0]
            name_removed = item_removed['name']
            msg = f"{name_removed}, is your Turn!"
            self.sentMsg(item_removed['phone'], msg )
            self._queue.pop(0)
            return ({"msg": f"{name_removed}, is your Turn"})
        else:
            return None

    def get_queue(self):         
        if len(self._queue) == 0:
            return None
        else:
            return self._queue

    def size(self):
        return len(self._queue)
    
    def sentMsg(self, phone, body):
        self.client.messages.create(
        to = phone, 
        from_= "+12059460962", 
        body = body
        )