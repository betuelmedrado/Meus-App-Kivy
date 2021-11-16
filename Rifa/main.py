

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFillRoundFlatIconButton, MDIconButton, MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window


from datetime import date
import time
from random import choice


import os
import json
import sqlite3


# Here is to when press the keyboar elevation the textinput
Window.softinput_mode = 'below_target'

# import sys
# sys.setrecursionlimit(5000)


# Window.size = 350,600

class Manager(ScreenManager):
    pass

class Date:
    def __init__(self):
        self.day = date.today().day
        self.month = date.today().month
        self.year = date.today().year


class Botao(BoxLayout):
    def __init__(self,label='',*args,**kwargs):
        super().__init__(**kwargs)
        self.ids.botao.text = label
        self.label = label

    def press_button(self):
        self.num_button = self.ids.botao.text
        self.ids.botao.background_color = 1,0,0,1
        Clock.schedule_once(self.checking,15)

    def checking(self,*args):
        check = self.open_databese()

        if check == []:
            self.ids.botao.background_color = 1,1,1,1
        else:
            pass

    # opening the data base to check and change the color of button
    def open_databese(self):
        conn = sqlite3.connect('numberTable.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rifa WHERE Number == "'+str(self.num_button)+'" ')

        return cursor.fetchall()

    def popup(self,msg,*args):

        box = BoxLayout(orientation='vertical')


        pop = Popup(title='Nome da pessoa', size_hint=(None, None),
                    size=('300dp', '400dp'), content=box)

        bt = MDIconButton(pos_hint=({'center_x':.5}),icon='credit-card-refund' ,on_release=pop.dismiss)

        box.add_widget(Content(msg.text))
        box.add_widget(bt)


        try:
            pop.show()
        except AttributeError:
            pop.open()

        return msg

class BotaoRed(BoxLayout):
    def __init__(self,msg,*args,**kwargs):
        super().__init__(**kwargs)
        self.ids.botaored.text = str(msg)

    def popup_person(self,number,*args,**kwargs):

        self.num = number.text

        box = BoxLayout(orientation='vertical')
        box_button = BoxLayout(size_hint_y=(.20))
        pop = Popup(title='Informações',size_hint=(None,None),
                    size=('300dp','400dp'), content=box)

        bt = MDIconButton(icon='credit-card-refund',pos_hint=({'center_x':.1}),on_release=pop.dismiss)
        bt_exclud = MDIconButton(icon='delete-forever',pos_hint=({'center_x': 1}),on_release=self.delet_edit)

        box_button.add_widget(Widget())
        box_button.add_widget(bt)
        box_button.add_widget(Widget())
        box_button.add_widget(bt_exclud)

        box.add_widget(ContentRed(number.text))
        box.add_widget(box_button)

        try:
            pop.show()
        except AttributeError:
            pop.open()

    def delet_edit(self,*args):
        try:
            conn = sqlite3.connect('numberTable.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM rifa WHERE Number == "'+self.num+'"')
            conn.commit()
            Grade().snackbar('Nome excluido com sucesso!')
            Grade().on_pre_enter()
        except:
            Grade().snackbar('Não foi possivel!')


    def exit(self):
        self.popup_person.dismiss()

class ContentRed(BoxLayout):

    def __init__(self,txt='',**kwargs):
        super().__init__(**kwargs)

        # Here get the number fo person table
        self.number_person = txt

        self.data_pesor()


    def data_pesor(self):

        conn = sqlite3.connect('numberTable.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rifa WHERE Number == "'+ self.number_person +'" ;')

        content = cursor.fetchall()

        try:
            self.ids.person.text = f'{str(content[0][1])} - {str(content[0][2])}'
            self.ids.pago.text = f'[size={"17dp"}]Foi pago?[/size]\n\n' \
                                 f'[color=#4682B4][size={"30dp"}][b]{str(content[0][3])}[/b][/size][/color]\n'
            if content[0][3] == 'Sim':
                self.ids.check_sim.active = True
            else:
                self.ids.check_nao.active = True
        except:
            print('erro data_pesor content_red!')


    def change_paid(self,msg):
        conn = sqlite3.connect('numberTable.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE rifa SET Paid = "'+msg+'"  WHERE Number == "'+str(self.number_person)+'" ')
        conn.commit()

        self.data_pesor()


class Content(BoxLayout):
    def __init__(self,label='',*args,**kwargs):
        super().__init__(**kwargs)
        self.ids.id_namber.text = label
        self.label = label

    def check(self,msg):
        self.pago = str(msg.text)

    def aperto(self,*args,**kwargs):
        # b = Botao()
        # b.teste()
        # grade = Grade()
        MDApp.get_running_app().root.curretn = 'grade'


    def get_content(self):
        person = self.ids.person.text
        number = self.ids.id_namber.text
        try:
            self.pago
        except AttributeError:
            pass

        active = True

        conn = sqlite3.connect('numberTable.db')
        cursor = conn.cursor()
        if person != '':
            try:
                cursor.execute('INSERT INTO rifa("Person", "Number", "Paid", "Activate")'
                               'VALUES("'+str(person.title())+'" , "'+number+'" , "'+str(self.pago)+'" , "'+str(active)+'" ) ; ')
                Grade().snackbar('Salvo com sucesso!')
                Grade()
            except AttributeError:
                Grade().snackbar('Informe se ja foi pago ou não!')
            except sqlite3.IntegrityError:
                Grade().snackbar('Esse numero já foi escolhido!')

            conn.commit()
        else:
            Grade().snackbar('Não foi informado nenhum nome!')


class Login(Screen):

    content = {}

    def __init__(self,*args,**kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.creat_db()
        self.creat_json()
        self.get_name()
        Clock.schedule_once(self.await_nome,1)

    def await_nome(self, *args):
        try:
            nome = self.read_json()
            self.ids.text_nome_login.text = str(nome[0]['Nome'])
        except IndexError:
            pass


    def on_leave(self):
        self.ids.warning.text = ''
        self.ids.se_cadastre.text = ''
        self.ids.icon.icon = ''

    def if_go_register(self):
        table = self.read_json()

        if table == []:
            MDApp.get_running_app().root.current = 'register'
        else:
            self.snackbar('já existe uma tabela só pode conter uma!')

    def logar(self):
        nome = self.ids.text_nome_login.text
        loga = self.read_json()

        if loga == []:
            self.ids.warning.text = 'Nenhuma tabela encontrada!'
            self.ids.se_cadastre.text = 'Crie uma tabela!'
            self.ids.icon.icon = 'arrow-right'
        elif nome == '':
            self.ids.warning.text = 'Campo vazil'
            self.ids.se_cadastre.text = 'Crie uma tabela!'
            self.ids.icon.icon = 'arrow-right'
        else:
            lista = []
            for nomes in loga:
                if nomes['Nome'] == nome.title():
                    self.get_name(nomes)
                    lista.append(nomes)
                    MDApp.get_running_app().root.current = 'grade'
                    self.ids.warning.text = ''
                    self.ids.se_cadastre.text =''
                    self.ids.icon.icon = ''
            if lista == []:
                self.ids.warning.text = 'Nome não cadastrado '
                self.ids.se_cadastre.text = 'Crie uma tabela!'
                self.ids.icon.icon = 'arrow-right'

    def creat_db(self):
        conn = sqlite3.connect('numberTable.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS rifa("ID" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , "Person" TEXT NOT NULL , "Number" INTEGER  UNIQUE NOT NULL , "Paid" TEXT , "Activate" TEXT);')


    def read_json(self):
        with open('rifa.json','r',encoding='utf-8') as json_content:
            self.lista = json.load(json_content)
        return self.lista

    def creat_json(self):
        try:
            with open('rifa.json','r',encoding='utf-8') as rifa:
                json.load(rifa)
        except FileNotFoundError:
            with open('rifa.json','w') as rifa:
                json.dump([],rifa,indent=2)
        try:
            with open('award.json','r') as award:
                json.load(award)
        except FileNotFoundError:
            with open('award.json','w') as award:
                json.dump([],award)

    def get_name(self,msg=''):
        with open('get_name.json','w',encoding='utf-8') as get:
            json.dump(msg,get,indent=2)

    def snackbar(self,msg):
        snack = Snackbar(text=str(msg))
        try:
            snack.open()
        except AttributeError:
            snack.show()

    def snackbar_delet(self,msg='Deseja excluir a tabgela!',*args,**kwargs):

        # Here is a class
        # Aqui é uma classe
        try:
            snackbar = Snackbar(
                text=str(msg),
                snackbar_x="10dp",
                snackbar_y="10dp",
            )
            snackbar.duration=5
            snackbar.size_hint_x = (
                                       Window.width - (snackbar.snackbar_x * 2)
                                   ) / Window.width
            snackbar.buttons = [

                MDFlatButton(
                    text="Excluir",
                    # text_color=(1,0,0,1),
                    on_press=self.calling,
                    on_release=snackbar.dismiss,
                ),
                MDFlatButton(
                    text="CANCEL",
                    # text_color=(1,0,0,1),
                    on_release=snackbar.dismiss,
                ),
            ]
            snackbar.show()
        except AttributeError:
            snackbar.open()

    def calling(self,*args):
        Snack().delet_table()

class Snack:

    def delet_table(self):
        try:
            with open('rifa.json','w') as rifa:
                json.dump([],rifa)

            with open('get_name.json','w') as get_name:
                json.dump('',get_name)

            with open('award.json','w') as award:
                json.dump([],award)

            try:
                os.remove('winner.json')
            except FileNotFoundError:
                pass

            self.delet_db()

            self.snack_warning('Tabela excluida com sucesso!')
        except:
            self.snack_warning('Não foi possivel excluir a tabela!')


    def delet_db(self,*args,**kwargs):
        conn = sqlite3.connect('numberTable.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM rifa')
        conn.commit()

    def snack_warning(self,msg):
        snackbar = Snackbar(text=str(msg))
        snackbar.animation_dir = 'Top'
        try:
            snackbar.show()
        except AttributeError:
            snackbar.open()


class Register(Screen,Date):

    dict = {}
    lista = []

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def select_val_table(self,msg):
        self.active_cinquenta = self.ids.check_cinquenta.active
        self.active_cem = self.ids.check_cem.active

        self.dict['Quantidade'] = msg.text
        return msg

    def return_login(self):
        MDApp.get_running_app().root.current = 'login'

    def read_json(self):
        with open('rifa.json','r',encoding='utf-8') as json_content:
            self.lista = json.load(json_content)
        return self.lista

    def comparacao(self):
        # comparing if exists name equal in list
        # comparando se existe nome iguais na lista "Mais por inquanto não esta usando"
        nome = str(self.ids.cadastro_nome.text)
        ler = self.read_json()

        informar = False

        for n in ler:
            if nome.title() == n['Nome']:
                informar = True
            else:
                pass
        return informar

    # Validing date
    def validing_date(self,day,month,year):

        try:
            if day == '' or month == '' or  year == '':
                self.snackbar('Campos data vazio!')
            elif int(year) < int(self.year):
                self.snackbar('Ano abaixo do atual!')
            elif int(self.month) == 1 and int(day) > 31 or int(self.month) == 3 and int(day) > 31 or int(self.month) == 5 and int(day) > 31 or int(self.month) == 7 and int(day) > 31 or int(self.month) == 8 and int(day) > 31 or int(self.month) == 10 and int(day) > 31 or int(self.month) == 12 and int(day) > 31:
                self.snackbar('Dia invalido esse mês vai até 31')
            elif int(self.month) == 2 and int(day) > 29:
                self.snackbar('Dia invalido Fevereiro vai até "29" !')
            elif int(self.month) == 4 and int(day) > 30 or int(self.month) == 6 and int(day) > 30 or int(self.month) == 9 and int(day) > 30 or int(self.month) == 11 and int(day) > 30 :
                self.snackbar('Dia invalido esse mês vai até "30" ')
            elif int(month) > 12:
                self.snackbar('Mês invalido!')
            else:
                if len(day) > 2 or len(day) < 0 or len(month) > 2 or len(month) < 0 or len(year) > 4 or len(year) < 4:
                    self.snackbar('Campos data invalido')
                    return False
                else:
                    return True
        except ValueError:
            self.snackbar('Só é válido numeros nos campos data')


    def register(self):
        self.active_cinquenta = self.ids.check_cinquenta.active
        self.active_cem = self.ids.check_cem.active
        award = self.ids.premio.text

        day = self.ids.day.text
        month = self.ids.month.text
        year = self.ids.year.text

        valid_date = self.validing_date(day,month,year)

        if valid_date == True:
            self.dict['Dia'] = day
            self.dict['Mês'] = month
            self.dict['Ano'] = year

            ativo = self.comparacao()

            if ativo:
                self.snackbar('Esse nome já tem uma tabela!')
            else:
                nome = str(self.ids.cadastro_nome.text)

                if nome == '' and self.active_cinquenta == True or nome == '' and self.active_cem == True :
                    self.snackbar('Nome não informado!')
                elif nome != '' and self.active_cinquenta == False and self.active_cem == False:
                    self.snackbar('Escolha um tipo de tabela!')
                elif nome == '' and self.active_cinquenta == False and self.active_cem == False:
                    self.snackbar('Escolha um tipo de tabela e insira um nome!')
                else:
                    self.read_json()
                    self.dict["Nome"] = nome.title()
                    self.dict["Premio"] = str(award)
                    self.lista.append(self.dict)
                    self.save_json()
                    self.save_name(self.dict['Quantidade'],nome)
                    MDApp.get_running_app().root.current = 'grade'

    def save_json(self):
        with open('rifa.json','w',encoding='utf-8') as save:
            json.dump(self.lista,save, indent=2)

    def save_name(self,quant, nome):
        get_content = {'Quantidade':quant, 'Nome': nome}
        with open('get_name.json','w') as name:
            json.dump(get_content, name)


    def snackbar(self, msg):
        self.snack = Snackbar(text=str(msg))
        try:
            self.snack.open()
        except AttributeError:
            self.snack.show()

class Grade(Screen):

    lista = {}
    lista_chosen = []
    cont = 5
    def __init__(self,*args,**kwargs):
        super().__init__(**kwargs)

        self.day = date.today().day
        self.month = date.today().month
        self.year = date.today().year


    # Here is only to test
        # self.day = 27
        # self.month = 9
        # self.year = 2021

    def on_pre_enter(self):

        self.chosen()
        self.get_name()
        self.build_grid()
        self.if_winner()

    def on_leave(self):
        self.lista_chosen = []

    def if_winner(self):
        # see if already completed the table to send the mesagem
        # vendo se já completou a tabela para enviar a mensagem
        length_chose = self.get_name()
        length_table = self.chosen()


        if len(length_table) >= int(length_chose['Quantidade']):
            try:
                with open('winner.json','r') as win:
                    json.load(win)
            except FileNotFoundError:
                self.snackbar('A Premiação já pode ser aberta!')

        active = False
        try:
            with open('winner.json','r') as win:
                json.load(win)
            active = True
        except FileNotFoundError:
            pass

        return active

    # function to get number chosen
    def get_name(self):
        with open('get_name.json','r') as get:
            self.lista = json.load(get)
        return self.lista

    # Function to create the table
    def build_grid(self,*args,**kwargs):
        self.ids.box.clear_widgets()
        self.grid = GridLayout(cols=10, spacing=2)

        nome = self.lista["Nome"]
        valor = int(self.lista["Quantidade"])
        self.ids.name_table.title = str(nome+' - '+str(valor))
        active = self.if_winner()

        if valor == 50:
            self.grid.cols = 5

        for c in range(valor+1):
            if c == 0:
                pass
            else:
                if c in set(self.lista_chosen):
                    self.grid.add_widget(BotaoRed(msg=str(c)))
                else:
                    if self.if_winner() == True:
                        self.grid.add_widget(Botao(label=str(c), disabled=True))
                    else:
                        self.grid.add_widget(Botao(label=str(c)))

        self.ids.box.add_widget(self.grid)

    def return_login(self):
        MDApp.get_running_app().root.current = 'login'

    def go_person(self,*args,**kwargs):
        conn = sqlite3.connect('numberTable.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rifa')

        # geting the amount of person
        # obtendo a quantidade de pessoas
        cont = []

        lista = []
        for item in cursor.fetchall():
            lista += (item[1], item[2], item[3])
            cont.append(item[1])

        data_table = MDDataTable(
            column_data=[
                ("Nome", dp(20)),
                ("Numero", dp(20)),
                ("Pago?", dp(20))
            ],
            row_data=[
                lista
            ],
        )

        box = BoxLayout(orientation='vertical')
        pop = Popup(title=f'{len(cont)} - Participantes', content=box)
        bt = MDIconButton(icon='credit-card-refund',pos_hint=({'cente_x': .5}),on_release=pop.dismiss)
        box.add_widget(data_table)
        box.add_widget(bt)
        pop.open()

    def chosen(self):
        lista_chosen = []

        conn = sqlite3.connect('numberTable.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Number FROM rifa')
        # cursor.execute('SELECT * FROM rifa')

        chosen_button = cursor.fetchall()
        for iten in chosen_button:
            self.lista_chosen.append(iten[0])

        return set(self.lista_chosen)

    # this method is to the do cont
    # Esse Método é para fazer a contagem
    def time(self,*args):
        Clock.schedule_once(self.times,1)
        Clock.schedule_once(self.clear_screen,1.7)

    # Complemento da class time
    def times(self,*args):
        self.box = BoxLayout()
        label = Label(text=str(self.cont), font_size=('400dp'), bold=True,
                      color=(0,0,1,1))
        label.outline_color = (0,0,0,1)
        label.outline_width = 5
        self.box.add_widget(label)
        self.add_widget(self.box)

        self.cont -= 1
        if self.cont < 0:
            pass
        else:
            self.time()

        if self.cont < 0 :
            self.entry_award()

    # To clear the box of count
    # Para limpar a caixa de contagem
    def clear_screen(self,*args):
        self.box.clear_widgets()

    def calling_award(self,**kwargs):
        date = {}

        with open('rifa.json','r') as content:
            date = json.load(content)

        day = int(date[0]['Dia'])
        month = int(date[0]['Mês'])
        year = int(date[0]['Ano'])

        tamanho = date[0]['Quantidade']

        # seeing if already completad the table
        # vendo se já completou a tabela
        length_table = self.chosen()

        if_win = self.if_winner()

        if if_win == False:
            if int(self.day) >= int(day) and int(self.month) >= int(month) and int(self.year) >= int(year) or int(self.month) > int(month) and int(self.year) >= int(year) or int(self.year) > int(year):
                self.pop_award()
            elif len(length_table) >= int(tamanho):
                self.pop_award()
            else:
                self.snackbar(f'O premio só vai ser liberado na data correta! {str(day).zfill(2)}/{str(month).zfill(2)}/{year}')
        else:
            self.entry_award()


    def entry_award(self,*args):
        MDApp.get_running_app().root.current = 'award'

    def snackbar(self,msg,*args,**kwargs):
        snack = Snackbar(text=str(msg),duration=(5))

        try:
            snack.open()
        except AttributeError:
            snack.show()

    def pop_award(self,*args):

        box = BoxLayout(orientation='vertical')
        box_button = BoxLayout(spacing='11dp')
        label = Label(text='Cuidado Você está preste a abrir a rifa!\nDesejá abrir? ',color=(1,0,0,1))

        pop = Popup(title='Deseja abrir a rifa!',size_hint=(None,None), size=('300dp','200dp'),content=box)

        bt_sim = Button(text='Sim',on_press=self.time, on_release=pop.dismiss)
        bt_nao = Button(text='Não', on_release=pop.dismiss)

        box.add_widget(label)
        box_button.add_widget(bt_sim)
        box_button.add_widget(bt_nao)
        box.add_widget(box_button)

        pop.open()

class Award(Screen):

    lista = []

    def get_content(self):
        conn = sqlite3.connect('numberTable.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rifa' )

        return cursor.fetchall()

    def rafflo(self):
        numero = self.get_content()

        for number in numero:
            self.lista.append(number[2])

        try:
            escolhendo = choice(self.lista)
            num = self._winner(escolhendo)
            self.open_db(num)
        except IndexError:
            Grade().snackbar('Nenhum numero informado!')

    def open_db(self,num):
        conn = sqlite3.connect('numberTable.db')
        cursor = conn.cursor()
        content = cursor.execute('SELECT * FROM rifa WHERE "Number" == "'+str(num)+'" ')
        c = content.fetchall()

        with open('rifa.json','r') as award:
            premio = json.load(award)

        self.ids.winner.text = f'{c[0][1]} \n\n [size={"30dp"}]Numero sorteado[/size] \n\n {c[0][2]} '
        self.ids.award.text = f'[size={"30dp"}]Premiação[/size]\n[b]{premio[0]["Premio"]}[/b]'

    def _winner(self,msg):

        # escolheu um numero e escreveu no arquivo e não vai escrever mais no arquivo
        try:
            with open('winner.json','r') as win:
                winner = json.load(win)
                return winner
        except FileNotFoundError:
            with open('winner.json','w') as win:
                json.dump(msg,win)
                return msg

    def return_home(self):
        MDApp.get_running_app().root.current = 'grade'

    def on_pre_enter(self):
        self.rafflo()


class RifaApp(MDApp):

    def build(self):
        Builder.load_string(open('rifas.kv', encoding='utf-8').read())
        self.theme_cls.primay_palette = 'BlueGrey'
        self.theme_cls.accent_palette = 'Yellow'

        return Manager()

RifaApp().run()