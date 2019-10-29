import socket
import threading
import time
from io import BytesIO


class ClientTCP(threading.Thread):
    def __init__(self, host, port, initial_message):
        super().__init__()
        self.host = host
        self.port = port
        self.connected = False
        self.initial_message = initial_message
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(True)

    def init_connection(self):
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
            return True
        except (ValueError, Exception) as e:
            print(e)
            pass
        return False

    def proceso_(self, line):
        text = line.rstrip().decode("utf-8")
        # print("Linea recibida: {}".format(line.rstrip()))
        print(text)
        if text == "@[JSONWriterEND]":
            print("El proceso ha finalizado")
            self.connected = False

    def send__initial_message(self):
        self.socket.sendall(str(self.initial_message).encode("utf-8"))

    def escuchar(self):
        print("Escuchando")
        self.send__initial_message()
        with BytesIO() as buffer:
            while self.connected:
                try:
                    resp = self.socket.recv(100)  # Read in some number of bytes -- balance this
                except (BlockingIOError, Exception) as e:
                    print("Error producido por conexión: ", e)  # Do whatever you want here, this just
                    time.sleep(1)  # illustrates that it's nonblocking
                    self.connected = False
                else:
                    buffer.write(resp)  # Write to the BytesIO object
                    buffer.seek(0)  # Establecer el puntero de archivo temporal SoF
                    start_index = 0
                    for line in buffer:
                        start_index += len(line)
                        self.proceso_(line)  # La linea
                    """ Si recibimos líneas terminadas en nueva línea, esto será distinto de cero.
                         En ese caso, leemos los bytes restantes en la memoria, truncamos
                         el objeto BytesIO, reinicie el puntero del archivo y vuelva a escribir el
                         bytes restantes de nuevo en él. Esto avanzará el puntero del archivo
                         apropiadamente. Si start_index es cero, el búfer no contiene
                         cualquier línea terminada en nueva línea, por lo que establecemos el puntero del archivo en
                         fin del archivo para no sobrescribir bytes.
                    """
                    if start_index:
                        buffer.seek(start_index)
                        remaining = buffer.read()
                        buffer.truncate(0)
                        buffer.seek(0)
                        buffer.write(remaining)
                    else:
                        buffer.seek(0, 2)
        pass

    def run(self):
        connected = self.init_connection()
        if connected:
            print("Conexion establecida con exito")
            threading.Thread(self.escuchar()).start()
            return
        print("Error al conectar al servidor")


ClientTCP("127.0.0.1", 2020, "-convert --pages all --guess --format JSON --outfile ./catalogo.json --silent "
                             "./db_otros_files/otra_bodega/catalogo.pdf\n").start()
