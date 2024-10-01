import itertools
import random

from qgis._core import QgsWkbTypes, QgsFeature, QgsGeometry
from qgis._gui import QgsRubberBand
from qgis.core import QgsVectorLayer

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from qgis.utils import iface
from qgis.core import QgsRasterLayer, QgsProject


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('QGIS Script runner')

        self.layout = QVBoxLayout()

        self.button1 = QPushButton('Run a configuration')
        self.button1.clicked.connect(self.run_button)

        self.button2 = QPushButton('Zoom to the point')
        self.button2.clicked.connect(self.zoom_button)

        self.button3 = QPushButton('Buffer project(feature has not finished yet- beta version)')
        self.button3.clicked.connect(self.buffer_button)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)

        self.setLayout(self.layout)
        self.setFixedSize(400, 200)

    def held_karp(self, costs):
        vertices = list(costs.keys())
        n = len(vertices)

        vertex_index = {vertex: idx for idx, vertex in enumerate(vertices)}
        index_vertex = {idx: vertex for vertex, idx in vertex_index.items()}

        cost = [[0] * n for _ in range(n)]
        for i, vertex_from in enumerate(vertices):
            for vertex_to, c in costs[vertex_from].items():
                j = vertex_index[vertex_to]
                cost[i][j] = c

        C = {}
        for k in range(1, n):
            C[(1 << k, k)] = (cost[0][k], 0)

        for subset_size in range(2, n):
            for subset in itertools.combinations(range(1, n), subset_size):
                bits = 0
                for bit in subset:
                    bits |= 1 << bit
                for k in subset:
                    prev_bits = bits & ~(1 << k)
                    res = []
                    for m in subset:
                        if m == 0 or m == k:
                            continue
                        res.append((C[(prev_bits, m)][0] + cost[m][k], m))
                    C[(bits, k)] = min(res)

        bits = (1 << n) - 2
        res = []
        for k in range(1, n):
            res.append((C[(bits, k)][0] + cost[k][0], k))
        opt, parent = min(res)

        path = []
        bits = (1 << n) - 2
        for i in range(n - 1):
            path.append(parent)
            new_bits = bits & ~(1 << parent)
            _, parent = C[(bits, parent)]
            bits = new_bits

        path.append(0)
        path = list(reversed(path))

        opt_path_labels = [index_vertex[idx] for idx in path]

        return opt, opt_path_labels

    def run_button(self):
        wms_url = 'contextualWMSLegend=0&crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=Raster&styles=&url=https://mapy.geoportal.gov.pl/wss/service/PZGIK/ORTO/WMS/StandardResolution'

        layer_name = 'Geoportal WMS'
        wms_layer = QgsRasterLayer(wms_url, layer_name, 'wms')

        csv = "/home/szymon/Desktop/PycharmProjects/OrangeTask/networks_node.csv"
        uri = f'file://{csv}?delimiter=,&xField=longitude&yField=latitude'

        customer_layer = QgsVectorLayer(uri, 'Clients', 'delimitedtext')
        self.topology_layer = QgsVectorLayer(uri, 'Clients', 'delimitedtext')

        features = self.topology_layer.getFeatures()
        points = []

        for feature in features:
            geometry = feature.geometry()
            if geometry.type() == QgsWkbTypes.PointGeometry:
                    point = geometry.asPoint()
                    points.append(point)

        self.reference = points[1]

        graph = {}
        vertices = [chr(97 + i) for i in range(14)]

        for vertex in vertices:
            edges = {}
            for other_vertex in vertices:
                if other_vertex != vertex:
                    edges[other_vertex] = random.randint(1, 8)
            graph[vertex] = edges

        #print(graph)

        opt_index = [chr(97 + i) for i in range(14)];
        print(opt_index)
        mapping_lists = dict(zip(opt_index, points))

        opt_cost, opt_index = self.held_karp(graph)

        print(opt_index)

        points = [mapping_lists[element] for element in opt_index]
        print(len(points))

        n = 0
        while n+1 < len(points):
            layer = QgsVectorLayer('LineString?crs=epsg:4326', 'Linie', 'memory')
            provider = layer.dataProvider()

            line = QgsGeometry.fromPolylineXY([points[n], points[n+1]])
            feature = QgsFeature()
            feature.setGeometry(line)
            provider.addFeature(feature)

            QgsProject.instance().addMapLayer(layer)

            rb = QgsRubberBand(iface.mapCanvas(), True)
            rb.setColor(QColor(0, 0, 255))
            rb.setWidth(2)
            rb.addPoint(points[n])
            rb.addPoint(points[n+1])
            rb.show()
            n += 1

        try:
            if not wms_layer.isValid():
                raise ValueError("the WMS layer cannot be loaded")

            if not customer_layer.isValid():
                raise ValueError("the client layer cannot be loaded")

            QgsProject.instance().addMapLayer(wms_layer)
            iface.messageBar().pushMessage('success', 'the WMS layer has been loaded', level=Qgis.Info)

            QgsProject.instance().addMapLayer(customer_layer)
            iface.messageBar().pushMessage("success", 'Clients layer has been loaded', level=Qgis.Info)

        except ValueError as e:
            iface.messageBar().pushMessage('file location unavailable', str(e), level=Qgis.Critical)

    def zoom_button(self):
        try:
            zoom_point = self.reference
            canvas = iface.mapCanvas()
            canvas.setExtent(QgsGeometry.fromPointXY(zoom_point).boundingBox())
            zoom_power = 25
            canvas.zoomScale(canvas.scale() / zoom_power)
            canvas.refresh()
        except AttributeError as e:
            iface.messageBar().pushMessage('terrain map is not loaded yet', str(e), level=Qgis.Critical)

    def buffer_button(self):
        try:
            buffer_point = self.reference
            buffer_coefficient = 0.01
            buffer = QgsGeometry.fromPointXY(buffer_point).buffer(buffer_coefficient, 2)
            buffer_factor = QgsFeature()
            buffer_factor.setGeometry(buffer)

            self.buffer_layer = QgsVectorLayer('Polygon?crs=EPSG:4326', 'buffer', 'memory')
            self.buffer_layer.startEditing()
            self.buffer_layer.dataProvider().addFeatures([buffer_factor])
            self.buffer_layer.commitChanges()

            QgsProject.instance().addMapLayer(self.buffer_layer)
            iface.messageBar().pushMessage('success', 'buffer has been created', level=Qgis.Info)
        except AttributeError as e:
            iface.messageBar().pushMessage('terrain map is not loaded yet', str(e), level=Qgis.Critical)

dialog = MyDialog()
dialog.show()
