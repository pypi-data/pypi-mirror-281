import ctypes
import os

class MemoryStruct(ctypes.Structure):
    _fields_ = [("memory", ctypes.POINTER(ctypes.c_char)), ("size", ctypes.c_size_t)]

lib_path = '/usr/local/lib/green_requests.so'
if not os.path.exists(lib_path):
    raise FileNotFoundError("Library 'green_requests.so' is not found in /usr/local/lib/. Please install it before using this package.")
green_req = ctypes.CDLL(lib_path)


green_req.make_request.restype = MemoryStruct
green_req.make_request.argtypes = [ctypes.c_char_p]

def get(url):
    response = green_req.make_request(url.encode('utf-8'))
    response_data = ctypes.string_at(response.memory, response.size)
    green_req.free_memory.argtypes = [MemoryStruct]
    green_req.free_memory(response)
    return response_data.decode('utf-8')
