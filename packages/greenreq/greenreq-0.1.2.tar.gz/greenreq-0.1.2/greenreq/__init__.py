import ctypes
import os

class MemoryStruct(ctypes.Structure):
    _fields_ = [("memory", ctypes.POINTER(ctypes.c_char)),
                ("size", ctypes.c_size_t)]

# Path to the library
lib_path = os.path.join(os.path.dirname(__file__), 'green_requests.so')

# Load the library
try:
    requests_c = ctypes.CDLL(lib_path)
except OSError as e:
    raise ImportError(f"Could not load library '{lib_path}': {e}")

# Define the return type and argument types for make_request
requests_c.make_request.restype = MemoryStruct
requests_c.make_request.argtypes = [ctypes.c_char_p]

# Export the functions you need
def make_request(url):
    response = requests_c.make_request(url.encode('utf-8'))
    response_data = ctypes.string_at(response.memory, response.size)
    result = response_data.decode('utf-8')
    requests_c.free_memory(response)
    return result
