import sys
import json
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
from PyQt5 import QtWebEngineWidgets

from ipyleaflet import Map, Marker, LayersControl, basemaps
from ipywidgets import HTML, IntSlider
from ipywidgets.embed import embed_data


class MapWindow(QWidget):
    def __init__(self, base_coords):
        self.base_coords = base_coords
        super().__init__()
        self.layout = QVBoxLayout()
        self.title = QLabel("<b>Another Map Example</b>")
        self.layout.addWidget(self.title)

        self.web = QtWebEngineWidgets.QWebEngineView(self)

        s1 = IntSlider(max=200, value=100)
        s2 = IntSlider(value=40)

        self.map = Map(center=self.base_coords,
                       basemaps=basemaps.Esri.WorldTopoMap, zoom=10)

        self.marker = Marker(location=self.base_coords)
        self.marker.popup = HTML(value='Marker')
        self.map.add_layer(self.marker)

        data = embed_data(views=[s1, s2, self.map])

        html_template = """
        <html>
          <head>
            <title>Widget</title>
            <script 
              src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js" 
              integrity="sha256-Ae2Vz/4ePdIu6ZyI/5ZGsYnb+m0JlOmKPjt6XZ9JJkA=" 
              crossorigin="anonymous">
            </script>
            <script
              data-jupyter-widgets-cdn="https://cdn.jsdelivr.net/npm/"
              src="https://unpkg.com/@jupyter-widgets/html-manager@*/dist/embed-amd.js" 
              crossorigin="anonymous">
            </script>
            <script type="application/vnd.jupyter.widget-state+json">
              {manager_state}
            </script>
          </head>
          <body>
            <h1>Widget</h1>
            <div id="first-slider-widget">
              <!-- This script tag will be replaced by the view's DOM tree -->
              <script type="application/vnd.jupyter.widget-view+json">
                {widget_views[0]}
              </script>
            </div>
            <hrule />
            <div id="second-slider-widget">
              <!-- This script tag will be replaced by the view's DOM tree -->
              <script type="application/vnd.jupyter.widget-view+json">
                {widget_views[1]}
              </script>
            </div>
            <!-- The ipyleaflet map -->
            <div id="ipyleaflet-map">
                <script type="application/vnd.jupyter.widget-view+json">
                    {widget_views[2]}
                </script>
            </div>
          </body>
        </html>
        """

        manager_state = json.dumps(data['manager_state'])
        widget_views = [json.dumps(view) for view in data['view_specs']]
        rendered_template = html_template.format(
            manager_state=manager_state, widget_views=widget_views)
        self.web.setHtml(rendered_template)
        self.layout.addWidget(self.web)
        self.setLayout(self.layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    base_coords = [40.76358185278211, 29.90650776805874]
    widget = MapWindow(base_coords)
    widget.resize(900, 800)
    sys.exit(app.exec_())
