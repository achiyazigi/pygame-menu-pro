class Event:
    def __init__(self):
        self.subscribers = dict()
    
    def subscribe(self, event_type:str, fn):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(fn)

    def post_event(self, event_type:str, *data):
        if event_type not in self.subscribers:
            return
        for fn in self.subscribers[event_type]:
            fn(*data)