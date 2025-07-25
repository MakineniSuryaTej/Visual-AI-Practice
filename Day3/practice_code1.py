import threading
import keyboard
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QLabel, QLineEdit, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer
from vision_core import screenshot, ask_gemini 

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_hotkey_listener()
    
    def start_hotkey_listener(self):
        def listen():
            print("Hotkey listener started")
            keyboard.add_hotkey('ctrl+shift+a', self.safe_trigger)
            keyboard.wait()

        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
    
    def safe_trigger(self):
        QTimer.singleShot(0, self.trigger_analysis)

    def init_ui(self):
        self.setWindowTitle("AI Assistant")
        self.setGeometry(100, 100, 600, 600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()

        self.question_input = QLineEdit(self)
        self.question_input.setPlaceholderText("What do you want to ask about your screen?")
        layout.addWidget(self.question_input)

        self.ask_button = QPushButton("Analyze Screen", self)
        self.ask_button.clicked.connect(self.handle_ask)
        layout.addWidget(self.ask_button)

        self.response_area = QTextEdit(self)
        self.response_area.setReadOnly(True)
        layout.addWidget(self.response_area)

        self.setLayout(layout)
    
    def handle_ask(self):
        question = self.question_input.text().strip()
        if not question:
            QMessageBox.warning(self, "Input Error", "Please enter a question.")
            return
        
        self.response_area.setText("Capturing screen and thinking...")
        try:
            image_path = screenshot()
            response = ask_gemini(image_path, question)
            self.response_area.setText(response)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.response_area.setText("Failed to get a response.")
    
    def trigger_analysis(self):
        question = self.question_input.text().strip()
        if not question:
            question = "What is in this screenshot? Summarize it in 2 sentences."

        self.response_area.setText("Hotkey triggered. Capturing screen...")
        try:
            image_path = screenshot()
            response = ask_gemini(image_path, question)
            self.response_area.setText(response)
            self.activateWindow()
        except Exception as e:
            self.response_area.setText(f"Error: {str(e)}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())