import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog

class GraphApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Граф")
        
        self.adjacency_matrix = []
        
        self.create_main_window()

    def create_main_window(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid()

        fill_matrix_button = ttk.Button(main_frame, text="Заполнить матрицу", command=self.open_fill_matrix_window)
        fill_matrix_button.grid(row=0, column=0, padx=10, pady=10)

        dfs_button = ttk.Button(main_frame, text="Обход в глубину", command=self.dfs)
        dfs_button.grid(row=0, column=1, padx=10, pady=10)

        bfs_button = ttk.Button(main_frame, text="Обход в ширину", command=self.bfs)
        bfs_button.grid(row=0, column=2, padx=10, pady=10)

        dijkstra_button = ttk.Button(main_frame, text="Алгоритм Дейкстры", command=self.dijkstra)
        dijkstra_button.grid(row=0, column=3, padx=10, pady=10)

        floyd_warshall_button = ttk.Button(main_frame, text="Алгоритм Флойда-Уоршелла", command=self.floyd_warshall)
        floyd_warshall_button.grid(row=1, column=0, padx=10, pady=10)

        ford_fulkerson_button = ttk.Button(main_frame, text="Алгоритм Форда-Фалкерсона", command=self.ford_fulkerson)
        ford_fulkerson_button.grid(row=1, column=1, padx=10, pady=10)

    def open_fill_matrix_window(self):
        fill_matrix_window = tk.Toplevel(self.root)
        fill_matrix_window.title("Заполнить матрицу")

        vertices_label = ttk.Label(fill_matrix_window, text="Количество вершин:")
        vertices_label.grid(row=0, column=0, padx=10, pady=10)

        vertices_entry = ttk.Entry(fill_matrix_window)
        vertices_entry.grid(row=0, column=1, padx=10, pady=10)

        submit_button = ttk.Button(fill_matrix_window, text="Подтвердить", command=lambda: self.fill_matrix(fill_matrix_window, int(vertices_entry.get())))
        submit_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def fill_matrix(self, window, num_vertices):
        matrix_window = tk.Toplevel(window)
        matrix_window.title("Матрица смежности")

        self.adjacency_matrix = [[0] * num_vertices for _ in range(num_vertices)]

        for i in range(num_vertices):
            for j in range(num_vertices):
                entry = ttk.Entry(matrix_window, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)

        submit_button = ttk.Button(matrix_window, text="Подтвердить", command=lambda: self.get_adjacency_matrix(matrix_window))
        submit_button.grid(row=num_vertices, column=0, columnspan=num_vertices, padx=10, pady=10)

    def get_adjacency_matrix(self, window):
        children = window.winfo_children()

        for child in children:
            if isinstance(child, ttk.Entry):
                row = int(child.grid_info()["row"])
                column = int(child.grid_info()["column"])
                value = int(child.get())
                self.adjacency_matrix[row][column] = value

        window.destroy()

    def dfs(self):
        start_vertex = self.get_start_vertex()
        visited = [False] * len(self.adjacency_matrix)
        path = []
        self.dfs_recursive(start_vertex, visited, path)
        messagebox.showinfo("Обход в глубину", f"Путь: {path}")

    def dfs_recursive(self, vertex, visited, path):
        visited[vertex] = True
        path.append(vertex)

        for i in range(len(self.adjacency_matrix)):
            if self.adjacency_matrix[vertex][i] != 0 and not visited[i]:
                self.dfs_recursive(i, visited, path)

    def bfs(self):
        start_vertex = self.get_start_vertex()
        visited = [False] * len(self.adjacency_matrix)
        path = []
        queue = [start_vertex]
        visited[start_vertex] = True

        while queue:
            vertex = queue.pop(0)
            path.append(vertex)

            for i in range(len(self.adjacency_matrix)):
                if self.adjacency_matrix[vertex][i] != 0 and not visited[i]:
                    queue.append(i)
                    visited[i] = True

        messagebox.showinfo("Обход в ширину", f"Путь: {path}")

    def dijkstra(self):
        start_vertex, end_vertex = self.get_start_end_vertices()
        num_vertices = len(self.adjacency_matrix)
        distance = [float("inf")] * num_vertices
        distance[start_vertex] = 0
        visited = [False] * num_vertices
        path = []

        for _ in range(num_vertices):
            min_distance = float("inf")
            min_vertex = -1

            for v in range(num_vertices):
                if not visited[v] and distance[v] < min_distance:
                    min_distance = distance[v]
                    min_vertex = v

            visited[min_vertex] = True

            for v in range(num_vertices):
                if (
                    not visited[v]
                    and self.adjacency_matrix[min_vertex][v] != 0
                    and distance[min_vertex] + self.adjacency_matrix[min_vertex][v] < distance[v]
                ):
                    distance[v] = distance[min_vertex] + self.adjacency_matrix[min_vertex][v]

        if distance[end_vertex] == float("inf"):
            messagebox.showinfo("Алгоритм Дейкстры", "Пути нет")
        else:
            current_vertex = end_vertex
            while current_vertex != start_vertex:
                path.insert(0, current_vertex)
                for v in range(num_vertices):
                    if (
                        self.adjacency_matrix[v][current_vertex] != 0
                        and distance[current_vertex] == distance[v] + self.adjacency_matrix[v][current_vertex]
                    ):
                        current_vertex = v
                        break
            path.insert(0, start_vertex)

            messagebox.showinfo("Алгоритм Дейкстры", f"Путь: {path}, Длина: {distance[end_vertex]}")

    def floyd_warshall(self):
        num_vertices = len(self.adjacency_matrix)
        distances = [[float("inf") if i != j else 0 for j in range(num_vertices)] for i in range(num_vertices)]

        for i in range(num_vertices):
            for j in range(num_vertices):
                if self.adjacency_matrix[i][j] != 0:
                    distances[i][j] = self.adjacency_matrix[i][j]

        for k in range(num_vertices):
            for i in range(num_vertices):
                for j in range(num_vertices):
                    distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])

        messagebox.showinfo("Алгоритм Флойда-Уоршелла", f"Матрица кратчайших путей:\n{distances}")

    def ford_fulkerson(self):
        start_vertex, end_vertex = self.get_start_end_vertices()
        max_flow = self.ford_fulkerson_algorithm(start_vertex, end_vertex)
        messagebox.showinfo("Алгоритм Форда-Фалкерсона", f"Максимальный поток: {max_flow}")

    def ford_fulkerson_algorithm(self, source, sink):
        residual_graph = self.adjacency_matrix.copy()
        num_vertices = len(residual_graph)
        parent = [-1] * num_vertices
        max_flow = 0

        while self.bfs(residual_graph, source, sink, parent):
            path_flow = float("inf")
            s = sink

            while s != source:
                path_flow = min(path_flow, residual_graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                residual_graph[u][v] -= path_flow
                residual_graph[v][u] += path_flow
                v = parent[v]

        return max_flow

    def bfs(self, graph, source, sink, parent):
        num_vertices = len(graph)
        visited = [False] * num_vertices
        queue = [source]
        visited[source] = True

        while queue:
            u = queue.pop(0)

            for v in range(num_vertices):
                if not visited[v] and graph[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u

        return True if visited[sink] else False

    def get_start_vertex(self):
        start_vertex = simpledialog.askinteger("Начальная вершина", "Введите номер начальной вершины:", parent=self.root)
        return start_vertex

    def get_start_end_vertices(self):
        start_vertex = simpledialog.askinteger("Начальная вершина", "Введите номер начальной вершины:", parent=self.root)
        end_vertex = simpledialog.askinteger("Конечная вершина", "Введите номер конечной вершины:", parent=self.root)
        return start_vertex, end_vertex

    def run(self):
        self.root.mainloop()

app = GraphApp()
app.run()
