# tuplespace.py
import threading

class TupleSpace:
    def __init__(self):
        self.tuple_space = {}

    def put(self, k, v):
        self.tuple_space[k] = v
        # 更新状态
        global tuple_count, total_key_length, total_value_length, total_operations
        tuple_count += 1
        total_key_length += len(k)
        total_value_length += len(v)
        total_operations += 1
        return "OK"

    def read(self, k):
        global total_operations
        total_operations += 1
        return self.tuple_space.get(k, "ERR Key not found")

    def get(self, k):
        global total_operations
        total_operations += 1
        return self.tuple_space.pop(k, "ERR Key not found")
