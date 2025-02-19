import mediapipe as mp

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import (QCoreApplication, Qt , QSize, pyqtSignal,QDate,QTimer)
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
    QHBoxLayout, QGridLayout, QLineEdit, QMessageBox, QGroupBox, QSpacerItem, QStackedWidget,QMainWindow)
from PyQt6.QtGui import QIcon,QImage, QMouseEvent, QFontDatabase, QFont


from components.formLogin import FormLogin
from imageTitle import ImageTitle
from utils.messageBox import showMessageBox
from database.database import Database
from createAccountPage import CreateAccountPage
from controlPage import ControlPage
from editPage import EditPage
from detailPage import DetailPage
from processPage import ProcessPage
from utils.logger import AppLogger


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hand Hygiene Testing")
        self.setWindowIcon(QIcon("mainWindow.png"))
        self.setFixedSize(QSize(1024, 768))
        self.setStyleSheet("background-color: #B4B4B4;")

        # StepUp Logger
        self.logger = AppLogger().get_logger()
        
        # Root Layout
        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(vBox)

        # LoginPage Widget
        self.loginPageWidget = QWidget()
        loginPageVBox = QVBoxLayout()
        loginPageVBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loginPageWidget.setLayout(loginPageVBox)

        # Title
        self.titleLoginLabel = QLabel('Hand Hygiene Testing')
        self.titleLoginLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.titleLoginLabel.setStyleSheet(
            '''
                font-size: 30px;
                font-weight: bold;
            '''
        )
        loginPageVBox.addWidget(self.titleLoginLabel)

        # Center layout
        hBoxCenter = QHBoxLayout()
        hBoxCenter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loginPageVBox.addLayout(hBoxCenter)

        # Image Title
        self.imageTitle = ImageTitle()
        hBoxCenter.addWidget(self.imageTitle, alignment=Qt.AlignmentFlag.AlignCenter)

        # FormLogin UI
        self.formLogin = FormLogin()
        hBoxCenter.addWidget(self.formLogin, alignment=Qt.AlignmentFlag.AlignCenter)

        # Stack Widget ----------------------------------------------------------------------------------
        self.stackedWidget = QStackedWidget()
         # Add LoginPage and CreateAccountPage to QStackedWidget
        self.stackedWidget.addWidget(self.loginPageWidget)

        # Create Account Page
        self.createAccountPage = CreateAccountPage(self.stackedWidget)
        self.stackedWidget.addWidget(self.createAccountPage)

        # Control Page
        self.controlPage = ControlPage(self.stackedWidget)
        self.stackedWidget.addWidget(self.controlPage)

        # Edit Page
        self.editPage = EditPage(self.stackedWidget)
        self.stackedWidget.addWidget(self.editPage)

        # Detail Page
        self.detailPage = DetailPage(self.stackedWidget)
        self.stackedWidget.addWidget(self.detailPage)

        # progress Page
        self.processPage = ProcessPage(self.stackedWidget)
        self.stackedWidget.addWidget(self.processPage)

        # Set LoginPage as the initial widget
        # self.stackedWidget.setCurrentWidget(self.controlPage)
        # self.stackedWidget.setCurrentWidget(self.detailPage)
        # for 5test
        # self.stackedWidget.setCurrentWidget(self.editPage)
        # self.stackedWidget.setCurrentWidget(self.controlPage)


        vBox.addWidget(self.stackedWidget)

        # ------------------------------------------------------------------------------------------

        # Logic --------------------------------------------------------------------------------------

        # Get UserInput instance
        self.formLogin.getUserInput().textChanged.connect(self.onUserInputChanged)
        # Get PasswordInput instance
        self.formLogin.getPasswordInput().textChanged.connect(self.onPasswordInputChanged)

        # Get signUpBtn instance
        self.formLogin.getSignUpBtn().clicked.connect(self.submitLogin)

        # Get instance of LableToPageRegister
        self.formLogin.getLableToCreateAccountPage().mousePressEvent = self.onClickToCreateAccount

    # Database ------------------------------------------------------------------------------------
        self.db = Database()

    # Event -------------------------------------------------------------------------------------
        self.adminLogin = {
            'username' : '',
            'password' : ''
        }
        

    # Keyboard Event 
    def keyPressEvent(self, event):
        if self.stackedWidget.currentIndex() == 0:
            if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                print("Enter key pressed")
                self.submitLogin()


    def onClickToCreateAccount(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.stackedWidget.setCurrentWidget(self.createAccountPage)  # Switch to CreateAccountPage
            print('Clicked Register label')

    # Get username
    def onUserInputChanged(self, text):
        print(f"Username changed to: {text}")
        self.adminLogin['username'] = text

    # Get password
    def onPasswordInputChanged(self, text):
        print(f"Password changed to: {text}")
        self.adminLogin['password'] = text

    # Submit Login
    def submitLogin(self):
        # Check Login in SQLite; return True when login is successful
        loginStatus = self.db.checkLogin(self.adminLogin)

        if loginStatus:
            showMessageBox(title='Login', topic='Login Success')  # Message Box
            self.stackedWidget.setCurrentWidget(self.controlPage) 
            self.logger.info(f"Login Success username : {self.adminLogin['username']}") # Log
        
        else:
            showMessageBox(title='Login', topic='Login Fail',mode='error')  # Message Box
            self.logger.info(f"Login Unsuccess username : {self.adminLogin['username']}") # Log
        
        # print(f"Login username: {self.adminLogin['username']} password: {self.adminLogin['password']}")

    # def closeEvent(self, event):
    #     msg_box = QMessageBox(self)
    #     msg_box.setWindowTitle("Exit Confirmation")
    #     msg_box.setText("Are you sure you want to exit?")
    #     msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    #     msg_box.setDefaultButton(QMessageBox.StandardButton.No)

    #     # ✅ กำหนด CSS ให้กับ QMessageBox
    #     msg_box.setStyleSheet("""
    #         QMessageBox {
    #             background-color: #FFFFFFFF;  /* เปลี่ยนสีพื้นหลัง */
    #             color: white;  /* เปลี่ยนสีตัวอักษร */
    #             font-size: 16px;
    #         }
    #         QPushButton {
    #             background-color: #1C8CDB;
    #             color: white;
    #             font-size: 14px;
    #             padding: 6px 12px;
    #             border-radius: 4px;
    #         }
    #         QPushButton:hover {
    #             background-color: #1476B3;
    #         }
    #         QPushButton:pressed {
    #             background-color: #0F5C91;
    #         }
    #         QLabel{
    #             background-color: transparent;
    #         }
    #     """)

    #     reply = msg_box.exec()

    #     if reply == QMessageBox.StandardButton.Yes:
    #         print("Program is closing...")
    #         event.accept()
    #     else:
    #         event.ignore()

if __name__ == "__main__":
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication([])

    font_id = QFontDatabase.addApplicationFont("font/NotoSans-Regular.ttf")
    font_families = QFontDatabase.applicationFontFamilies(font_id)

    if font_families:
        app.setFont(QFont(font_families[0])) 
    else:
        app.setFont(QFont("Arial"))  

    window = LoginPage()
    window.show()
    app.exec()