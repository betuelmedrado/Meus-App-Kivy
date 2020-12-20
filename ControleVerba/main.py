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
from kivy.animation import Animation
import json
import os
import shutil
from time import sleep

# Window.size = 600, 700
class Gerenciador(ScreenManager):
    pass

class Botaos(ButtonBehavior,Label):
    cor = ListProperty([0,.5,7,1])
    cor2 = ListProperty([0,0,.1,1])

    def __init__(self,**kwargs):
        super(Botaos,self).__init__(**kwargs)
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


class Setting(Screen):

    def __init__(self,*args,**kwargs):
        super(Setting,self).__init__(**kwargs)
        self.dados_usuario = App.get_running_app().user_data_dir +'/'

    def on_pre_leave(self,*args):
        porcentagen = str(self.ids.df_porcentagen.text)
        self.ids.mensagen_setting.text = ''
        if porcentagen != '':
            arq_porcentagen = open('porcentagen.txt','w')
            arq_porcentagen.write(porcentagen)


    def limpar(self,*args,**kwargs):
        pasta = self.dados_usuario
        try:
            # para excluir o diretório
            shutil.rmtree(pasta)
        except OSError:
            self.ids.mensagen_setting.text = 'O diretorio não foi excluido'
        else:
            self.ids.mensagen_setting.text = str('O diretorio foi excluido com sucesso\n Todos arquivos foram apagados!\n   '
                                                 '                Reinicie o app...')

    def popap(self,*args,**kwargs):

        box = BoxLayout(orientation='vertical')
        pop = Popup(title='Deseja limpar o diretórios de arquivos?',size_hint=(None,None),
                    width='200dp',height='150dp',content=box)
        box_botao = BoxLayout(spacing=5,padding=3)
        image = Image(source='image/atencao.png')

        bt_sim = Button(text='Sim',on_press=self.limpar, on_release=pop.dismiss)
        bt_nao = Button(text='Não',on_release=pop.dismiss)

        box_botao.add_widget(bt_sim)
        box_botao.add_widget(bt_nao)

        box.add_widget(image)
        box.add_widget(box_botao)

        anim_bt_nao = Animation(color=(0,0,0,1))+Animation(color=(1,1,1,1))
        anim_bt_nao.start(bt_nao)
        anim_bt_nao.repeat = True

        pop.open()
        return True


class Menu(Screen):
    pop_sound = None
    poppap_sound = None

    def __init__(self,**kwargs):
        super(Menu,self).__init__(**kwargs)
        self.dados_usuario = App.get_running_app().user_data_dir + '/'


    def on_pre_enter(self):
        Window.bind(on_request_close=self.confirmar)
        # self.ids.lb_menu.text = 'Controle de Finanças'

        # Adicionando o som do pupap
        if self.pop_sound == None:
            self.pop_sound = SoundLoader.load('poppap.mp3')

        # Criando os arquivo logo quando abrir o app
        if self.dados_usuario+'arq_eventos.txt' and self.dados_usuario+'arq/gastos.txt':
            pass
        else:
            data = open(self.dados_usuario+'arq_eventos.txt','w')
            Data().valor('gastos.txt')

        if self.dados_usuario+'SaveData.json':
            pass
        else:
            with open(self.dados_usuario+'SaveData.json','w') as data:
                data.close()

    def confirmar(self,*args,**kwargs):
        self.pop_sound.play()

        box = BoxLayout(spacing='10dp',orientation='vertical')
        pop = Popup(title='Deseja realmente sai?', size_hint=(None,None),
                    size=('200dp','150dp'),content=box)
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
        self.dados_usuario = App.get_running_app().user_data_dir + '/'

    def valor(self,name,valores=''):
        if valores != '':
            arq = open(f'{self.dados_usuario+name}', 'a')
            arq.write(f'{valores}\n')
        else:
            pass

    def ler_valor(self,name):
        try:
            arq = open(f'{self.dados_usuario+name}','r')
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
            arq = open(self.dados_usuario+'Valores.txt','r')
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
    get = ''
    def __init__(self,**kwargs):
        super(Adicionar,self).__init__(**kwargs)
        self.data = (f'{self.data_day}/{self.data_month}/{self.data_year}')
        self.dados_usuario = App.get_running_app().user_data_dir + '/'


    def on_pre_enter(self):
        self.ids.lb_title.text = str('Adicione os cerviços e os gastos')
        self.get = self.ids.mensagen_add.text
        self.dados_usuario = App.get_running_app().user_data_dir + '/'
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_keyboard=self.teclas)
        self.save_data()

    def save_data(self):
        modelo = self.ids.text_modelo.text.capitalize()
        local = self.ids.text_local.text.capitalize()
        eventos = self.ids.text_eventos.text
        valor_int = self.ids.text_valor.text
        gastos = 0

        if self.ids.text_gastos.text != '':
            try:
                gastos = str(int(self.ids.text_gastos.text))
            except ValueError:
                self.ids.mensagen_gastos.text = 'Digitos invalido no campo gastos "Só numeros"'
        else:
            gastos = 0


        try:
            # Aqui é para a self.lista receber os conteudos do arquivo json
            with open(self.dados_usuario+'SaveData.json', 'r') as dados:
                self.lista = json.load(dados)  # Aqui é para a lista sempre receber o conteudo do arquivo json primeiro
                self.lista.append(f'{self.data:<25} {modelo:<30} {local:<25} {float(valor_int):>8} R$')
                self.ids.text_modelo.text = ''
                self.ids.text_local.text = ''
                self.ids.text_valor.text = ''

                try:
                    # criando um arquivo Valores
                    self.valor('Valores.txt', int(valor_int))
                except ValueError:
                    pass
                self.ids.mensagen_add.text = 'Arquivos salvos com sucesso!'
                self.get = self.ids.mensagen_add.text
        except:
            # self.ids.mensagen_add.text = 'Nada foi salvo'
            self.get = self.ids.mensagen_add.text

        try:
            # criando um arquivo json e recebendo os conteudo da lista
            with open(self.dados_usuario+'SaveData.json', 'w') as data:
                json.dump(self.lista, data)
        except FileNotFoundError:
            pass

        try:
            if gastos != 0 and eventos != '':
                # criando um arquivo gastos
                self.valor('gastos.txt',gastos)
            elif gastos == 0 and eventos != '':
                pass
            elif gastos != 0 and eventos == '':
                pass
        except ValueError:
            pass

        if gastos != 0 and eventos != '':
            # criando arquivo para os eventos de gastos
            arq_eventos = open(self.dados_usuario+'arq_eventos.txt', 'a')
            arq_eventos.write(f'{eventos}  {gastos}\n')
            self.ids.mensagen_gastos.text = 'Eventos gastos salvos'
            self.ids.mensagen_add.text = self.get
            self.ids.text_eventos.text = ''
            self.ids.text_gastos.text = ''
        elif gastos != 0 and eventos == '':
            self.ids.mensagen_gastos.text = 'Compo Eventos não preenchidos'
            self.ids.mensagen_add.text = self.get
        elif gastos == str:
            self.ids.mensagen_sobra.text = 'Digitos invalido no campo gastos "Só numeros"'
        elif gastos == 0 and eventos != '':
            self.ids.mensagen_gastos.text = 'Campo gastos não preenchidos corretamente'
            self.ids.mensagen_add.text = self.get
        # sleep(3)
        # self.ids.mensagen_add.text = 'Alguns Valores estão errado Revise'



    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'Menu'
            return True
    def teclas(self,window,key,*args):
        if key == 13:
            self.save_data()

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)


class Visualizar(Screen,Data):
    soma = 0

    def __init__(self,**kwargs):
        super(Visualizar,self).__init__(**kwargs)
        self.box = Box()
        self.lista = []
        self.lista_valores = []
        self.soma = Visualizar.soma
        # pegando o diretório do usuario
        self.dados_usuario = App.get_running_app().user_data_dir + '/'

        self.texto = str('{:<30} {:<30} {:<30} {:>6}'.format('Data','Modelo','Local','Valor'))

    def add(self):
        try:
            with open(self.dados_usuario+'SaveData.json','r',encoding='utf-8') as data:
                self.lista = json.load(data)
        except FileNotFoundError:
            try:
                with open(self.dados_usuario+'SaveData.json', 'w') as data:
                    data.close()
            except FileNotFoundError:
                pass
        except json.decoder.JSONDecodeError:
            pass

        self.lista.reverse()
        for linha in self.lista:
            self.ids.coteiner.add_widget(Box(label=str(linha)))

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

    def popap(self,root,*args):

        self.root = root

        coteiner = BoxLayout(orientation='vertical')
        pop = Popup(title='Deseja realmente excluir?', content=coteiner, size_hint=(None, None),
                    size=('200dp', '150dp'))
        image = Image(source='image/atencao.png')
        bt_box = BoxLayout(spacing=11,padding=5)

        bt_sim = Botaos(text='Sim', on_press=self.deletar, on_release=pop.dismiss)
        bt_nao = Botaos(text='Não',on_release=pop.dismiss)

        bt_box.add_widget(bt_sim)
        bt_box.add_widget(bt_nao)

        coteiner.add_widget(image)
        coteiner.add_widget(bt_box)
        pop.open()

        # return True

    def deletar(self,*args):
        texto = self.root.ids.texto.text
        try:
            self.lista.clear()
            with open(self.dados_usuario+'SaveData.json','r',encoding='utf-8')as get_json:
                self.lista = json.load(get_json)
            self.ids.coteiner.remove_widget(self.root)

            pos = self.lista.index(texto)
            self.lista.remove(texto)

            with open(self.dados_usuario+'SaveData.json','w',encoding='utf-8') as save_json:
                json.dump(self.lista, save_json)

            # Abrindo o arquivo Valores para obter os valores
            arq_valores = open(self.dados_usuario+'Valores.txt','r')

            # Adicionando os valores do arquivo na lista
            for valor in arq_valores.readlines():
                self.lista_valores.append(valor)
            arq_valores.close()

            # Removendo o valor da lista na posição do arquivo json "pos"
            try:
                del(self.lista_valores[pos])
            except IndexError:
                pass
            # Salvando novamente os valores no arquivo
            arq_valores_despejo = open(self.dados_usuario+'Valores.txt','w')
            for num in self.lista_valores:
                arq_valores_despejo.write(num)
            arq_valores_despejo.close()
            self.lista_valores.clear()

            # Reinscrevendo na tela
            try:
                self.ids.total_valor.text = f'Total: R$   {str(float(Visualizar().percentuais()))}'
            except TypeError:
                pass
        except ValueError or AttributeError:
            pass

        ##################################################################



class TelaTotal(Screen,Data):
    soma = 0
    def __init__(self,**kwargs):
        super(TelaTotal,self).__init__(**kwargs)
        # eventos = self.ids.text_eventos.text
        self.lista_eventos = []
        self.lista_gastos = []
        self.dados_usuario = App.get_running_app().user_data_dir + '/'

    def on_pre_enter(self):
        # aqui a TelaTotal recebe a porcentagen do arquivo
        arq_porcentagen = open('porcentagen.txt', 'r')
        self.main_porcentagen = arq_porcentagen.read()

        # trying open file gastos.txt  se não existir  a variavel arquiv sera criada com espaço em branco
        try:
            arquiv = self.ler_valor('gastos.txt')
        except FileNotFoundError:
            arquiv = 0

        # abrindo arquivo arq_eventos.txt para ler a quantidades de eventos
        try:
            add_arq = open(self.dados_usuario+'arq_eventos.txt', 'r')
            self.ids.gastos.clear_widgets()
            for iten in add_arq.readlines():
                self.ids.gastos.add_widget(Box_Total(label=str(iten)))
        except FileNotFoundError:
            add_arq = ''

        try:
            # Passando a variavel do arquiv com self.ler_valor('gastos.txt') para somas
            self.ids.total_gastos.text = str(f'Total gastos: {float(arquiv)}')
        except TypeError:
            pass

        # Tentando abrir o arquivo Valores.txt para soma se não existir será criado
        try:
            s_v = float(self.ler_valor('Valores.txt'))
            self.ids.Valor_soma.text = f'{s_v:.1f}'
        except FileNotFoundError:
            self.valor('Valores.txt')
        except TypeError:
            self.ids.Valor_soma.text = '0'

        # Criando e Mostrando as divisões das porcentagen e adicionando ao label
        percentual_main = float(self.percentuais() * int(self.main_porcentagen) / 100)
        percentual_sobra = float(self.percentuais() - percentual_main)
        self.ids.label_main.text = f'{self.main_porcentagen} %'
        self.ids.label_sobra.text = f'{100-int(self.main_porcentagen)} %'

        # Aqui formata os valores
        v_m = float(percentual_main)
        v_s = float(percentual_sobra)
        self.ids.valor_sobra.text = f'{v_s:.2f}'
        self.ids.valor_main.text = f'{v_m:.2f}'



    def popap(self, root, *args):
        self.root = root

        coteiner = BoxLayout(orientation='vertical')
        pop = Popup(title='Deseja realmente excluir?', content=coteiner, size_hint=(None, None),
                    size=('200dp', '150dp'))

        image = Image(source='image/atencao.png')
        bt_box = BoxLayout(spacing=11,padding=5)

        bt_sim = Botaos(text='Sim', on_press=self.deletar, on_release=pop.dismiss)
        bt_nao = Botaos(text='Não', on_release=pop.dismiss)

        bt_box.add_widget(bt_sim)
        bt_box.add_widget(bt_nao)

        coteiner.add_widget(image)
        coteiner.add_widget(bt_box)
        pop.open()


    def deletar(self,*args):
        texto = self.root.ids.texto.text
        try:
            # Excluindo dos arquivos eventos e gastos
            self.ids.gastos.remove_widget(self.root)

            # Limpando as listas
            self.lista_eventos.clear()
            self.lista_gastos.clear()

            ler_eventos = open(self.dados_usuario+'arq_eventos.txt','r')
            for eventos in ler_eventos:
                self.lista_eventos.append(eventos)

            # geting the position file
            pos_eventos = self.lista_eventos.index(texto)

            # deletando o valor na posição do evento
            del(self.lista_eventos[pos_eventos])

            # Re increvendo os eventos no arquivo
            add_eventos = open(self.dados_usuario+'arq_eventos.txt','w')
            for eventos in self.lista_eventos:
                add_eventos.write(eventos)

            # Abrindo o arquivo para leitura
            ler_gastos = open(self.dados_usuario+'gastos.txt','r')
            for valor in ler_gastos.readlines():
                self.lista_gastos.append(int(valor))
            ler_gastos.close()

            del(self.lista_gastos[pos_eventos])

            add_gastos = open(self.dados_usuario+'gastos.txt','w')
            for valor in self.lista_gastos:
                add_gastos.write(f'{str(valor)}\n')

            soma = sum(self.lista_gastos)
            self.ids.total_gastos.text = f'Total gastos: {str(float(soma))}'
        except ValueError or FileNotFoundError:
            pass


class Box(BoxLayout):
    # Class que tem um BoxLayout com a Label para inserir texto
    lista = []
    lista_valores = []
    def __init__(self,label='',**kwargs):
        super(Box,self).__init__(**kwargs)
        self.ids.texto.text = label
        self.label = label


    # def deletar(self,box):
    #     with open('SaveData.json','r') as data_json:
    #         for enu,linha in enumerate(json.load(data_json)):
    #             self.lista.append(linha)
    #
    #     self.remove_widget(box)
    #     self.lista.remove(self.label)
    #     print(self.label)
    #
    #
    #     with open('SaveData.json','w') as data:
    #         json.dump(self.lista, data)
    #
    #     arq_valores = open('Valores.txt','r')
    #     arq_valores.readline()
    #
    #     for valor in arq_valores:
    #         self.lista_valores.append(valor)

class Box_Total(BoxLayout):
    # Class que tem um BoxLayout com a Label para inserir texto
    lista = []
    lista_valores = []
    def __init__(self,label='',**kwargs):
        super(Box_Total,self).__init__(**kwargs)
        self.ids.texto.text = label
        self.label = label




class ControleVerbaApp(App):
    def build(self):
        return Gerenciador()
        # return Tela()

if __name__ == '__main__':
    ControleVerbaApp().run()
