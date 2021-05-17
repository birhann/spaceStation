import sys
import io
import random
import time
import folium  # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine

    
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        for i in range(5):
            x = random.uniform(40.6, 40.8)
            y= random.uniform(29.8, 30.0)
            time.sleep(10)
            print(x,y)

            m = folium.Map(
                tiles='cartodbpositron',
                zoom_start=14,
                location=(x,y),
                
            )
            folium.Marker(location=(x,y),popup='Uydu').add_to(m)
            # save map data to data object
            data = io.BytesIO()
            m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)
    
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
