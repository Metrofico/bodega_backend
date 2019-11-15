import socket
import time
from io import BytesIO
from threading import Thread, Lock

from app_usbodega import utils
from app_usbodega.graphql.subscription.ConvirtiendoCatalogoSubscription import ConvirtiendoCatalogoSubscription
from app_usbodega.graphql.subscription.PersonalNotificacionesSubscription import PersonalNotificacionesSubscription
from app_usbodega.models import Catalogos


class ClientTCP(Thread):
    def __init__(self, host, port, initial_message, user_id, file_name, dbfiles_out_replazable, uploaded_date,
                 callback=None):
        Thread.__init__(self)
        self.done = 0
        self.start_date = None
        self.total = None
        self.temp_count = 0
        self.temp_count_controller = 100
        self.temp_count_done = 0
        self.last_date_ended = None
        self.host = host
        self.port = port
        self.file_name = file_name
        self.dbfiles_out_replazable = dbfiles_out_replazable
        self.uploaded_date = uploaded_date
        self.user_id = user_id
        self.connected = False
        self.initial_message = initial_message
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(True)
        self.processing = False
        self.callback = callback

    def init_connection(self):
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
            return True
        except (ValueError, Exception) as e:
            print(e)
            pass
        return False

    def remaing(self):
        lc = Lock()
        while self.processing:
            lc.acquire()
            if not (self.total is None) and not (self.done == 0):
                last_date = self.last_date_ended
                start_date = self.start_date
                done = self.done
                total = self.total
                if not (done == 0) and not (total == 0):
                    if not (last_date is None) and not (start_date is None):
                        elapsed = last_date - start_date
                        remaing_timing = (((total - done) * elapsed) / done)
                        ConvirtiendoCatalogoSubscription.uploading_catalogo_status(self.user_id, done, total,
                                                                                   utils.segundos_a_formato(
                                                                                       remaing_timing),
                                                                                   "running")
                        time.sleep(1)
            lc.release()

    def proceso_(self, line):
        text = line.rstrip().decode("utf-8").replace("[PROGRESS]", "")
        # print("Linea recibida: {}".format(line.rstrip()))
        # print(text)
        if text == "@[JSONWriterEND]" or text == "@[CSVWriterEND]":
            self.processing = False
            ConvirtiendoCatalogoSubscription.uploading_catalogo_status(self.user_id, 0, 0,
                                                                       "",
                                                                       "")
            print("El proceso ha finalizado")
            catalogo = Catalogos(nameFile=self.file_name, file=self.dbfiles_out_replazable,
                                 date_uploaded=self.uploaded_date)
            catalogo.save()
            if not (self.callback is None):
                self.callback(True, self.user_id, self.dbfiles_out_replazable)
            PersonalNotificacionesSubscription.enviar_notificacion(self.user_id, "success",
                                                                   "El catálogo se ha terminado de convertir "
                                                                   "satisfactoriamente, "
                                                                   "ya puede reemplazarlo en el sistema actual")
            ConvirtiendoCatalogoSubscription.uploading_catalogo_status(self.user_id, 0, 0,
                                                                       "",
                                                                       "")
            self.connected = False
            return
        spliter = text.strip().split("/")
        done = spliter[0]
        total = spliter[1]
        if self.done == 0:
            self.total = int(total)
        self.last_date_ended = time.time()
        # self.last_date_ended = time.time()
        self.done = int(done)

    def send__initial_message(self):
        self.socket.sendall(str(self.initial_message).encode("utf-8"))

    def escuchar(self):
        PersonalNotificacionesSubscription.enviar_notificacion(self.user_id, "warning",
                                                               "El catálogo que se subio se está convirtiendo a "
                                                               "un formato "
                                                               "válido para el sistema por favor espere")
        self.send__initial_message()
        self.start_date = time.time()
        with BytesIO() as buffer:
            while self.connected:
                try:
                    resp = self.socket.recv(100)  # Read in some number of bytes -- balance this
                except (BlockingIOError, Exception) as e:
                    PersonalNotificacionesSubscription.enviar_notificacion(self.user_id, "error",
                                                                           "Se ha perdido la conexión con el servidor"
                                                                           "durante la conversión"
                                                                           "(intente nuevamente)")
                    print("Error producido por conexión: ", e)
                    time.sleep(1)
                    self.callback(False, self.user_id, self.dbfiles_out_replazable)
                    self.processing = False
                    self.connected = False
                else:
                    buffer.write(resp)
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
            self.processing = True
            Thread(target=self.remaing).start()
            Thread(target=self.escuchar()).start()
            return
        print("Error al conectar al servidor")
        if not (self.callback is None):
            self.callback(False, self.user_id, self.dbfiles_out_replazable)
        self.processing = False
        PersonalNotificacionesSubscription.enviar_notificacion(self.user_id, "error",
                                                               "No se pudo convertir el archivo, el servidor se "
                                                               "encuentra apagado (comuniquese con un administrador)")
