from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
import sys
import json
from datetime import datetime

# Enable High DPI display
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

class ModernBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Python Browser')
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize storage
        self.history = {}
        self.bookmarks = {}
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create navigation bar
        navbar = QToolBar()
        navbar.setMovable(False)
        self.addToolBar(navbar)

        # New Tab button
        new_tab_btn = QToolButton()
        new_tab_btn.setText('+')
        new_tab_btn.clicked.connect(lambda: self.add_new_tab())
        navbar.addWidget(new_tab_btn)

        # Back button
        back_btn = QToolButton()
        back_btn.setText('←')
        back_btn.clicked.connect(lambda: self.current_tab().back())
        navbar.addWidget(back_btn)

        # Forward button
        forward_btn = QToolButton()
        forward_btn.setText('→')
        forward_btn.clicked.connect(lambda: self.current_tab().forward())
        navbar.addWidget(forward_btn)

        # Reload button
        reload_btn = QToolButton()
        reload_btn.setText('↻')
        reload_btn.clicked.connect(lambda: self.current_tab().reload())
        navbar.addWidget(reload_btn)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Menu button
        menu_btn = QToolButton()
        menu_btn.setText('☰')
        
        # Create menu
        menu = QMenu()
        
        # Themes submenu
        themes_menu = menu.addMenu('Themes')
        dark_theme = themes_menu.addAction('Dark Theme')
        dark_theme.triggered.connect(self.set_dark_theme)
        light_theme = themes_menu.addAction('Light Theme')
        light_theme.triggered.connect(self.set_light_theme)
        
        menu_btn.setMenu(menu)
        navbar.addWidget(menu_btn)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        layout.addWidget(self.tabs)

        # Add initial tab
        self.add_new_tab()
        
        # Set default theme
        self.set_dark_theme()

    def add_new_tab(self, qurl=None):
        if qurl is None:
            qurl = QUrl('https://www.google.com')
        elif isinstance(qurl, bool):  # Fix for signal handling
            qurl = QUrl('https://www.google.com')
            
        browser = QWebEngineView()
        browser.setUrl(qurl)
        
        i = self.tabs.addTab(browser, 'New Tab')
        self.tabs.setCurrentIndex(i)
        
        browser.urlChanged.connect(lambda qurl, browser=browser:
            self.update_url_bar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
            self.tabs.setTabText(i, browser.page().title()))

    def current_tab(self):
        return self.tabs.currentWidget()

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)
        else:
            self.current_tab().setUrl(QUrl('https://www.google.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'https://www.google.com/search?q=' + url
        self.current_tab().setUrl(QUrl(url))

    def update_url_bar(self, q, browser=None):
        if browser != self.current_tab():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def set_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget { 
                background: #2b2b2b; 
                color: #ffffff; 
            }
            QTabBar::tab { 
                background: #363636; 
                color: #ffffff;
                padding: 8px;
                min-width: 100px;
            }
            QTabBar::tab:selected { 
                background: #454545; 
            }
            QToolBar { 
                background: #363636;
                border: none;
                padding: 5px;
            }
            QToolButton { 
                background: #454545;
                color: #ffffff;
                border: none;
                padding: 5px;
                margin: 2px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background: #505050;
            }
            QLineEdit { 
                background: #454545;
                color: #ffffff;
                border: none;
                padding: 5px;
                border-radius: 4px;
            }
            QMenu {
                background: #363636;
                color: #ffffff;
                border: 1px solid #505050;
            }
            QMenu::item:selected {
                background: #505050;
            }
        """)

    def set_light_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget { 
                background: #ffffff; 
                color: #000000; 
            }
            QTabBar::tab { 
                background: #f0f0f0; 
                color: #000000;
                padding: 8px;
                min-width: 100px;
            }
            QTabBar::tab:selected { 
                background: #e0e0e0; 
            }
            QToolBar { 
                background: #f0f0f0;
                border: none;
                padding: 5px;
            }
            QToolButton { 
                background: #e0e0e0;
                color: #000000;
                border: none;
                padding: 5px;
                margin: 2px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background: #d0d0d0;
            }
            QLineEdit { 
                background: #f0f0f0;
                color: #000000;
                border: 1px solid #d0d0d0;
                padding: 5px;
                border-radius: 4px;
            }
            QMenu {
                background: #ffffff;
                color: #000000;
                border: 1px solid #d0d0d0;
            }
            QMenu::item:selected {
                background: #e0e0e0;
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ModernBrowser()
    window.show()
    sys.exit(app.exec_())
