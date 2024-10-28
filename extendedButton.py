from kivy.uix.button import Button


class CustomButton(Button):
    default_color = "linen"
    toggled_color = "skyblue"
    hover_color = "red"
    is_toggeable = True

    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.original_color = self.background_color
        self.is_toggled = False
        self.bind(on_enter=self.on_mouse_enter)
        self.bind(on_leave=self.on_mouse_leave)
        self.bind(on_press=self.toggle)  # Add binding for toggle on press

    def on_mouse_enter(self, instance):
        if not self.is_toggled:
            self.background_color = self.hover_color

    def on_mouse_leave(self, instance):
        if not self.is_toggled:
            self.background_color = self.original_color

    def toggle(self, *args):
        if self.is_toggeable:
            self.is_toggled = not self.is_toggled and self.is_toggeable
            target_color = self.toggled_color if self.is_toggled else self.original_color
            self.background_color = target_color
