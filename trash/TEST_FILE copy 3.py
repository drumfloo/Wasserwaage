from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

class WaterLevel(Widget):
    def init(self, kwargs):
        super(WaterLevel, self).init(kwargs)
        self.orientation = 'vertical'
        self.level = 0.5
        self.label = Label(text='Wasserwaage: {:.2f}'.format(self.level))
        self.addwidget(self.label)

        # Zugriff auf den Beschleunigungssensor
        self.acceleration = [0, 0, 0]

        # Aktualisiere die Wasserwaage alle 0.1 Sekunden
        Clock.scheduleinterval(self.updatelevel, 0.1)

    def ontouch_move(self, touch):
        pass  # Deaktiviere die Berührungsbewegung, da wir den Beschleunigungssensor verwenden

    def update_level(self, dt):
        # Aktualisiere die Wasserwaage basierend auf den Beschleunigungssensordaten
        acceleration = Window.request_orientation()[1]
        self.level = 1.0 - acceleration[2]  # Verwende die Z-Achse für die Wasserwaage
        self.level = max(0.0, min(1.0, self.level))
        self.label.text = 'Wasserwaage: {:.2f}'.format(self.level)
        self.canvas.clear()
        self.draw_level()

    def draw_level(self):
        with self.canvas:
            # Zeichne die Wasserwaage
            Color(0, 0, 1)
            Rectangle(pos=(self.x, self.y), size=(self.width, self.height * self.level))
            Color(1, 1, 1)
            Rectangle(pos=(self.x, self.y), size=(self.width, self.height), width=2)

class WaterLevelApp(App):
    def build(self):
        return WaterLevel()

if __name__ == '__main':
    WaterLevelApp().run()