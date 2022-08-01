from cogs.Worker import Worker
from PyQt5.QtWidgets import  QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QCoreApplication, pyqtSignal, QThread

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
        self.label_connection.setText(f"Button pressed: {n}")

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
            lambda: self.label_connection.setText("Disconnected")
        )

    def close_connection(self):
        self.stop_signal.emit()  # emit the finished signal on stop
        self.label_status.setText("Push button to start host again")
        self.label_connection.setText("Connection Terminated")