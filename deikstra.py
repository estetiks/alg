import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QPushButton
from PyQt5.QtCore import Qt

# Создаем класс для главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Устанавливаем размеры окна
        self.setGeometry(100, 100, 800, 400)

        # Создаем сцену и представление для графики
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(10, 10, 780, 320)

        # Создаем кнопку для запуска алгоритма
        button1 = QPushButton('Запустить алгоритм обхода в ширину', self)
        button1.setGeometry(10, 340, 260, 50)
        button1.clicked.connect(self.run_dijkstra)

        button2 = QPushButton('Запустить алгоритм обхода в длину', self)
        button2.setGeometry(270, 340, 260, 50)
        button2.clicked.connect(self.run_dijkstra)

        button3 = QPushButton('Запустить алгоритм Дейкстры', self)
        button3.setGeometry(530, 340, 260, 50)
        button3.clicked.connect(self.run_dijkstra)

    def run_dijkstra(self):
        # Здесь можно реализовать алгоритм Дейкстры
        # и визуализацию результата на графике

        # Пример добавления узлов на график
        self.scene.clear()
        self.scene.addEllipse(50, 50, 30, 30, pen=Qt.black, brush=Qt.red)
        self.scene.addEllipse(150, 100, 30, 30, pen=Qt.black, brush=Qt.red)
        self.scene.addEllipse(250, 150, 30, 30, pen=Qt.black, brush=Qt.red)
        self.scene.addEllipse(350, 200, 30, 30, pen=Qt.black, brush=Qt.red)

        # Пример добавления ребер на график
        self.scene.addLine(65, 65, 165, 115, pen=Qt.black)
        self.scene.addLine(165, 115, 265, 165, pen=Qt.black)
        self.scene.addLine(265, 165, 365, 215, pen=Qt.black)
        

# Создаем экземпляр приложения
app = QApplication(sys.argv)

# Создаем экземпляр главного окна
window = MainWindow()

# Отображаем главное окно
window.show()

# Запускаем основной цикл приложения
sys.exit(app.exec_())
