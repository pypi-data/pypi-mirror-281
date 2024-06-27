import subprocess
import os
import sys
import json
from pathlib import Path
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QWidget, QComboBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QUrl

class ArchBrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("crl-browser - Search Engine")
        self.setGeometry(100, 100, 800, 600)
        self.crlnet_directory = str(Path.home())

        self.db_connection = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.language_combo_box = QComboBox()
        self.language_combo_box.addItems(["English", "Turkish"])
        self.language_combo_box.currentIndexChanged.connect(self.change_language)
        self.layout.addWidget(self.language_combo_box)

        self.instruction_text_edit = QTextEdit()
        self.instruction_text_edit.setReadOnly(True)
        self.instruction_text_edit.setStyleSheet("background-color: black; color: #00FFFF;")
        self.instruction_text_edit.setFont(QFont("Courier", 10))
        self.instruction_text_edit.append(self.tr("Welcome! You can search 'crl://' sites from here."))
        self.layout.addWidget(self.instruction_text_edit)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setStyleSheet("background-color: black; color: #00FFFF;")
        self.search_input.setFont(QFont("Courier", 10))
        self.layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("background-color: black; color: #00FFFF;")
        self.search_button.clicked.connect(self.search_sites)
        self.layout.addWidget(self.search_button)

        self.ddns_button = QPushButton("DDNS Manager")
        self.ddns_button.clicked.connect(self.ddns_manager)
        self.layout.addWidget(self.ddns_button)

        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)

        self.connect_to_database()

    def connect_to_database(self):
        try:
            # Assuming ddns.bin is responsible for database connection
            self.db_connection = subprocess.Popen(['./database'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            print("Database connection established successfully.")
        except Exception as e:
            print("Error connecting to database with ddns.bin:", e)
            self.db_connection = None

    def ddns_manager(self):
        try:
            subprocess.run([sys.executable, "ddns.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to run ddns.py: {e}")

    def search_sites(self):
        if self.db_connection is None:
            print("Database connection is not established.")
            return

        search_term = self.search_input.text().strip().lower()
        self.instruction_text_edit.clear()
        self.instruction_text_edit.append(f"Searching for '{search_term}'...")

        try:
            # Example of using ddns.bin for database query
            query_result = self.db_connection.communicate(input=f"SELECT name FROM domains WHERE name ILIKE '%{search_term}%'".encode())
            found_sites = query_result[0].decode().strip().split('\n')

            if found_sites:
                self.instruction_text_edit.append("Results found:")
                for site in found_sites:
                    self.instruction_text_edit.append(site)
                    self.load_and_display_site(site)
            else:
                self.instruction_text_edit.append("No results found.")
        except Exception as e:
            print("Error querying database with ddns.bin:", e)

    def load_and_display_site(self, site_name):
        try:
            # Example of using ddns.bin for database query
            query_result = self.db_connection.communicate(input=f"SELECT ip_address FROM domains WHERE name = '{site_name}'".encode())
            ip_address = query_result[0].decode().strip()

            if ip_address:
                url = f"http://{ip_address}/{site_name}"
                self.web_view.load(QUrl(url))

                site_content = self.get_site_content(site_name)
                if not site_content:
                    self.display_site_content("No site content available.")
        except Exception as e:
            print("Error querying database with ddns.bin:", e)

    def get_site_content(self, site_name):
        try:
            # Example of using requests to fetch site content
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT ip_address FROM domains WHERE name = %s", (site_name,))
            ip_address = cursor.fetchone()
            cursor.close()

            if ip_address:
                url = f"http://{ip_address[0]}/{site_name}"

                response = requests.get(url)
                if response.status_code == 200:
                    return response.text
                else:
                    print(f"HTTP Error {response.status_code}: {response.reason}")
        except Exception as e:
            print("Error fetching site content:", e)

        return None

    def display_site_content(self, content):
        self.instruction_text_edit.append("Site Content:")
        self.instruction_text_edit.append(content)

    def save_search_term(self, search_term):
        search_terms_file = os.path.join(self.crlnet_directory, "search_terms.json")
        if os.path.exists(search_terms_file):
            with open(search_terms_file, "r") as file:
                search_terms = json.load(file)
        else:
            search_terms = []

        search_terms.append(search_term)

        with open(search_terms_file, "w") as file:
            json.dump(search_terms, file)

    def load_user_info(self):
        if os.path.exists(self.user_info_file):
            with open(self.user_info_file, "r") as file:
                self.user_info = json.load(file)
        else:
            self.user_info = {}

    def change_language(self):
        language = self.language_combo_box.currentText()
        if language == "English":
            self.translator.load("translations/en.qm")
        elif language == "Turkish":
            self.translator.load("translations/tr.qm")
        QApplication.instance().installTranslator(self.translator)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArchBrowserWindow()
    window.show()
    sys.exit(app.exec())
