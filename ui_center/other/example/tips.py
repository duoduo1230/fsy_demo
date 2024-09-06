import sys
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Window")
        self.setGeometry(100, 100, 400, 200)  # Set window size

        # Create a horizontal layout for the top row
        top_layout = QHBoxLayout()

        # Add an image (replace 'image.jpg' with your actual image path)
        pixmap = QPixmap("image.jpg")
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        top_layout.addWidget(image_label)

        # Add two labels
        label1 = QLabel("Created successfully")
        label2 = QLabel("Another label")
        top_layout.addWidget(label1)
        top_layout.addWidget(label2)

        # Create a horizontal layout for the bottom row
        bottom_layout = QHBoxLayout()

        # Add a button to close the window
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        bottom_layout.addWidget(close_button)

        # Create a vertical layout to arrange the top and bottom rows
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        # Set the main layout for the window
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
