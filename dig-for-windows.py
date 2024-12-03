import sys
import os
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QLineEdit, QPushButton, 
                             QTextEdit, QLabel)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QPalette, QColor
import dns.resolver
import dns.rdatatype

class DNSLookupWorker(QThread):
    result_ready = Signal(str)
    error_occurred = Signal(str)
    
    def __init__(self, domain, record_type, nameserver):
        super().__init__()
        self.domain = domain
        self.record_type = record_type
        self.nameserver = nameserver
        
    def run(self):
        try:
            resolver = dns.resolver.Resolver()
            
            # Set custom nameserver if selected
            if self.nameserver:
                resolver.nameservers = [self.nameserver]
                
            answers = resolver.resolve(self.domain, self.record_type)
            
            result = f"\nQuery Results for {self.domain} ({self.record_type}):\n"
            result += "=" * 50 + "\n"
            
            for rdata in answers:
                result += f"{rdata}\n"
                
            self.result_ready.emit(result)
            
        except Exception as e:
            self.error_occurred.emit(f"Error: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("dig-for-windows")
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1920, 1080)
        self.resize(1280, 720)

        # Load settings and initialize the UI
        self.load_settings()
        self.setup_ui()
        
        # Load settings
        self.load_settings()
        self.update_theme()
        
    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Theme switch
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_switch = QPushButton("Toggle Dark/Light Mode")
        self.theme_switch.clicked.connect(self.toggle_theme)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_switch)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)
        
        # DNS server selection
        ns_layout = QHBoxLayout()
        ns_label = QLabel("Nameserver:")
        self.ns_combo = QComboBox()
        self.setup_nameservers()
        ns_layout.addWidget(ns_label)
        ns_layout.addWidget(self.ns_combo)
        layout.addLayout(ns_layout)
        
        # Domain input
        domain_layout = QHBoxLayout()
        domain_label = QLabel("Domain:")
        self.domain_input = QLineEdit()
        domain_layout.addWidget(domain_label)
        domain_layout.addWidget(self.domain_input)
        layout.addLayout(domain_layout)
        
        # Record type selection
        record_layout = QHBoxLayout()
        record_label = QLabel("Record Type:")
        self.record_combo = QComboBox()
        self.setup_record_types()
        record_layout.addWidget(record_label)
        record_layout.addWidget(self.record_combo)
        layout.addLayout(record_layout)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Lookup button
        self.lookup_button = QPushButton("Lookup")
        self.lookup_button.clicked.connect(self.perform_lookup)
        button_layout.addWidget(self.lookup_button)
        
        # Clear button
        self.clear_button = QPushButton("Clear Log")
        self.clear_button.clicked.connect(self.clear_log)
        button_layout.addWidget(self.clear_button)
        
        # Add button layout to main layout
        layout.addLayout(button_layout)
        
        # Results area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)
        
    def setup_nameservers(self):
        nameservers = {
            "System Default": "",
            "Cloudflare (1.1.1.1)": "1.1.1.1",
            "Google (8.8.8.8)": "8.8.8.8",
            "Hetzner - (helium.ns.hetzner.de)": "193.47.99.5",
            "Hetzner - (oxygen.ns.hetzner.com)": "88.198.229.192",
            "Hetzner - (hydrogen.ns.hetzner.com)": "213.133.100.98",
            "Quad9 (9.9.9.9)": "9.9.9.9"
        }
        
        for name, server in nameservers.items():
            self.ns_combo.addItem(name, server)
            
    def setup_record_types(self):
        record_types = [
            "A", "AAAA", "ANY", "CAA", "CNAME", "DNSKEY",
            "DS", "MX", "NS", "PTR", "SOA", "SRV", "TLSA", "TSIG", "TXT"
        ]
        
        for record_type in record_types:
            self.record_combo.addItem(record_type)
            
    def perform_lookup(self):
        domain = self.domain_input.text().strip()
        if not domain:
            self.results_text.setText("Please enter a domain name!")
            return
            
        record_type = self.record_combo.currentText()
        nameserver = self.ns_combo.currentData()
        
        self.lookup_button.setEnabled(False)
        self.results_text.append(f"\nQuerying {domain}...")
        
        self.worker = DNSLookupWorker(domain, record_type, nameserver)
        self.worker.result_ready.connect(self.handle_result)
        self.worker.error_occurred.connect(self.handle_error)
        self.worker.finished.connect(lambda: self.lookup_button.setEnabled(True))
        self.worker.start()
        
    def handle_result(self, result):
        self.results_text.append(result)
        
    def handle_error(self, error):
        self.results_text.append(error)
        
    def clear_log(self):
        self.results_text.clear()
        
    def load_settings(self):
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.settings_file = os.path.join(script_dir, "settings.json")
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.dark_mode = settings.get('dark_mode', True)  # Default to dark mode
            else:
                self.dark_mode = True  # Default to dark mode
        except Exception:
            self.dark_mode = True  # Default to dark mode if any error occurs
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump({'dark_mode': self.dark_mode}, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()
        self.save_settings()
        
    def update_theme(self):
        app = QApplication.instance()
        palette = QPalette()
        
        if self.dark_mode:
            # Dark theme colors
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            # Light theme colors with better contrast
            palette.setColor(QPalette.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
            palette.setColor(QPalette.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.Button, QColor(230, 230, 230))
            palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Link, QColor(0, 0, 255))
            palette.setColor(QPalette.Highlight, QColor(51, 153, 255))
            palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
            
        app.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())