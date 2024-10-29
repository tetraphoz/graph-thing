from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from extendedButton import CustomButton
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.label import Label
import sys
import heapq


# CASILLAS = int(sys.argv[1])
CASILLAS = 10


class Search(GridLayout):
    def __init__(self, **kwargs):
        super(Search, self).__init__(**kwargs)
        self.cols = CASILLAS
        self.rows = CASILLAS
        self.spacing = 5
        self.padding = 10
        self.buttons = []  # Estructura de datos para interactuar con botones

        # Generamos cuadricula
        for i in range(1, CASILLAS ** 2 + 1):
            button = CustomButton()
            if i == 1:
                button.background_color = "darkseagreen"
                button.background_normal = ''
                button.is_toggeable = False
            if i == CASILLAS ** 2:
                button.background_color = "maroon"
                button.background_normal = ''
                button.is_toggeable = False
            self.buttons.append(button)
            self.add_widget(button)

    def get_neighbours(self, index):
        neighbors = []
        row, col = index // CASILLAS, index % CASILLAS

        # Check all 4 directions: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < CASILLAS and 0 <= new_col < CASILLAS):
                neighbor_index = new_row * CASILLAS + new_col
                if not self.buttons[neighbor_index].is_toggled:
                    neighbors.append(neighbor_index)

        return neighbors

    def dfs(self):
        start = 0
        end = CASILLAS ** 2 - 1

        stack = [(start, [start])]
        visited = set()

        while stack:
            current, path = stack.pop()

            if current == end:
                return path

            if current not in visited:
                visited.add(current)

                for neighbor in self.get_neighbours(current):
                    if neighbor not in visited and not self.buttons[neighbor].is_toggled:
                        stack.append((neighbor, path + [neighbor]))

        return None  # No path found

    def bfs(self):
        start = 0
        end = CASILLAS ** 2 - 1

        queue = [(start, [start])]
        visited = set()

        while queue:
            current, path = queue.pop(0)

            if current == end:
                return path

            if current not in visited:
                visited.add(current)

                for neighbor in self.get_neighbours(current):
                    if neighbor not in visited and not self.buttons[neighbor].is_toggled:
                        queue.append((neighbor, path + [neighbor]))
            
        return None  # No path found


    def traced_path(self, desde, current):
        total_path = [current]

        while current in desde:
            current = desde[current]
            total_path.append(current)

        total_path.reverse()
        return total_path

    def heuristic(self, node, end):
        x_1, y_1 = divmod(node, CASILLAS)
        x_2, y_2 = divmod(end, CASILLAS)

        h = abs(x_1 - x_2) + abs(y_1 - y_2)
        return h

    def a_star(self):
        start = 0
        end = CASILLAS ** 2 - 1

        open_set = []
        heapq.heappush(open_set, (0, start))

        desde = {}
        costo = {node: float('inf') for node in range(CASILLAS ** 2)}
        costo[start] = 0

        costo_estimado = {node: float('inf') for node in range(CASILLAS ** 2)}
        costo_estimado[start] = self.heuristic(start, end)
        
        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == end:
                return self.traced_path(desde, current)

            for neighbor in self.get_neighbours(current):
                if not self.buttons[neighbor].is_toggled:
                    costo_tentativo = costo[current] + 1  

                    if costo_tentativo < costo[neighbor]:
                        desde[neighbor] = current
                        costo[neighbor] = costo_tentativo
                        costo_estimado[neighbor] = costo[neighbor] + self.heuristic(neighbor, end)

                        if neighbor not in [i[1] for i in open_set]:
                            heapq.heappush(open_set, (costo_estimado[neighbor], neighbor))

        return None  # No path found


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Agregamos cuadricula a ventana principal
        self.search_widget = Search(size_hint=(1, 0.9))
        self.add_widget(self.search_widget)

        # Agregamos botones
        button_layout = BoxLayout(size_hint=(1, 0.1))

        self.spinner = Spinner(text='DFS',
                               font_size = self.width / 2,
                               background_normal='',
                               color= 'black',
                               background_color = 'lavender',
                               values=('DFS', 'BFS', 'A*'))

        self.btn_buscar = Button(text="Buscar",
                                 font_size = self.width / 2,
                                 background_normal='',
                                 color= 'black',
                                 background_color = 'lavenderblush')
        self.btn_buscar.bind(on_press=self.buscar)

        btn_reiniciar = Button(text="Reiniciar",
                               font_size = self.width / 2,
                               background_normal='',
                               color= 'black',
                               background_color = 'mintcream')
        btn_reiniciar.bind(on_press=self.reiniciar)

        button_layout.add_widget(self.spinner)
        button_layout.add_widget(self.btn_buscar)
        button_layout.add_widget(btn_reiniciar)

        self.add_widget(button_layout)

    def reiniciar(self, instance):
        for button in self.search_widget.buttons:
            Animation.cancel_all(button, 'background_color')

        for i, button in enumerate(self.search_widget.buttons):
            if i != 0 and i != CASILLAS ** 2 - 1:
                button.is_toggeable = True
                if button.is_toggled:
                    button.toggle()
                else:
                    button.background_color = button.default_color

        self.btn_buscar.disabled = False
        self.spinner.disabled = False

    def restablecer_grid(self, instance):
        for button in self.search_widget.buttons:
            Animation.cancel_all(button, 'background_color')

        for i, button in enumerate(self.search_widget.buttons):
            if i == 0:
                button.background_color = "darkseagreen"
            elif i == CASILLAS ** 2 - 1:
                button.background_color = "maroon"
            else:
                button.is_toggeable = True
                if not button.is_toggled:
                    button.background_color = button.default_color

        self.btn_buscar.disabled = False
        self.spinner.disabled = False

    def buscar(self, instance):
        self.btn_buscar.disabled = True
        self.spinner.disabled = True

        # Congelar botones en grid
        for button in self.search_widget.buttons:
            button.is_toggeable = False

        # Obtener el valor del spinner
        busqueda_sel = self.spinner.text

        # Llamar a la función de búsqueda correspondiente
        path = None
        if busqueda_sel == 'DFS':
            path = self.search_widget.dfs()
        elif busqueda_sel == 'BFS':
            path = self.search_widget.bfs()
        elif busqueda_sel == 'A*':
            path = self.search_widget.a_star()

        if path:
            self.visualize(path)
        else:
            popup = Popup(title=':C',
                          content=Label(text='No es posible llegar a la meta',
                                        font_size=self.width / 50),
                          size_hint=(0.3, 0.2))
            popup.open()
            self.restablecer_grid(self)

    def visualize(self, path, index=1):  # Brincamos celda inicial
        if not path or index >= len(path):
            self.restablecer_grid(self)
            return

        # Tenemos que usar una lista de colores para poder animar
        anim = Animation(background_color=[0, 0.8, 0, 0.5], duration=0.005)
        head = self.search_widget.buttons[path[index]]

        anim.bind(on_complete=lambda *args: self.visualize(path, index+1))
        anim.start(head)


class SearchApp(App):
    def build(self):
        Window.borderless = True
        Window.fullscreen = 0
        Window.clearcolor = "cornsilk"
        return MainLayout()


if __name__ == '__main__':
    Window.size = (400, 500)
    SearchApp().run()
