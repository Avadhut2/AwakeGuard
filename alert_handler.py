from collections import deque
from database_handler import insert_alert

alert_queue = deque()
frame_stack = []

class AlertNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class AlertHistory:
    def __init__(self):
        self.head = None
    
    def add_alert(self, data):
        new_node = AlertNode(data)
        new_node.next = self.head
        self.head = new_node
    
    def display(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

history = AlertHistory()

def enqueue_alert(alert):
    alert_queue.append(alert)

def push_frame(frame):
    frame_stack.append(frame)

def undo_last_frame():
    if frame_stack:
        return frame_stack.pop()
    return None

def process_alerts():
    while alert_queue:
        alert = alert_queue.popleft()
        history.add_alert(alert)
        insert_alert(alert)
