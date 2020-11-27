#Varios teste até dar certo


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class Tela(BoxLayout):
    pass



class TestApp(App):
    def build(self):
        return Tela()

TestApp().run()