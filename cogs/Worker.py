import socket
from PyQt5.QtCore import QObject, pyqtSignal, QThread

from PyQt5.QtCore import  pyqtSignal


class Worker(QObject):
    finished = pyqtSignal()
    button = pyqtSignal(int)

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self.continue_run = True  # provide a bool run condition for the class

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'  # ip of host
        port = 12345
        server.bind((host, port))
        server.listen(5)
        c, addr = server.accept()
        print('Got connection from', addr)
        switch = {b'1': 1,
                  b'0': 0}
        while self.continue_run:
            client_message, _ = c.recvfrom(4096)
            print(client_message)
            try:
                self.button.emit(switch[client_message])
            except KeyError:
                self.button.emit(1)
            if client_message == b'close' or not self.continue_run:
                self.finished.emit()
                break
        self.finished.emit()
        server.close()
        print("Finished")

    def stop(self):
        self.continue_run = False
