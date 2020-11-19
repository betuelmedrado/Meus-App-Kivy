#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy import require
require('1.9.1')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Ellipse, Rectangle, Color
from kivy.properties import ListProperty
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
import json

# Window.size = 600, 700
class Gerenciador(ScreenManager):
    pass

class Botaos(ButtonBehavior,Label):
    cor = ListProperty([0,.5,7,1])
    cor2 = ListProperty([0,0,.1,1])

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.botao()

    def on_pos(self,*args):
        self.botao()
    def on_size(self,*args):
        self.botao()
    def on_cor(self,*args):
        self.botao()
    def on_press(self):
        self.cor,self.cor2 = self.cor2,self.cor
    def on_release(self):
        self.cor,self.cor2 = self.cor2,self.cor

    def botao(self,*args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor)
            Ellipse(size=(self.height,self.height),pos=(self.x,self.y))
            Ellipse(size=(self.height,self.height),pos=(self.x+self.width-self.height,self.y))
            Rectangle(size=(self.width-self.height,self.height),pos=(self.x+self.height/2, self.y))

class Menu(Screen):
    pop_sound = None
    poppap_sound = None

    def __init__(self,**kwargs):
        super(Menu,self).__init__(**kwargs)

    def on_pre_enter(self):
        Window.bind(on_request_close=self.confirmar)
        # self.ids.lb_menu.text = 'Controle de Finanças'
        if self.pop_sound == None:
            self.pop_sound = SoundLoader.load('poppap.mp3')

    def confirmar(self,*args,**kwargs):
        self.pop_sound.play()

        box = BoxLayout(spacing='10dp',orientation='vertical')
        pop = Popup(title='Deseja realmente sai?', size_hint=(None,None),
                    size=('300sp','200sp'),content=box)
        box_bt = BoxLayout(spacing='13dp',size_hint_y=None,height='30sp')

        image = Image(source='image/atencao.png')

        bt_sim = Botaos(text='Sim',on_release=App.get_running_app().stop)
        bt_nao = Botaos(text='Nao',on_release=pop.dismiss)

        box.add_widget(image)
        box_bt.add_widget(bt_sim)
        box_bt.add_widget(bt_nao)
        box.add_widget(box_bt)

        pop.open()
        return True
        

class Data:
    ListaValor = 0
    list_get = []
    def __init__(self):
        from datetime import date
        self.ListaValor = Data.ListaValor
        self.data_day = date.today().day
        self.data_month = date.today().month
        self.data_year = date.today().year

    def valor(self,name,valores=0):
        arq = open(f'{name}', 'a')
        arq.write(f'{valores}\n')

    def ler_valor(self,name):
        try:
            arq = open(f'{name}','r')
            arq.readline(0)
            self.ListaValor = 0
            self.list_get.clear()

            for linha in arq:
                try:
                    self.list_get.append((int(linha) ))
                except:
                    pass
                despejo = self.list_get
                self.ListaValor = sum(despejo)

            arq.close()
            return self.ListaValor
        except FileNotFoundError:
            pass

    def percentuais(self):
        try:
            arq = open('Valores.txt','r')
            arq.readline(0)
            soma = 0
            for valores in arq:
                try:
                    soma += int(valores)
                except ValueError:
                    pass
            return soma
        except FileNotFoundError:
            return 0


class Adicionar(Screen,Data):
    lista = []
    def __init__(self,**kwargs):
        super(Adicionar,self).__init__(**kwargs)

    def SaveData(self):
        try:
            data = (f'{self.data_day}/{self.data_month}/{self.data_year}')
            modelo = self.ids.text_modelo.text.capitalize()
            local = self.ids.text_local.text.capitalize()
            valor = self.ids.text_valor.text
            eventos = self.ids.text_eventos.text

            if self.ids.text_gastos.text != '':
                gastos = str(float(self.ids.text_gastos.text))
            else:
                gastos = 0

            self.lista.append(f'{data:<25} {modelo:<30} {local:<25} {float(valor):>8} R$')
            self.lista.reverse()

            try:
                # Aqui é para a self.lista receber os conteudos do arquivo json
                with open('SaveData.json', 'r') as dados:
                    self.lista = json.load(dados)  # Aqui é para a lista sempre receber o conteudo do arquivo json primeiro
                    self.lista.append(f'{data:<25} {modelo:<30} {local:<25} {float(valor):>8} R$')
                    self.lista.reverse()
            except:
                pass

            # criando um arquivo json
            with open('SaveData.json', 'w') as data:
                json.dump(self.lista, data)

            # criando um arquivo Valores
            self.valor('Valores.txt',int(self.ids.text_valor.text))
            try:
                # criando um arquivo gastos
                self.valor('gastos.txt', int(self.ids.text_gastos.text))
            except ValueError:
                pass

            self.ids.text_modelo.text = ''
            self.ids.text_local.text = ''
            self.ids.text_valor.text = ''
            self.ids.text_eventos.text = ''
            self.ids.text_gastos.text = ''
        except ValueError:
            pass

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'Menu'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)


class Visualizar(Screen,Data):
    soma = 0
    def __init__(self,**kwargs):
        super(Visualizar,self).__init__(**kwargs)

        self.lista = []
        self.soma = Visualizar.soma
        self.texto = str('{:<30} {:<30} {:<30} {:>6}'.format('Data','Modelo','Local','Valor'))

    def add(self):
        # arquivo_soma = open('cofre_soma.txt', 'r')
        # self.inteiros_soma = arquivo_soma.readlines()
        # arquivo_soma.close()
        # arq = open('cofre.txt', 'r+', encoding='utf-8')

        try:
            with open('SaveData.json','r',encoding='utf-8') as data:
                self.lista = json.load(data)
        except FileNotFoundError:
            with open('SaveData.json', 'w') as data:
                data.close()
        except json.decoder.JSONDecodeError:
            pass

        for linha in self.lista:
            self.ids.coteiner.add_widget(Box(label=str(linha)))

        # for valor in self.inteiros_soma:
        #     self.lista.append(valor.strip())
        # for num in self.lista:
        #     self.soma += float(num)
        # self.soma = 0


    def on_pre_enter(self):
        # colocando texto formatado
        self.ids.super_modelo_text.text = self.texto

        Window.bind(on_keyboard=self.voltar)
        self.add()
        try:
            self.ids.total_valor.text = f'Total: R$   {str(float(self.ler_valor("Valores.txt")))}'
        except TypeError:
            pass


    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'Menu'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        self.ids.coteiner.clear_widgets()
        # self.lista.clear()
        # self.inteiros_soma.clear()


class TelaTotal(Screen,Data):
    soma = 0

    def __init__(self,**kwargs):
        super(TelaTotal,self).__init__(**kwargs)

    def on_pre_enter(self):
        try:
            arquiv = self.ler_valor('gastos.txt')
        except FileNotFoundError:
            arquiv = ''

        self.ids.gastos.clear_widgets()
        self.ids.gastos.add_widget(Box(label=str(arquiv)))

        try:
            self.ids.Valor_soma.text = str(self.ler_valor('Valores.txt'))
        except FileNotFoundError:
            self.valor('Valores.txt')

        percentual_60 = float(self.percentuais() * 60 / 100)
        percentual_40 = float(self.percentuais() - percentual_60)
        self.ids.valor_60.text = str(percentual_60)
        self.ids.valor_40.text = str(percentual_40)



class Box(BoxLayout):
    # Class que tem um BoxLayout com a Label para inserir texto
    def __init__(self,label='',**kwargs):
        super(Box,self).__init__(**kwargs)
        self.ids.texto.text = label


class ControleVerbaApp(App):
    def build(self):
        return Gerenciador()
        # return Tela()

if __name__ == '__main__':
    ControleVerbaApp().run()
