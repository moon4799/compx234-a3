# tuplespace.py
import threading

class TupleSpace:
    def __init__(self):
        self.tuple_space = {}
        self.lock = threading.Lock()  # 用于保证线程安全

    def put(self, key, value):
        with self.lock:  # 确保该操作是线程安全的
            if key in self.tuple_space:
                return "ERR k already exists"
            else:
                self.tuple_space[key] = value
                return f"OK ({key}, {value}) added"

    def read(self, key):
        with self.lock:
            if key in self.tuple_space:
                return f"OK ({key}, {self.tuple_space[key]}) read"
            else:
                return f"ERR k does not exist"

    def get(self, key):
        with self.lock:
            if key in self.tuple_space:
                value = self.tuple_space.pop(key)
                return f"OK ({key}, {value}) removed"
            else:
                return f"ERR k does not exist"
