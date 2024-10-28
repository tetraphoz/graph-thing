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


class Search(GridLayout):
    def __init__(self, **kwargs):
        super(Search, self).__init__(**kwargs)
        self.cols = 10
        self.rows = 10
        self.spacing = 5
        self.padding = 10
        self.buttons = []  # Estructura de datos para interactuar con botones

        # Generamos cuadricula
        for i in range(1, 101):
            button = CustomButton()
            if i == 1:
                button.background_color = "darkseagreen"
                button.is_toggeable = False
            if i == 100:
                button.background_color = "maroon"
                button.is_toggeable = False
            self.buttons.append(button)
            self.add_widget(button)

    def get_neighbours(self, index):
        neighbors = []
        row, col = index // 10, index % 10

        # Check all 4 directions: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < 10 and 0 <= new_col < 10):
                neighbor_index = new_row * 10 + new_col
                if not self.buttons[neighbor_index].is_toggled:
                    neighbors.append(neighbor_index)

        return neighbors

    def dfs(self):
        start = 0  # Button 1
        end = 99   # Button 100

        if self.buttons[start].is_toggled or self.buttons[end].is_toggled:
            return None

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
        # TODO: Implementar
        pass

    def a_star(self):
        # TODO: Implementar
        pass


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
                          values=('DFS', 'BFS', 'A*'))

        btn_buscar = Button(text="Buscar")
        btn_buscar.background_color = "coral"
        btn_buscar.bind(on_press=self.buscar)

        btn_reiniciar = Button(text="Reiniciar")
        btn_reiniciar.background_color = "mediumvioletred"
        btn_reiniciar.bind(on_press=self.reiniciar)

        button_layout.add_widget(self.spinner)
        button_layout.add_widget(btn_buscar)
        button_layout.add_widget(btn_reiniciar)

        self.add_widget(button_layout)

    def reiniciar(self, instance):
        # Reiniciar animaciones
        for button in self.search_widget.buttons:
            Animation.cancel_all(button, 'background_color')

        # Descongelar botones
        for i, button in enumerate(self.search_widget.buttons):
            if i != 0 and i != 99:
                button.is_toggeable = True
                if button.is_toggled:
                    button.toggle()
                else:
                    button.background_color = button.default_color

    def buscar(self, instance):
        # Congelar botones
        for button in self.search_widget.buttons:
            button.is_toggeable = False

        # Cancelar animaciones por si acaso
        for button in self.search_widget.buttons:
            Animation.cancel_all(button, 'background_color')

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
                          content=Label(text='No es posible llegar a la meta'),
                          size_hint=(0.3, 0.2))
            popup.open()

    def visualize(self, path, index=0):
        if not path or index >= len(path):
            return

        # Tenemos que usar una lista de colores para poder animar
        head = self.search_widget.buttons[path[index+1]] # Brincamos celda inicial
        anim = Animation(background_color=[0, 1, 0, 1], duration=0.1) + \
               Animation(background_color=[0.7, 1, 0.7, 1], duration=0.1)

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
