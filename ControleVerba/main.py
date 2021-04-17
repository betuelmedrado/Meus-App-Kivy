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
from kivy.lang.builder import Builder
import json
import os
import shutil
from kivy.clock import Clock
from datetime import date

# Window.size = 350, 500

Window.clearcolor = .1,.1,.1,1
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

# pos_mes = 2
# dia_teste = 23

class Setting(Screen):
    lista_month = ['1-janeiro','2-fevereiro','3-março','4-abril','5-maio','6-junho','7-julho','8-agosto','9-setembro','10-outubro','11-novembro','12-dezembro']
    spiner = []
    ligar = None

    def __init__(self,*args,**kwargs):
        super(Setting,self).__init__(**kwargs)
        from datetime import date

        # Data day month and year
        self.day = date.today().day
        self.month = date.today().month
        self.year = date.today().year
        # self.month = pos_mes  # ============= teste

        # get the user directory
        # pegar o diretorio do usuario
        self.dados_usuario = App.get_running_app().user_data_dir +'/'

        step_spiner = open("step_spiner.txt",'r',encoding="utf-8")
        self.step_spiner = step_spiner.read()

        if self.step_spiner == '':
            self.step_spiner = self.lista_month[self.month-1]

        self.get_dir()

    def get_dir(self):
        # Here find the dir and the name and pass the content to the variavel spiner
        dados = str(self.dados_usuario)
        if os.path.isdir(dados):
            lista = os.listdir(dados)
            for pasta in lista:
                self.spiner.append(pasta.title())

    def on_pre_enter(self):
        self.ids.spiner_month.text = str(self.step_spiner).title()

        file = open("fechamento.txt","r")
        file_fechamento1 = file.read(2).strip()
        file_fechamento2 = file.read(3).strip()
        self.ids.fechamento1.text = str(file_fechamento1)
        self.ids.fechamento2.text = str(file_fechamento2)

    def on_pre_leave(self,*args):
        porcentagen = str(self.ids.df_porcentagen.text)
        self.ids.mensagen_setting.text = ''
        if porcentagen != '':
            if 'a'< porcentagen > 'z' or 'A'< porcentagen > 'Z':
                App.get_running_app().root.current = "setting"
                self.ids.mensagen_setting.text = "[color=990000ff][size=18sp]Informação de porcentagen incorretas![/size][/color]"
                Clock.schedule_once(self.retornar_msg, 7)
            else:
                arq_porcentagen = open('porcentagen.txt','w')
                arq_porcentagen.write(porcentagen)
        if self.ids.fechamento1.text != '' :
            try:
                if int(self.ids.fechamento1.text) > 31 or int(self.ids.fechamento2.text) > 31:
                    App.get_running_app().root.current = "setting"
                    self.ids.mensagen_setting.text = "[color=990000ff][size=18sp]Informação de fechamento incorretas![/size][/color]"
                    Clock.schedule_once(self.retornar_msg, 7)
                else:
                    file_fechamento = open('fechamento.txt', 'w')
                    file_fechamento.write(f'{self.ids.fechamento1.text}\n')
                    file_fechamento.write(self.ids.fechamento2.text)

            except ValueError:
                pass

        file_step_spiner = open('step_spiner.txt','w',encoding='utf-8')
        file_step_spiner.write(self.ids.spiner_month.text.strip().lower())
        file_step_spiner.close()

    def limpar(self,*args,**kwargs):
        pasta = self.dados_usuario
        try:
            # para excluir o diretório
            shutil.rmtree(pasta)

            file_step_spiner = open('step_spiner.txt', 'w', encoding='utf-8')
            file_step_spiner.write(self.lista_month[self.month - 1])
            file_step_spiner.close()

            file_month = open("month.txt","w", encoding="utf-8")
            file_month.write(self.lista_month[self.month - 1])
            file_month.close()

        except OSError:
            self.ids.mensagen_setting.text = 'O diretorio não foi excluido'
        else:
            self.ids.mensagen_setting.text = str('O diretorio foi excluido com sucesso\n Todos arquivos foram apagados!\n   '
                                                 '                Reinicie o app...')


    def excluir_mes(self,*args):
        """
        Function to exclud the folder of month choincing
        Função para excluir a pasta do mês escolhido
        :return:
        """
        try:
        # get values of month selecting in variable spiner_month
        # pega valor do mês selecionado na variável spiner_month
            folder_month = self.ids.spiner_month.text.strip()
            path = self.dados_usuario + str(folder_month)
            shutil.rmtree(path)
            # self.get_dir()
            self.ids.spiner_month.text = str(self.lista_month[self.month - 1])
            self.ids.mensagen_setting.text = "Diretório excluido com sucesso!"
        except FileNotFoundError:
            self.ids.mensagen_setting.text = "A pasta já foi excluida reinicie o aplicativo\n para atualizar"
            self.ids.spiner_month.text = str(self.lista_month[self.month - 1])
        Clock.schedule_once(self.retornar_msg,5)

    def retornar_msg(self,*args):
        self.ids.mensagen_setting.text = 'Apos incerir a porcentagen o programa recebe \n altomaticamente o valor!'

    def popap(self,*args,**kwargs):

        box = BoxLayout(orientation='vertical')
        pop = Popup(title='Deseja limpar o diretórios de arquivos?',size_hint=(None,None),
                    width='200dp',height='150sp',content=box)
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

    def popap2(self,*args, **kwargs):

        conteudo = BoxLayout(orientation="vertical")
        pop = Popup(title="Deseja excluir o mes selecionado?", size_hint=(None,None), width="200dp",height="150dp",
                    content=conteudo)
        image = Image(source="image/atencao.png")

        box = BoxLayout()
        bt_sim = Button(text="sim",on_press=self.excluir_mes, on_release=pop.dismiss)
        bt_nao = Button(text="não",on_release=pop.dismiss)

        box.add_widget(bt_sim)
        box.add_widget(bt_nao)

        conteudo.add_widget(image)
        conteudo.add_widget(box)

        pop.open()
        return True


class Menu(Screen):
    lista_month = ['1-janeiro','2-fevereiro','3-março','4-abril','5-maio','6-junho','7-julho','8-agosto','9-setembro','10-outubro','11-novembro','12-dezembro']

    lista_step = []
    pop_sound = None
    poppap_sound = None

    # Variavel para somar o len do arquivo Valores.txt
    find = ''
    def __init__(self,**kwargs):
        super(Menu,self).__init__(**kwargs)
        self.day = date.today().day
        self.pos_month = date.today().month
        # self.day = dia_teste   # =================== teste
        # self.pos_month = pos_mes  # ================ teste
        # self.data = Data()
        self.file_fechamento1 = 1
        self.file_fechamento2 = 0
        self.file_month = ''

        self.validng_month()

        # open or creats the month files
        # abre ou cria os arquivos mês
        try:
            open_file_month = open('month.txt','r', encoding='utf-8')
            self.file_month = open_file_month.read()

            step_spiner = open("step_spiner.txt","r", encoding="utf-8")
            self.step_spiner = step_spiner.read()

        except FileNotFoundError:
            # Só pra criar o arquivo spiner_month.txt , month.txt e step_spiner
            self.file_spiner = open('spiner_month.txt','a',encoding='utf-8')
            self.file_month = open('month.txt','w', encoding='utf-8')
            step_spiner = open('step_spiner.txt','w',encoding='utf-8')
            self.step_spiner = step_spiner.write(str(self.lista_month[self.pos_month - 1]))


            file_fechamento = open('fechamento.txt','w')
            file_porcento = open('porcentagen.txt','w')
            file_porcento.write(str(100))
            file_porcento.close()

            # Cria e escreve no arquivo month.txt e no arquivo spiner_month.txt
            self.file_month.write(str(self.lista_month[self.pos_month-1]))

            # adds in file sipener_month.txt
            # Adicionando ao arquivo sipner_month.txt
            self.file_spiner.write(self.lista_month[self.pos_month-1])

            # Aqui vira uma variavel para que se não estiver os arquivo na primeira vez que abre a variavel
            #-vai receber o valor da lista
            self.file_month = self.lista_month[self.pos_month - 1]

        try:
            fechamento = open("fechamento.txt", "r")
            self.file_fechamento1 = int(fechamento.read(2).strip())
            self.file_fechamento2 = int(fechamento.read(3).strip())
        except:
            fechamento = open("fechamento.txt","w")
            fechamento.write(str(1))


        if self.day > self.file_fechamento1:       # comparando o dia para abrir o mes seguinte
            file_month = open("month.txt",'w', encoding="utf-8")
            file_month.write(str(self.lista_month[self.pos_month - 1]))

        # get the directory of user
        # pegando o diretório do usuario
        self.dados_usuario = App.get_running_app().user_data_dir + '/'
        self.creat_folder()

    # Function to valid the month and change the folder of month
    # Funçã"o para validar o mês e mudar a pasta do mês
    def validng_month(self):
        lem = 0
        lista_json = []  # it to reading of file json

        self.lista_step.clear()
        # here change the month
        # aqui muda o mês
        if self.day >= int(self.file_fechamento1):
            if self.lista_month[self.pos_month - 1] != self.file_month or self.file_month != self.step_spiner :
                file_month = open('month.txt', 'w', encoding='utf-8')
                file_month.write(self.lista_month[self.pos_month - 1])
                file_month.close()

                # open file month to write in file "step_spiner
                file_month = open('month.txt','r', encoding='utf-8')

               # Here and to the app receive the month current
                file_step = open('step_spiner.txt', 'w', encoding='utf-8')
                file_step.write(str(file_month.read()))
                file_step.close()
            try:
                with open(self.dados_usuario + self.lista_month[pos_mes - 2] + '/' + 'SaveData.json','r') as dados_r:
                    lista_json = json.load(dados_r)
                    dados_r.close()
            except:
                pass
        # here close the fortnight of same month
        # aqui fecha a quinzena do mesmo mês
        if self.file_fechamento2 != 0:
            if self.day >= self.file_fechamento2:
                lem = 0
                l = None
                try:
                    # this "if" is to close the day of month
                    valor = open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "Valores.txt", 'r')
                    v = valor.readlines()
                    lem = len(v)
                except FileNotFoundError:
                    pass

                try:
                    lem_file_values = open(self.dados_usuario + self.lista_month[self.pos_month - 1] + '/' + 'lem_file_values.txt', 'r')
                    print(lem_file_values)
                    lem_file_values.read()
                    lem_file_values.close()
                    l = True
                except FileNotFoundError:
                    l = False

                try:
                    with open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "SaveData.json",'r') as json_dados:
                        self.lista_step = json.load(json_dados)
                except FileNotFoundError:
                    with open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "SaveData.json","w") as json_dados:
                        json_dados.close()
                except:
                    pass

                # if self.lista_step[lem:lem + 1] != []:
                if l == True:
                    pass
                else:
                    Clock.schedule_once(self.pop_mudar_mes, 1)


    def close_day(self,*args):
        lem = 0
        l = ''
        soma = 0
        v = None
        self.lista_step.clear()
        try:
            # this "if" is to close the day of month
            valor = open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "Valores.txt", 'r')
            v = valor.readlines()
            lem = len(v)
            for valores in v:
                soma += int(valores)
        except FileNotFoundError:
            pass

        try:
            with open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "SaveData.json",'r') as json_dados:
                self.lista_step = json.load(json_dados)
        except FileNotFoundError:
            with open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "SaveData.json","w") as json_dados:
                json_dados.close()
        except:
            pass

        if self.lista_step[lem:lem + 1] != []:
            pass
        else:
            file_porcento = open("porcentagen.txt","r")
            porcento = int(file_porcento.read())
            valor_porcento1 = soma * porcento / 100

            porcento2 = 100 - porcento
            valor_porcento2 = soma - valor_porcento1

            self.lista_step.append(f" Fechamento do dia ({self.day})     R$: {str(soma)}\n({porcento}% = R$: {valor_porcento1})  &  "
                                   f"({porcento2}% = R$: {valor_porcento2})")
            with open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "SaveData.json", 'w') as dados_json:
                json.dump(self.lista_step, dados_json)

            lem_file_values = open(self.dados_usuario + self.lista_month[self.pos_month - 1] + '/' + 'lem_file_values.txt','w')
            lem_file_values.write(str(f'{lem}\n'))
            lem_file_values.close()

            # the file "valores.txt" receiv of values 0 to an position of lista
            valor_0 = open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "Valores.txt", 'w')
            valor_0.write(f'{str(0)}\n')
            valor_0.close()

    def creat_folder(self):
        try:
            # Here creat the folder of monht
            path = os.mkdir(self.dados_usuario + str(self.file_month))

            # If exist the file then pass
            # Se existir o arquivo então passa
        except FileExistsError :
            pass
            # self.dados_usuario += file_month.read()

    def creat_file(self):
        # Criando os arquivo logo quando abrir o app
        if self.dados_usuario + self.lista_month[self.pos_mes - 1] + '/' + 'arq_eventos.txt' and self.dados_usuario + self.lista_month[self.pos_mes - 1] + '/' 'gastos.txt':
            pass
        else:
            data = open(self.dados_usuario + self.lista_month[self.pos_mes - 1] + '/' + 'arq_eventos.txt', 'w')
            Data().valor('gastos.txt')

        if self.dados_usuario + self.lista_month[self.pos_mes - 1] + '/' + 'SaveData.json':
            pass
        else:
            with open(self.dados_usuario + self.lista_month[self.pos_mes - 1] + '/' + 'SaveData.json', 'w') as data:
                data.close()

        # Tenta abrir o arquivo porcentagen para saber se existe se não existir cria um com um valor
        try:
            porcento = open('porcentagen.txt', 'r')
        except FileNotFoundError:
            porcento = open('porcentagen.txt', 'w')
            porcento.write('100')

    def on_pre_enter(self):
        # Window.bind(on_request_close=self.confirmar)
        self.validng_month()

        # that "try" and to when clear the tree of directory, not it give none error to returning screen menu
        # Esse try é para quando limpar a arvore de diretórios, não da nunhum erro ao voltar para tela menu
        try:
            self.creat_folder()
        except FileNotFoundError:
            pass

        # self.creat_file()

        # Adicionando o som do pupap carrega osom na variavel
        if self.pop_sound == None:                        # ==================== soudloader
            self.pop_sound = SoundLoader.load('poppap.mp3')

    def confirmar(self,*args,**kwargs):
        self.pop_sound.play()

        box = BoxLayout(spacing='10dp',orientation='vertical')
        pop = Popup(title='Deseja realmente sai?', size_hint=(None,None),
                    size=('200sp','150sp'),content=box)
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

    def pop_mudar_mes(self,*args,**kwargs):

        box = BoxLayout(spacing='10dp', orientation='vertical')
        pop = Popup(title=f'O mes fecha dia {int(self.file_fechamento2)} deseja fechalo?', size_hint=(None, None),
                    size=('200sp', '150sp'), content=box)
        box_bt = BoxLayout(spacing='13dp', size_hint_y=None, height='30sp')

        image = Image(source='image/atencao.png')

        bt_sim = Botaos(text='Sim', on_press=self.close_day, on_release=pop.dismiss)
        bt_nao = Botaos(text='Nao', on_release=pop.dismiss)

        box.add_widget(image)
        box_bt.add_widget(bt_sim)
        box_bt.add_widget(bt_nao)
        box.add_widget(box_bt)

        pop.open()
        return True


class Data:
    lista_month = ['1-janeiro', '2-fevereiro', '3-março', '4-abril', '5-maio', '6-junho', '7-julho', '8-agosto',
                   '9-setembro', '10-outubro', '11-novembro', '12-dezembro']
    ListaValor = 0
    list_get = []
    def __init__(self):
        from datetime import date
        self.ListaValor = Data.ListaValor
        self.data_day = date.today().day
        self.data_month = date.today().month
        self.data_year = date.today().year

        # self.data_month = pos_mes   # =================== teste

        file_month = open('step_spiner.txt','r', encoding='utf-8')
        self.month_step = file_month.read()

        if self.month_step == '':
            self.month_step = str(self.lista_month[self.data_month - 1])

        self.dados_usuario = App.get_running_app().user_data_dir + '/' + str(self.month_step) + '/'
        file_month.close()

    # Function to create and give am append in the file
    def valor(self,name,valores=''):
        if valores != '':
            self.dados_usuario = App.get_running_app().user_data_dir + '/' + str(self.month_step) + '/'
            arq = open(f'{self.dados_usuario +name}', 'a' , encoding='utf-8')
            arq.write(f'{valores}\n')
        else:
            pass

    def ler_valor(self,name):
        file_step = open('step_spiner.txt','r',encoding='utf-8')
        self.dados_usuario = App.get_running_app().user_data_dir + '/' + str(file_step.read()) + '/'
        try:
            len_file_values = open(self.dados_usuario + "lem_file_values.txt","r")
            len_file = len_file_values.read()
            len_file_values.close()
        except FileNotFoundError:
            pass

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
    lista_month = ['1-janeiro', '2-fevereiro', '3-março', '4-abril', '5-maio', '6-junho', '7-julho', '8-agosto','9-setembro', '10-outubro', '11-novembro', '12-dezembro']
    lista = []
    get = ''
    def __init__(self,**kwargs):
        super(Adicionar,self).__init__(**kwargs)
        self.data = (f'{str(self.data_day).zfill(2)}/{str(self.data_month).zfill(2)}/{str(self.data_year).zfill(4)}')

        self.day = self.data_day
        self.pos_month = self.data_month

        # self.day = dia_teste      # ================== teste day
        # self.pos_month = pos_mes  # ================== teste month

        try:
            fechamento = open("fechamento.txt", "r")
            self.file_fechamento1 = int(fechamento.read(2).strip())
            self.file_fechamento2 = int(fechamento.read(3).strip())
        except:
            pass

        # here is to when the month change, while the day is not larger than file_fechamento1 not change the directory
        # aqui é para quando o mês mudar, enquanto o dia não for maior que file_fechamento1 não muda o diretório
        if self.day < self.file_fechamento1:
            self.pos_month -= 1


        self.dados_usuario = App.get_running_app().user_data_dir + '/'+ self.lista_month[self.pos_month-1] +'/'

        if self.day > 5:        # ===============  day
            Menu().creat_folder()

    def on_pre_enter(self):
        self.get = self.ids.mensagen_add.text
        # self.dados_usuario = App.get_running_app().user_data_dir + '/'
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_keyboard=self.teclas)
        # self.save_data()

    def save_data(self):
        modelo = self.ids.text_modelo.text.capitalize()
        local = self.ids.text_local.text.capitalize()
        valor_int = self.ids.text_valor.text
        eventos = self.ids.text_eventos.text
        gastos = 0

        if self.ids.text_gastos.text != '':
            try:
                gastos = str(int(self.ids.text_gastos.text))
            except ValueError:
                self.ids.mensagen_gastos.text = 'Digitos invalido no campo gastos "Só numeros"'
                Clock.schedule_once(self.retorna_mesagens,5)
        else:
            gastos = 0

        if gastos != 0 and eventos != '':
            # criando arquivo para os eventos de gastos
            arq_eventos = open(self.dados_usuario + 'arq_eventos.txt', 'a')
            arq_eventos.write(f'{eventos}  {gastos}\n')
            self.ids.mensagen_gastos.text = 'Eventos gastos salvos com sucesso!'
            self.ids.mensagen_add.text = self.get
            self.ids.text_eventos.text = ''
            self.ids.text_gastos.text = ''
            Clock.schedule_once(self.retorna_mesagens, 5)

        elif gastos != 0 and eventos == '':
            self.ids.mensagen_gastos.text = 'Campo Eventos não preenchidos'
            self.ids.mensagen_add.text = self.get
            Clock.schedule_once(self.retorna_mesagens, 5)

        # elif gastos != 0 and eventos != '':
        #     self.ids.mensagen_sobra.text = 'Digitos invalido no campo gastos "Só numeros"'
        elif eventos != '' and gastos == 0:
            self.ids.mensagen_gastos.text = 'Campo gastos não preenchidos '
            Clock.schedule_once(self.retorna_mesagens, 5)
            self.ids.mensagen_add.text = self.get

        if valor_int != '':
            if 'a'<= valor_int <='z':
                self.ids.mensagen_add.text = 'O valor só pode conter números!'
                Clock.schedule_once(self.retorna_mesagens,5)
            else:
                try:
                    # Aqui é para a self.lista receber os conteudos do arquivo json
                    with open(self.dados_usuario+'/'+'SaveData.json', 'r') as dados:
                        self.lista = json.load(dados)  # Aqui é para a lista sempre receber o conteudo do arquivo json primeiro
                        self.lista.append(f'{self.data:<25} {modelo:<30} {local:<25} {float(valor_int):>8} R$')
                        self.ids.text_modelo.text = ''
                        self.ids.text_local.text = ''
                        self.ids.text_valor.text = ''

                except:
                    self.lista.append(f'{self.data:<25} {modelo:<30} {local:<25} {float(valor_int):>8} R$')
                    # self.ids.mensagen_add.text = 'Nada foi salvo'
                    self.get = self.ids.mensagen_add.text

                try:
                    # criando um arquivo json e recebendo os conteudo da lista
                    with open(self.dados_usuario+'/'+'SaveData.json', 'w') as data:
                        json.dump(self.lista, data)
                        self.ids.text_modelo.text = ''
                        self.ids.text_local.text = ''
                        self.ids.text_valor.text = ''

                        try:
                            # criando um arquivo Valores
                            self.valor('Valores.txt', str(int(valor_int)))
                        except ValueError:
                            pass
                        self.ids.mensagen_add.text = 'Arquivos salvos com sucesso!'
                        self.get = self.ids.mensagen_add.text
                        Clock.schedule_once(self.retorna_mesagens,5)
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


    def retorna_mesagens(self,*args):
        self.ids.mensagen_gastos.text = 'Adicione os gastos com eventos ocorridos e\n valores.'
        self.ids.mensagen_add.text = 'Adicione a cima o modelo do carro/moto, \nlocal e valor'

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
    sem_botao = False
    l = 0
    def __init__(self,**kwargs):
        super(Visualizar,self).__init__(**kwargs)
        self.box = Box()
        self.lista = []
        self.lista_valores = []
        self.soma = Visualizar.soma

        self.day = self.data_day

        # self.day = dia_teste   # ============= teste day

        file_step_spiner = open('step_spiner.txt', 'r', encoding='utf-8')
        self.file_step_spiner = file_step_spiner.read()

        # pegando o diretório do usuario
        self.dados_usuario = App.get_running_app().user_data_dir + '/' + str(self.file_step_spiner) + '/'

        self.texto = str('{:<30} {:<30} {:<30} {:>6}'.format('Data','Modelo','Local','Valor'))

    def add(self):
        soma_atual = 0
        # para tirar os botães
        try:
            sem_botao = open(self.dados_usuario + "lem_file_values.txt", "r")
            self.l = int(sem_botao.read())
            self.sem_botao = True
        except FileNotFoundError:
            self.sem_botao = False

        open_spiner = open('step_spiner.txt', 'r', encoding='utf-8')
        step_spiner = str(open_spiner.read())
        open_spiner.close()

        self.month = open('month.txt', 'r', encoding='utf-8')
        month = self.month.read()

        try:
            with open(self.dados_usuario+'SaveData.json','r',encoding='utf-8') as data:
                self.lista.clear()
                self.lista = json.load(data)
        except FileNotFoundError:
            try:
                with open(self.dados_usuario+'SaveData.json', 'w') as data:
                    data.close()
            except FileNotFoundError:
                pass
        except json.decoder.JSONDecodeError:
            pass

        selecao = []
        if self.sem_botao == True:
            # Éssa parte é para pegar os dias que ja foram fechado
            for valor in self.lista[0:int(self.l) + 1]:
                selecao.append(valor)
            del(self.lista[0:int(self.l) + 1])
        else:
            pass

        # hare is to add the values in box correct
        # Aqui é para adicionar os valores no Box corretos
        self.lista.reverse()
        for num, linha in enumerate(self.lista):
            if step_spiner.lower() != month :
                self.ids.coteiner.add_widget(BiforeTotal(texto=str(linha)))
            else:
                self.ids.coteiner.add_widget(Box(label=str(linha)))

        if self.sem_botao == True:
            # Aqui adiciona os dias que já foram fechado no box
            selecao.reverse()
            for valor in selecao:
                self.ids.coteiner.add_widget(BiforeTotal(texto=str(valor)))

    def on_pre_enter(self):
        # colocando texto formatado
        self.ids.super_modelo_text.text = self.texto

        self.file_step_spiner = open('step_spiner.txt', 'r', encoding='utf-8')

        # pegando o diretório do usuario
        self.dados_usuario = App.get_running_app().user_data_dir + '/' + str(self.file_step_spiner.read()) + '/'

        Window.bind(on_keyboard=self.voltar)

        self.add()

        try:
            self.ids.total_valor.text =''
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
        lem = 0

        try:
            file_lem_values = open(self.dados_usuario+"lem_file_values.txt","r")
            lem = file_lem_values.read()
        except FileNotFoundError:
            pass

        try:
            self.lista.clear()
            with open(self.dados_usuario+'SaveData.json','r',encoding='utf-8')as get_json:
                self.lista = json.load(get_json)
            self.ids.coteiner.remove_widget(self.root)

            pos = self.lista.index(texto)
            self.lista.remove(texto)

            with open(self.dados_usuario+'SaveData.json','w',encoding='utf-8') as save_json:
                json.dump(self.lista, save_json)

            # opening file Valores to get the valores
            # Abrindo o arquivo Valores para obter os valores
            arq_valores = open(self.dados_usuario+'Valores.txt','r')

            # Adiction the values of file in lista
            # Adicionando os valores do arquivo na lista
            for valor in arq_valores.readlines():
                self.lista_valores.append(valor)
            arq_valores.close()

            # Remuve the values of lista in position of file json "pos"
            # Removendo o valor da lista na posição do arquivo json "pos"
            try:
                del(self.lista_valores[pos-int(lem)])
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
        self.dados_usuarios = App.get_running_app().user_data_dir + '/'

    def on_pre_enter(self):

        open_spiner = open('step_spiner.txt', 'r', encoding='utf-8')
        file_spiner = str(open_spiner.read())

        self.dados_usuario = self.dados_usuarios + file_spiner + '/'
        open_spiner.close()

        self.month = open('month.txt','r',encoding='utf-8')
        month = self.month.read()

        # aqui a TelaTotal recebe a porcentagen do arquivo
        try:
            arq_porcentagen = open('porcentagen.txt', 'r')
            self.main_porcentagen = arq_porcentagen.read()
            arq_porcentagen.close()
        except:
            self.main_porcentagen = 100

        # trying open file gastos.txt  se não existir  a variavel arquiv sera criada com espaço em branco
        try:
            arquiv = self.ler_valor('gastos.txt')
        except FileNotFoundError:
            arquiv = 0

        # Opening file arq_eventos.txt to read the amount of events
        # abrindo arquivo arq_eventos.txt para ler a quantidades de eventos
        try:
            add_arq = open(self.dados_usuario+'arq_eventos.txt', 'r')
            self.ids.gastos.clear_widgets()
            for iten in add_arq.readlines():
                if file_spiner.lower() != month:
                    self.ids.gastos.add_widget(BiforeTotal(texto=str(iten)))
                else:
                    self.ids.gastos.add_widget(Box_Total(label=str(iten)))
        except FileNotFoundError:
            add_arq = ''

        try:
            # Passando a variavel do arquiv com self.ler_valor('gastos.txt') para somas
            self.ids.total_gastos.text = str(f'Total gastos: {float(arquiv)}')
        except TypeError:
            pass

        # Trying open the file valores.txt to sum if not exist it will be create
        # Tentando abrir o arquivo Valores.txt para soma se não existir será criado
        try:
            s_v = float(self.ler_valor('Valores.txt'))
            self.ids.Valor_soma.text = f'R$ {s_v:.1f}'
        except FileNotFoundError:
            self.valor('Valores.txt')
        except TypeError:
            self.ids.Valor_soma.text = '0'

        # Create and showing thes division ofs percentagen and aditioning in label
        # Criando e Mostrando as divisões das porcentagen e adicionando no label
        percentual_main = float(self.percentuais() * int(self.main_porcentagen) / 100)
        percentual_sobra = float(self.percentuais() - percentual_main)
        self.ids.label_main.text = f'{self.main_porcentagen} %'
        self.ids.label_sobra.text = f'{100-int(self.main_porcentagen)} %'

        percentual_gasto_main = float((int(self.main_porcentagen) * int(arquiv)) / 100)
        percentual_gasto_sobra = float(arquiv - percentual_gasto_main)

        self.atualizar_rst()

        # Here format the values
        # Aqui formata os valores
        v_m = float(percentual_main)
        v_s = float(percentual_sobra)
        self.ids.valor_sobra.text = f'{v_s:.2f}'
        self.ids.valor_main.text = f'{v_m:.2f}'

    def on_pre_leave(self):
        self.ids.total_gastos.text = ''
        self.ids.gastos.clear_widgets()

    def popap(self, root, *args):
        self.root_bt = root

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

    def atualizar_rst(self):

        # trying open file gastos.txt  se não existir  a variavel arquiv sera criada com espaço em branco
        try:
            arquiv = self.ler_valor('gastos.txt')
        except FileNotFoundError:
            arquiv = 0

        # Create and showing thes division ofs percentagen and aditioning in label
        # Criando e Mostrando as divisões das porcentagen e adicionando no label
        percentual_main = float(self.percentuais() * int(self.main_porcentagen) / 100)
        percentual_sobra = float(self.percentuais() - percentual_main)
        self.ids.label_main.text = f'{self.main_porcentagen} %'
        self.ids.label_sobra.text = f'{100 - int(self.main_porcentagen)} %'

        percentual_gasto_main = float((int(self.main_porcentagen) * int(arquiv)) / 100)
        percentual_gasto_sobra = float(arquiv - percentual_gasto_main)

        self.ids.porc_gasto.text = f"""
.. _Total:
Porcentagen dos gastos
==========

                Total_: R$ {arquiv:.1f}
**[size=30]{self.main_porcentagen}%**   =  {percentual_gasto_main}[/size] 

**[size=30]{100 - int(self.main_porcentagen)}%**  =  {percentual_gasto_sobra}[/size]

"""

    def deletar(self,*args):
        texto = self.root_bt.ids.texto.text
        try:
            # Excluindo dos arquivos eventos e gastos
            self.ids.gastos.remove_widget(self.root_bt)

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


class BiforeTotal(BoxLayout):
    def __init__(self,texto='',**kwargs):
        super(BiforeTotal,self).__init__(**kwargs)
        self.ids.biforetotal.text = texto

class Box(BoxLayout):
    # Class que tem um BoxLayout com a Label para inserir texto
    lista = []
    lista_valores = []
    def __init__(self,label='',**kwargs):
        super(Box,self).__init__(**kwargs)
        self.ids.texto.text = label
        self.label = label

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
        Builder.load_string(open('verba.kv', encoding='utf-8').read())
        return Gerenciador()


if __name__ == '__main__':
    ControleVerbaApp().run()
