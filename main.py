import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QCoreApplication, QObject, pyqtSignal, QThread


# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    button = pyqtSignal(int)

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self.continue_run = True  # provide a bool run condition for the class

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '192.168.155.213'  # ip of host
        port = 12345
        server.bind((host, port))
        server.listen(5)
        c, addr = server.accept()
        print('Got connection from', addr)
        while self.continue_run:
            print("Button pushed")
            client_message, _ = c.recvfrom(4096)
            print(client_message)
            if client_message == b'1':
                self.button.emit(1)
            elif client_message == b'0':
                self.button.emit(0)
            elif client_message == b'close' or not self.continue_run:
                server.close()
                self.finished.emit()
                print("Finished")
                break
        self.finished.emit()
        server.close()
        print("Finished")

    def stop(self):
        self.continue_run = False


class Window(QMainWindow):
    stop_signal = pyqtSignal()

    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Host")
        layout = QVBoxLayout()
        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)
        self.label_status = QLabel('To start host push the button')
        self.label_connection = QLabel("")

        btnStart = QPushButton("Open Connection")
        btnStop = QPushButton("Close Connection")
        btnQuit = QPushButton("Close Application")

        btnStart.clicked.connect(self.open_connection)
        btnStop.clicked.connect(self.close_connection)
        btnQuit.clicked.connect(QCoreApplication.instance().quit)

        layout.addWidget(self.label_status)
        layout.addWidget(self.label_connection)
        layout.addWidget(btnStart)
        layout.addWidget(btnStop)
        layout.addWidget(btnQuit)

        self.centralWidget.setLayout(layout)

    def reportProgress(self, n):
        if n == 1:
            self.label_connection.setText(f"Button pressed: {n}")
        else:
            self.label_connection.setText(f"Button not  pressed: {n}")

    def open_connection(self):
        self.label_status.setText("To close connection click button")
        self.thread = QThread()
        self.connection = Worker()
        self.stop_signal.connect(self.connection.stop)
        self.connection.moveToThread(self.thread)
        self.thread.started.connect(self.connection.run)

        self.connection.finished.connect(self.thread.quit)
        self.connection.finished.connect(self.connection.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.connection.button.connect(self.reportProgress)

        self.thread.start()
        self.thread.finished.connect(
            lambda: self.label_connection.setText("Button NOT Pressed")
        )

    def close_connection(self):
        self.stop_signal.emit()  # emit the finished signal on stop
        self.label_status.setText("Push button to start host again")
        self.label_connection.setText("Connection Terminated")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Window()
    main_window.show()
    sys.exit(app.exec_())
