from cogs.Worker import Worker
from PyQt5.QtWidgets import  QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QCoreApplication, pyqtSignal, QThread


class Window(QMainWindow):
    stop_signal = pyqtSignal()

    def __init__(self):
        super(Window, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Host")
        self.setGeometry(250, 300, 250, 300)
        layout = QVBoxLayout()
        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)
        self.label_status = QLabel('To start host push the button')
        self.label_connection = QLabel("")

        btn_start = QPushButton("Open Connection")
        btn_stop = QPushButton("Close Connection")
        btn_quit = QPushButton("Close Application")

        btn_start.clicked.connect(self.open_connection)
        btn_stop.clicked.connect(self.close_connection)
        btn_quit.clicked.connect(QCoreApplication.instance().quit)

        layout.addWidget(self.label_status)
        layout.addWidget(self.label_connection)
        layout.addWidget(btn_start)
        layout.addWidget(btn_stop)
        layout.addWidget(btn_quit)

        self.centralWidget.setLayout(layout)

    def report_progress(self, n):
        self.label_connection.setText(f"Button pressed: {n}")

    def open_connection(self):
        self.thread = QThread()
        self.connection = Worker()
        self.stop_signal.connect(self.connection.stop)
        self.connection.moveToThread(self.thread)
        self.thread.started.connect(self.connection.run)

        self.connection.finished.connect(self.thread.quit)
        self.connection.finished.connect(self.connection.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.connection.button.connect(self.report_progress)

        self.thread.start()
        self.label_status.setText("To close connection click button")
        self.thread.finished.connect(
            lambda: self.label_connection.setText("Disconnected")
        )

    def close_connection(self):
        self.stop_signal.emit()  # emit the finished signal on stop
        self.label_status.setText("Push button to start host again")
        self.label_connection.setText("Connection Terminated")
