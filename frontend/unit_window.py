from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLineEdit,
                            QPushButton, QSizePolicy, QWidget, QMainWindow, QLabel, QApplication)
from backend import windows_util, initializers
from . import threading, debug_utils, game_manager
import sys

class UnitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.unit_window = initializers.qt["unit_window"]
            self.unit_window_res = self.unit_window["unit_window_res"]
        except KeyError as e:
            raise KeyError(f"Returned {e} when trying to get both unit window and unit window resolution.")
        self.center = windows_util.resolutionMid(self.unit_window_res[0], self.unit_window_res[1])
        self.setupWindow()
    

    def setupWindow(self):
        self.setWindowTitle("Unit Window")
        self.widget = QWidget()
        self.main_layout = QVBoxLayout(self.widget)
        self.setCentralWidget(self.widget)
        self.setGeometry(self.center[0], self.center[1], self.unit_window_res[0], self.unit_window_res[1])
        self.widget.setStyleSheet("background-color: #1b1b1f;")
        

        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        for i in range(3):
            unit_container = QWidget()
            unit_vbox = QVBoxLayout(unit_container)
            unit_hbox = QHBoxLayout()
            unit_hbox2 = QHBoxLayout()

            unit_container.setStyleSheet("""
                    background-color: #2b2b2f;
                    padding: 2px;
                """)

            label = QLabel()
            label.setText(f"Unit {i + 1}")
            label.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            "padding: 1px;"
                            )
            label.setAlignment(Qt.AlignCenter)
            unit_vbox.addWidget(label, alignment=Qt.AlignHCenter)
            unit_label = QLabel("Unit slot")
            unit_label.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
            text_input = QLineEdit()
            text_input.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
            text_input.setPlaceholderText(f"Slot for Unit {i + 1}")
            coordinates_label = QLabel("Unit Coordinates:")
            coordinates_label.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
            coordinates_input_x = QLineEdit()
            coordinates_input_x.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
            coordinates_input_y = QLineEdit()
            coordinates_input_y.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
            
            coordinates_place = QPushButton(text="Place")
            coordinates_place.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )

            unit_hbox.setSpacing(2)
            unit_hbox.setContentsMargins(0, 0, 0, 0)

            grab_slot = text_input.text()
            unit_hbox.addWidget(unit_label, alignment=Qt.AlignHCenter)
            unit_hbox.addWidget(text_input, alignment=Qt.AlignHCenter)
            unit_hbox2.addWidget(coordinates_label, alignment=Qt.AlignHCenter)
            unit_hbox2.addWidget(coordinates_input_x)
            unit_hbox2.addWidget(coordinates_input_y)
            unit_hbox2.addWidget(coordinates_place)


            unit_vbox.addLayout(unit_hbox)
            unit_vbox.addLayout(unit_hbox2)
            self.hbox1.addWidget(unit_container)


        self.main_layout.addLayout(self.hbox1)
        for i in range(3):
            unit_container = QWidget()
            unit_vbox = QVBoxLayout(unit_container)
            unit_hbox = QHBoxLayout()
            unit_hbox2 = QHBoxLayout()

            unit_container.setStyleSheet("""
                    background-color: #2b2b2f;
                    padding: 2px;
                """)

            label = QLabel(f"Unit {i + 3}")
            label.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            "padding: 1px;"
                            )
            label.setAlignment(Qt.AlignCenter)
            unit_vbox.addWidget(label, alignment=Qt.AlignHCenter)
            unit_label = QLabel("Unit slot")
            unit_label.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
            text_input = QLineEdit()
            text_input.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
            text_input.setPlaceholderText(f"Slot for Unit {i + 1}")

            coordinates_label = QLabel("Unit Coordinates:")
            coordinates_label.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
            coordinates_input_x = QLineEdit()
            coordinates_input_x.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
            coordinates_input_y = QLineEdit()
            coordinates_input_y.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
            coordinates_place = QPushButton(text="Place")
            coordinates_place.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )

            unit_hbox.setSpacing(2)
            unit_hbox.setContentsMargins(0, 0, 0, 0)

            grab_slot = text_input.text()
            unit_hbox.addWidget(unit_label, alignment=Qt.AlignHCenter)
            unit_hbox.addWidget(text_input, alignment=Qt.AlignHCenter)
            unit_hbox2.addWidget(coordinates_label, alignment=Qt.AlignHCenter)
            unit_hbox2.addWidget(coordinates_input_x)
            unit_hbox2.addWidget(coordinates_input_y)
            unit_hbox2.addWidget(coordinates_place)


            unit_vbox.addLayout(unit_hbox)
            unit_vbox.addLayout(unit_hbox2)
            self.hbox2.addWidget(unit_container)
        self.main_layout.addLayout(self.hbox2)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UnitWindow()
    window.show()
    sys.exit(app.exec_())