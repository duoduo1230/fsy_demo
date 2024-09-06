import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QDateEdit, QVBoxLayout, QWidget
from PySide2.QtCore import QDate

class DateEditExample(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a QMainWindow with a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a QVBoxLayout to hold the QDateEdit widget
        layout = QVBoxLayout(central_widget)

        # Create a QDateEdit widget and set its date to today
        date_edit = QDateEdit(QDate.currentDate())
        date_edit.setDisplayFormat("yyyy.MM.dd")  # Set the display format

        # Restrict the valid date range to today plus or minus 365 days
        date_edit.setMinimumDate(QDate.currentDate().addDays(-365))
        date_edit.setMaximumDate(QDate.currentDate().addDays(365))

        # Add the QDateEdit widget to the layout
        layout.addWidget(date_edit)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DateEditExample()
    window.show()
    sys.exit(app.exec_())
