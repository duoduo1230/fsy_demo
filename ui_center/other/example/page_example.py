from PySide2 import QtGui
from PySide2 import QtWidgets


def createIntroPage():
    page = QtWidgets.QWizardPage()
    page.setTitle("Introduction")

    label = QtWidgets.QLabel("This wizard will help you register your copy of "
            "Super Product Two.")
    label.setWordWrap(True)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page


def createRegistrationPage():
    page = QtWidgets.QWizardPage()
    page.setTitle("Registration")
    page.setSubTitle("Please fill both fields.")

    nameLabel = QtWidgets.QLabel("Name:")
    nameLineEdit = QtWidgets.QLineEdit()

    emailLabel = QtWidgets.QLabel("Email address:")
    emailLineEdit = QtWidgets.QLineEdit()

    layout = QtWidgets.QGridLayout()
    layout.addWidget(nameLabel, 0, 0)
    layout.addWidget(nameLineEdit, 0, 1)
    layout.addWidget(emailLabel, 1, 0)
    layout.addWidget(emailLineEdit, 1, 1)
    page.setLayout(layout)

    return page


def createConclusionPage():
    page = QtWidgets.QWizardPage()
    page.setTitle("Conclusion")

    label = QtWidgets.QLabel("You are now successfully registered. Have a nice day!")
    label.setWordWrap(True)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page


def backprint():
    print("Action: back Page: " + wizard.currentPage().title())

def nextprint():
    print("Action: next Page: " + wizard.currentPage().title())

def commitprint():
    print("Action: commit Page: " + wizard.currentPage().title())

def finishprint():
    print("Action:finish Page: " + wizard.currentPage().title())

def cancelprint():
    print("Action:cancel Page: " + wizard.currentPage().title())

if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)

    wizard = QtWidgets.QWizard()

    wizard.addPage(createIntroPage())
    wizard.addPage(createRegistrationPage())
    wizard.addPage(createConclusionPage())

    wizard.button(QtWidgets.QWizard.BackButton).clicked.connect(backprint)
    wizard.button(QtWidgets.QWizard.NextButton).clicked.connect(nextprint)
    wizard.button(QtWidgets.QWizard.CommitButton).clicked.connect(commitprint)
    wizard.button(QtWidgets.QWizard.FinishButton).clicked.connect(finishprint)
    wizard.button(QtWidgets.QWizard.CancelButton).clicked.connect(cancelprint)

    wizard.setWindowTitle("Trivial Wizard")
    wizard.show()
    print("Page :" + wizard.currentPage().title())

    sys.exit(wizard.exec_())