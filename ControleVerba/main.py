#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy import require
require('1.9.1')
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp

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
from kivy.properties import ListProperty, ObjectProperty
# from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.lang.builder import Builder
import json
import os
import shutil
from kivy.clock import Clock
from datetime import date


# internal commit: position and  error

# Window.size = 350, 600

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

# dia_teste = 5
# mes_teste = 7

class Dados:
    lista_month = ['1-janeiro', '2-fevereiro', '3-março', '4-abril', '5-maio', '6-junho', '7-julho', '8-agosto',
                   '9-setembro', '10-outubro', '11-novembro', '12-dezembro']
    ListaValor = 0
    list_get = []
    def __init__(self):
        super().__init__()
        from datetime import date
        self.ListaValor = Dados.ListaValor
        self.data_day = date.today().day
        self.data_month = date.today().month
        self.data_year = date.today().year

        # self.data_day = dia_teste     # =================== teste
        # self.data_month = mes_teste   # =================== teste


        try:
            file_month = open('step_spiner.txt','r', encoding='utf-8')
            self.month_step = file_month.read()
        except FileNotFoundError:
            self.month_step = self.lista_month[self.data_month - 1]
            file_month = None

        if self.month_step == '':
            self.month_step = str(self.lista_month[self.data_month - 1])

        self.dados_usuario = MDApp.get_running_app().user_data_dir + '/' + str(self.month_step) + '/'

        try:
            file_month.close()
        except:
            pass

    # Function to create and give am append in the file
    def valor(self,name_arq, valores=''):
        if valores != '':
            self.dados_usuario = MDApp.get_running_app().user_data_dir + '/' + str(self.month_step) + '/'
            arq = open(f'{self.dados_usuario + name_arq}', 'a' , encoding='utf-8')
            arq.write(f'{valores}\n')
        else:
            pass

    def ler_valor(self,name):
        file_step = open('step_spiner.txt','r',encoding='utf-8')
        self.dados_usuario = MDApp.get_running_app().user_data_dir + '/' + str(file_step.read()) + '/'

        try:
            arq = open(f'{self.dados_usuario + name}','r')
            arq.readline(0)

            self.ListaValor = 0
            self.list_get.clear()

            for linha in arq:
                try:
                    self.list_get.append((float(linha) ))
                except:
                    pass
                despejo = self.list_get
                self.ListaValor = sum(despejo)

            arq.close()
            return self.ListaValor
        except FileNotFoundError:
            pass

    def read_json(self,arq):
        try:
            with open(self.dados_usuario + arq, 'r', encoding='utf-8') as data:
                # self.lista.clear()
                return json.load(data)
        except FileNotFoundError:
            return list('')
        except json.decoder.JSONDecodeError:
            return list('')

    def valor_json(self,arq):
        valores_somados = 0
        try:
            with open(self.dados_usuario + arq,'r') as conteudo:
                valores = json.load(conteudo)

            for pos, iten in enumerate(valores):
                valores_somados += float(valores[pos]["valor"])
            return valores_somados
        except FileNotFoundError:
            pass

class Setting(Screen):
    lista_month = ['1-janeiro','2-fevereiro','3-março','4-abril','5-maio','6-junho','7-julho','8-agosto','9-setembro','10-outubro','11-novembro','12-dezembro']
    spiner = []
    ligar = None
    cor = ListProperty()
    cor2 = ListProperty()
    def __init__(self,*args,**kwargs):
        super(Setting,self).__init__(**kwargs)
        from datetime import date

        self.cor = [.12, .25, 0, 0]
        self.snaker = None

        # Data day month and year
        self.day = date.today().day
        self.month = date.today().month
        self.year = date.today().year

        # self.day = dia_teste    # ============== teste
        # self.month = mes_teste  # ============= teste

        # get the user directory
        # pegar o diretorio do usuario
        self.dados_usuario = MDApp.get_running_app().user_data_dir +'/'

        step_spiner = open("step_spiner.txt",'r',encoding="utf-8")
        self.step_spiner = step_spiner.read()

        if self.step_spiner == '':
            self.step_spiner = self.lista_month[self.month-1]

        self.get_dir()
        self.path = str(self.dados_usuario + str(self.step_spiner) + '/')

    def ativo(self,**kwargs):
        var = ''
        if self.ids.switch.active:
            self.ids.fechamento1.readonly = False
            self.ids.fechamento1.background_color = 1,1,1,1
            self.ids.fechamento1.foreground_color = 1,0,0,1

            self.ids.fechamento2.readonly = False
            self.ids.fechamento2.background_color = 1,1,1,1
            self.ids.fechamento2.foreground_color = 1,0,0,1

            self.ids.dia.color = 1,1,1,1
            self.ids.ate.color = 1,1,1,1

            self.snacker('Fechamento do mês altomático!')

            self.cor = .12, .25, 0, .255
            var ='True'

        else:
            self.ids.fechamento1.readonly = True
            self.ids.fechamento1.background_color = 0,0,0,.2
            self.ids.fechamento1.foreground_color = 0,0,0,.2

            self.ids.fechamento2.readonly = True
            self.ids.fechamento2.background_color = 0,0,0,.2
            self.ids.fechamento2.foreground_color = 0,0,0,.2

            self.ids.dia.color = 0,0,0,.2
            self.ids.ate.color = 0,0,0,.2

            self.snacker('Fechamento do mês Manual!')

            self.cor = .12, .25, 0, 0
            var = 'False'

        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   Recente
        try:
            arq_swith = open('arq_swith.txt','w')
            arq_swith.write(str(var))
        except FileNotFoundError:
            pass

    def snacker(self,msg,*args,**kwargs):
        self.snaker = Snackbar(text=msg)
        self.snaker.show()


    def back_menu(self):
        MDApp.get_running_app().root.current = 'Menu'

    def get_dir(self):
        # Here find the dir and the name and pass the content to the variavel spiner
        dados = str(self.dados_usuario)
        if os.path.isdir(dados):
            lista = os.listdir(dados)
            for pasta in lista:
                if pasta.title() == 'app' or pasta.title() == 'App':
                    pass
                else:
                    self.spiner.append(pasta.title())

    def voltar_adicionar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'Adicionar'
        return True

    def on_enter(self):
        self.ativo()

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar_adicionar)

        self.ids.spiner_month.text = str(self.step_spiner).title()

        file = open("fechamento.txt","r")
        file_fechamento1 = file.read(2).strip()
        file_fechamento2 = file.read(3).strip()
        self.ids.fechamento1.text = str(file_fechamento1)
        self.ids.fechamento2.text = str(file_fechamento2)

        porcentage = open('porcentagen.txt','r')
        p = porcentage.read()
        self.ids.df_porcentagen.text = p

        # when entering the setting screen the swith button goes to the chosen position :copiado + ou -
        # quando entrar na tela de configuração, o botão swith vai para a posição escolhida

        # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx to exclud
        # path = str(self.dados_usuario + str(self.lista_month[self.month - 1]) + '/')
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx to exclud
        try:
            arq_swith = open('arq_swith.txt', 'r')
            bt_swith = arq_swith.read()
        except FileNotFoundError:
            bt_swith = False

        if bt_swith == 'True':
            self.ids.switch.active = True
        else:
            self.ids.switch.active = False

    def on_pre_leave(self,*args):
        Window.unbind(on_keyboard=self.voltar_adicionar)

        porcentagen = str(self.ids.df_porcentagen.text)
        if porcentagen != '':
            if 'a'< porcentagen > 'z' or 'A'< porcentagen > 'Z':
                MDApp.get_running_app().root.current = "setting"
                self.popup_mensagen("Informação de porcentagen incorretas!")
            else:
                arq_porcentagen = open('porcentagen.txt','w')
                arq_porcentagen.write(porcentagen)

        if self.ids.fechamento1.text != '' :
            try:
                if int(self.ids.fechamento1.text) > 31 or int(self.ids.fechamento2.text) > 31:
                    MDApp.get_running_app().root.current = "setting"
                    self.popup_mensagen("Informação de fechamento incorretas!")
                else:
                    file_fechamento = open('fechamento.txt', 'w')
                    file_fechamento.write(f'{self.ids.fechamento1.text}\n')
                    file_fechamento.write(f'{self.ids.fechamento2.text}')
            except ValueError:
                if self.ids.fechamento2.text == '' or self.ids.fechamento2.text == 0:
                    file_fechamento = open('fechamento.txt', 'w')
                    file_fechamento.write(f'{self.ids.fechamento1.text}\n')
                    file_fechamento.write('')
                    MDApp.get_running_app().root.get_screen('Menu').ids.bt_active.disabled = True
                pass

        file_step_spiner = open('step_spiner.txt','w',encoding='utf-8')
        file_step_spiner.write(self.ids.spiner_month.text.strip().lower())
        file_step_spiner.close()

        # when entering the setting screen the swith button goes to the chosen position :copiado + ou -
        # quando entrar na tela de configuração, o botão swith vai para a posição escolhida
        # str(self.ids.switch.active)
        # path = str(self.dados_usuario + str(self.lista_month[self.month - 1]) + '/')
        # arq_swith = open(path + 'arq_swith.txt', 'W')
        # arq_swith.write()


    def limpar(self,*args,**kwargs):
        """
        Function to delet all diretory treen
        Função para deletar toda a arvore de diretorio
        :param args:
        :param kwargs:
        :return:
        """
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
            Menu().creat_folder()
            Menu().validng_month(True)
            self.popup_mensagen('Odiretório foi excluído com Sucesso!')
        except OSError:
            self.popup_mensagen('O diretorio não foi excluido')

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
            self.popup_mensagen("Diretório excluido com sucesso!")
        except FileNotFoundError:
            self.popup_mensagen("A pasta já foi excluida reinicie o aplicativo\n para atualizar")
            self.ids.spiner_month.text = str(self.lista_month[self.month - 1])
        Menu().creat_folder()
        Menu().validng_month(True)

    def popup_mensagen(self,msg,*args,**kwargs):

        box = BoxLayout()
        pop = Popup(title=msg,
                    size_hint=(None,None),width='300dp',height='150dp',content=box)
        botao = Button(text='Fechar',color=(.2,0,1,1),size_hint=(None,None),size=('100dp','35dp'),pos_hint={'center_x':.5},on_press=pop.dismiss)

        box.add_widget(botao)
        pop.open()
        return True


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

        anim_bt_nao = Animation(color=(0,0,0,1))+Animation(color=(1,0,0,1))
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


class Menu(Screen, Dados):
    lista_step = []
    # pop_sound = None
    # poppap_sound = None
    desligar = 0

    # Variavel para somar o len do  arquivo Valores.txt
    find = ''
    def __init__(self,**kwargs):
        super(Menu,self).__init__(**kwargs)
        self.day = date.today().day
        self.pos_month = date.today().month

        # self.day = dia_teste   # =================== teste
        # self.pos_month = mes_teste  # ================ teste

        self.file_fechamento1 = 1
        self.file_fechamento2 = 0
        self.file_month = ''
        self.arq_swith = 'True'

        self.creat_file_into()

        # open or creats the month files
        # abre ou cria os arquivos mês
        try:
            open_file_month = open('month.txt','r', encoding='utf-8')
            self.file_month = open_file_month.read()
            open_file_month.close()

            step_spiner = open("step_spiner.txt","r", encoding="utf-8")
            self.step_spiner = step_spiner.read()
            step_spiner.close()

            file_fechamento = open('fechamento.txt', 'r')
            self.file_fechamento1 = int(file_fechamento.read(2).strip())
            file_fechamento.close()

            file_porcento = open('porcentagen.txt', 'r')
            file_porcento.read()
            file_porcento.close()

            file_swith = open('arq_swith.txt','r')
            self.arq_swith = file_swith.read()
            file_swith.close()

            self.validng_month()

        except FileNotFoundError:
            self.creat_file_into()
            self.validng_month()

        # geting the values of file fechamento.txt to the closeding of month
        try:
            fechamento = open("fechamento.txt", "r")
            self.file_fechamento1 = int(fechamento.read(2).strip())
            self.file_fechamento2 = int(fechamento.read(3).strip())
        except ValueError:
            pass

        # get the directory of user
        # pegando o diretório do usuario
        self.dados_usuario = MDApp.get_running_app().user_data_dir + '/'

        self.creat_folder()
        self.creat_file_user()

    def snackbar(self):
        warning = Snackbar(text='Fechado com sucesso!')
        warning.show()

    # Function to valid the month and change the folder of month
    # Funçã"o para validar o mês e mudar a pasta do mês
    def mdicon_ceta(self,icn,color):
        """
        To add the arrow warning that the close month button is active
        Para adicionar a seta avisando que o botão de fechar o mês do menu esta ativo
        :return:
        """
        # icn = 'arrow-right-bold-outline'
        # color = [1,0,0,1]
        try:
            self.ids.mdicon.icon = icn
            self.ids.mdicon.color = color
        except AttributeError:
            pass

    def opcao_ativo(self):
        """
            Retorna True ou False para escolher o fechamento do mês altomatico ou manual
        :return: True or False
        """
        try:
            arq = open('arq_swith.txt', 'r')
            seletor = arq.read()
        except AttributeError:
            seletor = 'False'
        except FileNotFoundError:
            seletor = 'False'
        return seletor

    def validng_month(self,permicao=False):
        """

        :param permicao: Foi criado para quando excluir as pastas do mês,
        o parametro 'permicao' da permição ao programa para criar as pastas mesmo não estando no dia certo
        :return:
        """
        lem = 0
        lista_json = []  # it to reading of file json
        self.lista_step.clear()
        seletor = self.opcao_ativo()

        # here change the month
        # aqui muda o mês


        if self.day >= self.file_fechamento1 or permicao == True:

            if self.lista_month[self.pos_month - 1] != str(self.file_month) and str(self.arq_swith) == 'True' or str(self.file_month) != str(self.step_spiner) or permicao == True:

                file_month = open('month.txt', 'w', encoding='utf-8')
                file_month.write(self.lista_month[self.pos_month - 1])
                file_month.close()

                # open file month to write in file "step_spiner
                file_month = open('month.txt','r', encoding='utf-8')

                # Here and to the app receive the month current
                file_step = open('step_spiner.txt', 'w', encoding='utf-8')
                file_step.write(str(self.lista_month[self.pos_month - 1]))
                file_step.close()
            try:
                # with open(self.dados_usuario + self.lista_month[pos_mes - 2] + '/' + 'SaveData.json','r') as dados_r:
                with open(self.dados_usuario + str(self.file_month) + '/' + 'SaveData.json', 'r') as dados_r:
                    lista_json = json.load(dados_r)
                    dados_r.close()
            except:
                pass

        # here close the fortnight of same month
        # aqui fecha a quinzena do mesmo mês
        if self.file_fechamento2 != 0 or permicao == True:
            if self.day >= self.file_fechamento2 or permicao == True:
                lem = 0
                l = True
                try:
                    # with open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "SaveData.json",'r') as json_dados:
                    with open(self.dados_usuario + str(self.file_month) + "/" + "SaveData.json",'r') as json_dados:
                        self.lista_step = json.load(json_dados)
                except FileNotFoundError:
                    # with open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "SaveData.json","w") as json_dados:
                    with open(self.dados_usuario + str(self.file_month) + "/" + "SaveData.json","w") as json_dados:
                        json_dados.close()
                except:
                    pass

                # Not let the box of close the month open later what already close the month
                # Não deixa a caixa de fechar o mês abrir depois que já fechou o mês
                fechar = open(self.dados_usuario + str(self.file_month) + "/" + "Mes_fechado.txt","r",encoding="utf-8")
                fechado = fechar.read()
                fechar.close()

                if seletor == 'True':
                    if self.desligar > 0 or self.day < self.file_fechamento2 or self.file_fechamento2 <=0 or fechado == "Fechado":
                        pass
                    else:
                        self.desligar += 1
                        Clock.schedule_once(self.pop_mudar_mes, 1)
                else:
                    self.mdicon_ceta('arrow-right-bold-outline',[1,0,0,1])
                    try:
                        self.ids.bt_active.disabled = False
                    except AttributeError:
                        pass

    def close_gastos(self):
        # A dict to get the values
        get_json = {}
        lista_gastos = []

        path = self.dados_usuario + str(self.file_month) + "/"

        with open(path + "GastosFechado.json","r") as get_gastos:
            lista_gastos += json.load(get_gastos)

        # geting will the values of file to pass to the file "GastosFechados" as a dict
        # Obtendo o valores do arquivo para passar para o arquivo "GastosFechado" com um dicionario
        arq_eventos = open(path + "arq_eventos.txt","r")
        eventos = arq_eventos.readlines()
        arq_eventos.close()

        # geting will the values of file to pass to the file "GastosFechados" as a dict
        # Obtendo o valores do arquivo para passar para o arquivo "GastosFechado" com um dicionario

        arq_gasto = ''

        var = ''
        val = ''
        s = ''
        for n,iten in enumerate(eventos):
            var = iten

            arq_gasto = open(path + "gastos.txt","r")
            gastos = arq_gasto.readlines()
            # val = gastos

            get_json["Eventos"] = var
            get_json["Valor"] = gastos[n]
            lista_gastos.append(get_json.copy())
        try:
            arq_gasto.close()
        except:
            pass

        try:
            with open(path + "GastosFechado.json", "w") as valor:
                json.dump(lista_gastos, valor, indent=2)
        except FileNotFoundError:
            pass

        # To clear the file
        clear_eventos = open(path + "arq_eventos.txt","w")
        clear_eventos.write('')
        clear_eventos.close()

        # To clear the file
        clear_gastos = open(path + "gastos.txt","w")
        clear_gastos.write("")
        clear_gastos.close()

    def close_day(self,*args):

        lem = 0
        soma = 0
        v = None

        # seletor = self.opcao_ativo()

        self.lista_step.clear()

        # only to get thes values of file "SaveData"
        valor = []
        try:
            # with open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "SaveData.json", "r") as valor:
            with open(self.dados_usuario + str(self.file_month) + "/" + "SaveData.json", "r") as valor:
                valor = json.load(valor)
        except FileNotFoundError:
            pass

        v = 0
        try:
            for pos, idice in enumerate(valor):
                v = float(idice["valor"])
                soma += v
        except TypeError:
            pass
        #========================

        # here and only to get the values of porcentage of file "porcentagen"
        # aqui é apenas para obter o valor da porcentagen do arquivo "porcentagen"
        file_porcento = open("porcentagen.txt", "r")
        porcento = int(file_porcento.read())
        valor_porcento1 = soma * porcento / 100

        porcento2 = 100 - porcento
        valor_porcento2 = soma - valor_porcento1

        # GASTOS ##############################
        # geting the values of file gasto to sum
        gastos = open(self.dados_usuario + str(self.file_month) + "/" + "gastos.txt")

        valor_gastos = 0
        for valor in gastos:
            valor_gastos += float(valor)

        # diving porcent of values gastos

        valor_gasto1 = valor_gastos * porcento / 100
        valor_gasto2 = valor_gastos - valor_gasto1

        if valor == [] and gastos == '':
            pass
        else:
            self.lista_step.append(
                f" \n\n[color=#FFA726]Fechamento do dia   {self.day}     Total: {soma:.2f} R$[/color]\n{porcento}%  /  {valor_porcento1:.2f} R$   &     "
                f"{porcento2}%  /  {valor_porcento2:.2f} R$\n   [color=#FFA726]Gastos[/color]   {porcento}%    {valor_gasto1:.2f} R$   /   {porcento2}%  {valor_gasto2:.2f} R$\n"
                f"valores posicionados a baixo\n\n")

        try:
            # with open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "SaveData.json",'r') as json_dados:
            with open(self.dados_usuario + str(self.file_month) + "/" + "SaveData.json",'r') as json_dados:
                self.lista_step += json.load(json_dados)
            # with open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "SaveData.json", 'w') as json_clear:
            with open(self.dados_usuario + str(self.file_month) + "/" + "SaveData.json",'w') as json_clear:
                json.dump([],json_clear)
        except FileNotFoundError:
            pass

        try:
            # with open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "Fechado.json",'r') as read_fechado:
            with open(self.dados_usuario + str(self.file_month) + "/" + "Fechado.json",'r') as read_fechado:
                self.lista_step += (json.load(read_fechado))
        except json.decoder.JSONDecodeError:
            pass


        # with open(self.dados_usuario + self.lista_month[self.pos_month - 1] + "/" + "Fechado.json", 'w') as dados_json:
        with open(self.dados_usuario + str(self.file_month) + "/" + "Fechado.json",'w') as dados_json:
            json.dump(self.lista_step, dados_json, indent=2)
            self.snackbar()

        self.mdicon_ceta('android',[0,0,0,1])

        with open(self.dados_usuario + str(self.file_month) + "/" + "Mes_fechado.txt","w") as fechar:
            fechar.write("Fechado")

        self.close_gastos()

        self.validng_month(True)
        self.creat_folder()

    def creat_folder(self):
        try:
            # Here creat the folder of monht
            path = os.mkdir(self.dados_usuario + str(self.file_month))

            # If exist the file then pass
            # Se existir o arquivo então passa
        except FileNotFoundError:
            os.mkdir(self.dados_usuario)
            path = os.mkdir(self.dados_usuario + str(self.file_month))
        except FileExistsError :
            pass

    def creat_file_into(self):

        # open or creats the month files
        # abre ou cria os arquivos mês
        try:
            open_file_month = open('month.txt', 'r', encoding='utf-8')
            open_file_month.close()

            step_spiner = open("step_spiner.txt", "r", encoding="utf-8")
            step_spiner.close()

            file_fechamento = open('fechamento.txt', 'r')
            file_fechamento.close()

            file_porcento = open('porcentagen.txt', 'r')
            file_porcento.close()

            file_swith = open('arq_swith.txt','r')
            file_swith.close()

        except FileNotFoundError:
            open_file_month = open('month.txt', 'w', encoding='utf-8')
            open_file_month.write(str(self.lista_month[self.pos_month - 1]))
            open_file_month.close()

            step_spiner = open('step_spiner.txt', 'w', encoding='utf-8')
            step_spiner.write(str(self.lista_month[self.pos_month - 1]))
            step_spiner.close()

            file_fechamento = open('fechamento.txt', 'w')
            file_fechamento.write('01')
            file_fechamento.close()

            file_porcento = open('porcentagen.txt', 'w')
            file_porcento.write(str(100))
            file_porcento.close()

            file_swith = open('arq_swith.txt', 'w')
            file_swith.write('True')
            file_swith.close()

    def creat_file_user(self):
        # dados_user = self.dados_usuario + self.lista_month[self.pos_month - 1] + '/'
        dados_user = self.dados_usuario + str(self.file_month) + '/'


        # Creat the files soon when open the app
        # Criando os arquivo logo quando abrir o app
        try:
            arq_eventos = open(dados_user + 'Mes_fechado.txt', 'r')
            arq_eventos.close()
        except FileNotFoundError:
            self.creat_folder()
            data = open(dados_user + 'Mes_fechado.txt', 'w')
            data.close()

        try:
            arq_gasto = open(dados_user + 'gastos.txt','r')
            arq_gasto.close()
        except FileNotFoundError:
            arq_gasto = open(dados_user + 'gastos.txt','w')
            arq_gasto.close()

        try:
            arq_gasto_fechados = open(dados_user + 'GastosFechado.json','r', encoding='utf-8')
            arq_gasto_fechados.close()
        except FileNotFoundError:
            with open(dados_user + 'GastosFechado.json','w',encoding='utf-8') as gastos_fechado:
                json.dump([],gastos_fechado)

        try:
            data_json = open(dados_user + 'SaveData.json','r', encoding='utf-8')
            data_json.close()
        except FileNotFoundError:
            lista = []
            with open(dados_user + 'SaveData.json', 'w', encoding='utf-8') as data:
                json.dump(lista,data)

        try:
            arq_fechado_json = open(dados_user  + 'Fechado.json','r')
            arq_fechado_json.close()
        except FileNotFoundError:
            lista = []
            with open(dados_user + 'Fechado.json','w') as fechar:
                json.dump(lista,fechar)

    def on_pre_enter(self):
        # Window.bind(on_request_close=self.confirmar)
        self.validng_month()

        # that "try" and to when clear the tree of directory, not it give none error to returning screen menu
        # Esse try é para quando limpar a arvore de diretórios, não da nunhum erro ao voltar para tela menu
        try:
            self.creat_folder()
        except FileNotFoundError:
            pass

        # opening the file "Mes_fechado" to  no let activate the button "fecha mês"
        # abrindo o arquivo "Mes_fechado" para não deixar activar o botão do "fechar mês"
        is_fechado = open(self.dados_usuario + str(self.file_month) + '/' + "Mes_fechado.txt","r",encoding='utf-8')
        fechado = is_fechado.read()
        is_fechado.close()

        arq_swhit = self.opcao_ativo()
        if arq_swhit == 'False' and fechado != 'Fechado' or arq_swhit == 'False' or self.day >= self.file_fechamento2 and fechado != 'Fechado':
            # here activate the button
            self.desliga()
        else:
            self.desliga(True)

        # self.creat_file()

        # Adicionando o som do pupap carrega osom na variavel
        # if self.pop_sound == None:                # ==================== soudloader
        #     self.pop_sound = SoundLoader.load('poppap.mp3')

    def press_bt(self,content):
        self.content = content
        # self.ids.image_adicionar.source = 'image/bt_dark.png'
        content.source = 'image/bt_dark.png'
        Clock.schedule_once(self.release_bt,0.1)

    def release_bt(self,*args):
        self.content.source ='image/botaoVidro.png'

    def desliga(self,warning=False,*args, **kwargs):

        # warning fica recebendo numeros do local da variavel e não esta recebendo se é True ou False
        if warning != False and warning != True:
            warning = False

        # Here is to activate the button month
        try:
            self.ids.bt_active.disabled = warning
        except AttributeError:
            pass

        if warning == False:
            self.mdicon_ceta('arrow-right-bold-outline',[1,0,0,1])
        elif warning == True:
            self.mdicon_ceta('android',[0,0,0,1])

        return warning

    def pop_opcao(self,*args,**kwargs):
        box = BoxLayout()

        pop = Popup(title='Deseja fechar?', size_hint=(None,None),size=('200dp','100dp'), content=box)

        bt_sim = MDFlatButton(text='Sim', on_press=self.close_day, on_release=pop.dismiss)
        bt_nao = MDFlatButton(text='Não',on_release=pop.dismiss)
        box.add_widget(bt_sim)
        box.add_widget(bt_nao)

        pop.open()

    def pop_mudar_mes(self,*args,**kwargs):

        box = BoxLayout(spacing='10dp', orientation='vertical')
        pop = Popup(title=f'O mes fecha dia {int(self.file_fechamento2)} deseja fechalo?', size_hint=(None, None),
                    size=('200sp', '150sp'), content=box)
        box_bt = BoxLayout(spacing='13dp', size_hint_y=None, height='30sp')

        image = Image(source='image/atencao.png')

        bt_sim = Botaos(text='Sim', on_press=self.close_day, on_release=pop.dismiss)
        bt_nao = Botaos(text='Nao', on_press=pop.dismiss , on_release=self.desliga )

        box.add_widget(image)
        box_bt.add_widget(bt_sim)
        box_bt.add_widget(bt_nao)
        box.add_widget(box_bt)

        pop.open()
        return True

class Adicionar(Screen,Dados):
    lista = []
    dicionario = {}
    get = ''
    def __init__(self,**kwargs):
        super(Adicionar,self).__init__(**kwargs)
        self.data = (f'{str(self.data_day).zfill(2)}/{str(self.data_month).zfill(2)}/{str(self.data_year).zfill(4)}')

        self.day = self.data_day
        self.pos_month = self.data_month

        # To it know if the month change /
        # para saber se o mês mudou sem pemição por comta do fechamento manual do mês
        self.plug = False

        # self.day = dia_teste      # ================== teste day
        # self.pos_month = mes_teste # ================== teste month

        try:
            fechamento = open("fechamento.txt", "r")
            self.file_fechamento1 = int(fechamento.read(2).strip())
            self.file_fechamento2 = int(fechamento.read(3).strip())
        except:
            pass


        arq_month = open('month.txt','r',encoding='utf-8')
        self.file_month = arq_month.read()
        arq_month.close()


        # here is to when the month change, while the day is not larger than file_fechamento1 not change the directory
        # aqui é para quando o mês mudar, enquanto o dia não for maior que file_fechamento1 não muda o diretório
        if self.day < self.file_fechamento1:
            self.pos_month -= 1


        # self.dados_usuario = MDApp.get_running_app().user_data_dir + '/' + self.lista_month[self.pos_month - 1] +'/'
        self.dados_usuario = MDApp.get_running_app().user_data_dir + '/' + str(self.file_month) + '/'

        # Aqui é para só cria a pasta do mês quando o botão do fechar mês estiver for precionado quando o mês for fechar manual ou automatico
        try:
            with open('arq_swith.txt','r') as swithread:
                swith = swithread.read()
        except FileNotFoundError:
            swith = 'False'

        if swith == 'True':
            if self.day == int(self.file_fechamento1):        # ===============  day
                Menu().creat_folder()

    def back_menu(self):
        MDApp.get_running_app().root.current = 'Menu'

    def go_setting(self):
        MDApp.get_running_app().root.current = 'setting'

    def on_pre_enter(self):
        self.get = self.ids.mensagen_add.text
        # self.dados_usuario = App.get_running_app().user_data_dir + '/'
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_keyboard=self.teclas)
        # self.save_data()

    def save_data(self):
        modelo = self.ids.text_modelo.text.capitalize()
        local = self.ids.text_local.text.capitalize()
        valor_int = ''
        try:
            valor_int = str(float(self.ids.text_valor.text))
        except ValueError:
            self.ids.mensagen_add.text = 'Digito invalido Não digite \ncaracteres especiais "." "," e outros'
            Clock.schedule_once(self.retorna_mesagens,5)


        self.dicionario['data'] = self.data
        self.dicionario['modelo'] = modelo
        self.dicionario['local'] = local
        self.dicionario['valor'] = valor_int

        eventos = self.ids.text_eventos.text
        gastos = 0

        if self.ids.text_gastos.text != '':
            try:
                gastos = str(float(self.ids.text_gastos.text))
            except ValueError:
                self.ids.mensagen_gastos.text = 'Digitos invalido no campo gastos "Só numeros"'
                Clock.schedule_once(self.retorna_mesagens,5)
        else:
            gastos = 0

        if gastos != 0 and eventos != '':
            # criando arquivo para os eventos de gastos
            arq_eventos = open(self.dados_usuario + 'arq_eventos.txt', 'a')
            arq_eventos.write(f'{eventos.upper()}:  {float(gastos)} R$\n')
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
                    with open(self.dados_usuario+'/'+'SaveData.json', 'r', encoding='utf-8') as dados:
                        self.ids.text_modelo.text = ''
                        self.ids.text_local.text = ''
                        self.ids.text_valor.text = ''

                        self.lista = json.load(dados)  # Aqui é para a lista sempre receber o conteudo do arquivo json primeiro

                        # self.lista.append(f'{self.data:<25} {modelo:<30} {local:<25} {float(valor_int):>8} R$')
                        self.lista.append(self.dicionario)

                except FileNotFoundError and json.decoder.JSONDecodeError:
                    # self.lista.append(f'{self.data:<25} {modelo:<30} {local:<25} {float(valor_int):>8} R$')
                    self.lista.append(self.dicionario)
                    self.get = self.ids.mensagen_add.text

                    with open(self.dados_usuario + '/' + 'SaveData.json', 'w', encoding='utf-8') as data:
                        json.dump(self.lista, data, indent=2)
                        self.ids.text_modelo.text = ''
                        self.ids.text_local.text = ''
                        self.ids.text_valor.text = ''

                # criando um arquivo json e recebendo os conteudo da lista
                try:
                    with open(self.dados_usuario+'/'+'SaveData.json', 'w', encoding='utf-8') as data:
                        json.dump(self.lista, data, indent=2)
                        self.ids.text_modelo.text = ''
                        self.ids.text_local.text = ''
                        self.ids.text_valor.text = ''
                        self.lista.clear()
                        self.dicionario.clear()
                        try:
                            # criando um arquivo Valores
                            self.valor('Valores.txt', str(int(valor_int)))
                        except ValueError:
                            pass
                        self.ids.mensagen_add.text = 'Arquivos salvos com sucesso!'
                        self.get = self.ids.mensagen_add.text
                        Clock.schedule_once(self.retorna_mesagens,5)
                except:
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
        self.ids.mensagen_add.text = 'Adicione a cima o modelo do carro/moto,\n local e valor'

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'Menu'
            return True

    def teclas(self,window,key,*args):
        if key == 13:
            self.save_data()

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)


class Visualizar(Screen,Dados):
    soma = 0
    # sem_botao = False
    # l = 0
    def __init__(self,**kwargs):
        super(Visualizar,self).__init__(**kwargs)
        self.box = Box()
        self.lista = []
        self.lista_fechado = []
        self.lista_valores = []
        self.soma = Visualizar.soma

        self.day = self.data_day
        # self.day = dia_teste   # ============= teste day


        file_step_spiner = open('step_spiner.txt', 'r', encoding='utf-8')
        self.file_step_spiner = file_step_spiner.read()

        # pegando o diretório do usuario
        self.dados_usuario = MDApp.get_running_app().user_data_dir + '/' + str(self.file_step_spiner) + '/'

        self.texto = str('{:<30} {:<30} {:<30} {:>6}'.format('Data','Modelo','Local','Valor'))

    def back_menu(self):
        MDApp.get_running_app().root.current = 'Menu'
    def back_setting(self):
        MDApp.get_running_app().root.current = 'setting'

    def add(self):
        open_spiner = open('step_spiner.txt', 'r', encoding='utf-8')
        step_spiner = str(open_spiner.read())
        open_spiner.close()

        self.month = open('month.txt', 'r', encoding='utf-8')
        month = self.month.read()

        self.lista_data = self.read_json('SaveData.json')

        self.lista_fechado = self.read_json('Fechado.json')

        # hare is to add the values in box correct
        # Aqui é para adicionar os valores no Box corretos
        self.lista_data.reverse()
        self.lista_fechado.reverse()


        for num, linha in enumerate(self.lista_data):
            # if float(self.lista_data[num]["valor"]) <= float(999):
            valor_sem_virgula = str(self.lista_data[num]["valor"]).replace(',','.')
            # valor = int(self.lista_data[num]["valor"])
            valor = valor_sem_virgula

            # else:
            #     valor = float(self.lista_data[num]["valor"])

            try:
                # formatado = (f'{"":>10} {self.lista[num]["data"]:<20}  {self.lista[num]["modelo"]:<30}  {self.lista[num]["local"]:<35}  {float(self.lista[num]["valor"]):>10}  R$ {"":>10}')
                formatado = str('   {:<25} {:<20} {:<30} {:>20}'.format(self.lista_data[num]["data"], self.lista_data[num]["modelo"],
                                                                     self.lista_data[num]["local"],str(valor).replace('.',',')))
            except FileNotFoundError:
                formatado = ''
            self.ids.coteiner.add_widget(Box(label=str(formatado))) # if

        self.lista_fechado.reverse()
        for pos, valor in enumerate(self.lista_fechado):
            try:
                itens_fechados = str('{:<25} {:<20} {:<30} {:<20}'.format(self.lista_fechado[pos]["data"],self.lista_fechado[pos]["modelo"],
                                                                      self.lista_fechado[pos]["local"],float(self.lista_fechado[pos]["valor"])))
            except TypeError:
                itens_fechados = self.lista_fechado[pos]
            self.ids.coteiner.add_widget(BiforeTotal(texto=str(itens_fechados)))  # else

    def on_pre_enter(self):
        # colocando texto formatado
        self.ids.super_modelo_text.text = self.texto

        self.file_step_spiner = open('step_spiner.txt', 'r', encoding='utf-8')

        # pegando o diretório do usuario
        self.dados_usuario = MDApp.get_running_app().user_data_dir + '/' + str(self.file_step_spiner.read()) + '/'

        Window.bind(on_keyboard=self.voltar)

        self.add()

        try:
            self.ids.total_valor.text =''
            self.ids.total_valor.text = f"Total: R$   {str(float(self.valor_json('SaveData.json'))).replace('.',',')}"
        except TypeError:
            pass

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'Menu'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        self.lista.clear()
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

    def pop_fechados(self,*args,**kwargs):

        var = []
        total = 0
        for pos,linha in enumerate(self.lista_fechado):
            try:
                var += (self.lista_fechado[pos]["data"],self.lista_fechado[pos]["modelo"],self.lista_fechado[pos]["local"],self.lista_fechado[pos]["valor"])
                total += float(self.lista_fechado[pos]["valor"])
            except TypeError:
               pass
            except IndexError:
                pass

        tabela = MDDataTable(
            column_data=[
                ("Data",dp(20)),
                ("Modelo",dp(20)),
                ("Local",dp(20)),
                ("Valor",dp(20))
            ],
            row_data=[
                var
            ],
        )
        popap = Popup(title="Fechados" + '  Total  R$: '+ str(total) ,size_hint=(None,None),size=('350dp','400dp'),
                      content=tabela)

        popap.open()

    def deletar(self,*args):
        texto = self.root.ids.texto.text.replace(',','.')

        try:
            self.lista.clear()
            self.lista_valores.clear()

            # variaveis para pegar a posição do dicionário que devera ser exclida
            valores = ''
            val = ''
            pos = 0

            # with open(self.dados_usuario+'SaveData.json','r',encoding='utf-8')as get_json:
            #     self.lista = json.load(get_json)

            self.lista = self.read_json('SaveData.json')
            self.ids.coteiner.remove_widget(self.root)

            # preparando o texto para a posição
            for valorTexto in texto.split():
                valores += valorTexto

            # Pegando a posição do dicionário
            for posi, valor in enumerate(self.lista):
                self.lista_valores.append(self.lista[posi - 1].values())

                for v in valor.values():
                    val += str(v)

                if str(valores) == str(val):
                    pos = posi
                val = ''

            del(self.lista[pos])

            with open(self.dados_usuario+'SaveData.json','w',encoding='utf-8') as save_json:
                json.dump(self.lista, save_json)

            # Reinscrevendo na tela
            try:
                self.ids.total_valor.text = f'Total: R$   {str(float(self.valor_json("SaveData.json")))}'
            except TypeError:
                pass
        except ValueError or AttributeError:
            pass


class TelaTotal(Screen,Dados):
    soma = 0
    arquiv = 0
    def __init__(self,**kwargs):
        super(TelaTotal,self).__init__(**kwargs)
        self.lista_eventos = []
        self.lista_gastos = []
        self.dados_usuarios = MDApp.get_running_app().user_data_dir + '/'

    def back_menu(self):
        MDApp.get_running_app().root.current = 'Menu'

    def back_setting(self):
        MDApp.get_running_app().root.current = 'setting'

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'Menu'
        return True

    def percentuais(self):
        valor = self.valor_json('SaveData.json')
        return valor

    def show_data(self):
        # Opening file "step_spiner.txt" to give access folder of month
        open_spiner = open('step_spiner.txt', 'r', encoding='utf-8')
        file_spiner = str(open_spiner.read())

        # Access folder month
        self.dados_usuario = self.dados_usuarios + file_spiner + '/'
        open_spiner.close()

        self.month = open('month.txt', 'r', encoding='utf-8')
        month = self.month.read()

        # Here TelaTotal get percentage of file
        # aqui a TelaTotal recebe a porcentagen do arquivo
        try:
            arq_porcentagen = open('porcentagen.txt', 'r')
            self.main_porcentagen = arq_porcentagen.read()
            arq_porcentagen.close()
        except:
            self.main_porcentagen = 100

        # trying open file gastos.txt  se não existir  a variavel arquiv sera criada com espaço em branco
        try:
            self.arquiv = self.ler_valor('gastos.txt')
        except FileNotFoundError:
            self.arquiv = 0

        try:
            with open(self.dados_usuario + 'GastosFechado.json', 'r') as fechados:
                gastos_fechados = json.load(fechados)
        except FileNotFoundError:
            pass

        # Opening file arq_eventos.txt to read the amount of events
        # abrindo arquivo arq_eventos.txt para ler a quantidades de eventos
        try:
            add_arq = open(self.dados_usuario + 'arq_eventos.txt', 'r')
            self.ids.gastos.clear_widgets()
            self.ids.show_gastos.clear_widgets()

            for iten in add_arq.readlines():
                self.ids.gastos.add_widget(Box_Total(label=str(iten).replace('.', ',')))
            for iten in gastos_fechados:
                self.ids.show_gastos.add_widget(BiforeTotal(texto=str(iten["Eventos"]).replace('.', ',')))
        except FileNotFoundError:
            add_arq = ''

        valor = 0
        try:
            for v in gastos_fechados:
                valor += float(v["Valor"])
        except UnboundLocalError:
            pass

        self.ids.valor_total_fechado.text = str(valor)

        try:
            # Passando a variavel do arquiv com self.ler_valor('gastos.txt') para somas
            self.ids.total_gastos.text = str(f"Total gastos: {str(float(self.arquiv)).replace('.', ',')}")
        except TypeError:
            pass

        # Trying open the file valores.txt to sum if not exist it will be create
        # Tentando abrir o arquivo Valores.txt para soma se não existir será criado
        try:
            s_v = self.valor_json('SaveData.json')
            self.ids.Valor_soma.text = f'R$ {s_v:.2f}'.replace('.', ',')
        except FileNotFoundError:
            pass
        except TypeError:
            self.ids.Valor_soma.text = '0'

        # Create and showing thes division ofs percentagen and aditioning in label
        # Criando e Mostrando as divisões das porcentagen e adicionando no label
        percentual_main = 0
        percentual_sobra = 0
        try:
            percentual_main = float(self.percentuais() * float(self.main_porcentagen) / 100)
            percentual_sobra = float(self.percentuais() - percentual_main)
            self.ids.label_main.text = f'{self.main_porcentagen} %'
            self.ids.label_sobra.text = f'{100 - float(self.main_porcentagen)} %'
        except TypeError:
            pass

        try:
            percentual_gasto_main = float((int(self.main_porcentagen) * int(self.arquiv)) / 100)
            percentual_gasto_sobra = float(self.arquiv - percentual_gasto_main)
        except TypeError:
            percentual_gasto_main = 0
            percentual_gasto_sobra = 0

        self.atualizar_rst()

        # Here format the values
        # Aqui formata os valores
        v_m = float(percentual_main)
        v_s = float(percentual_sobra)
        self.ids.valor_sobra.text = f'{v_s:.2f}'.replace('.', ',')
        self.ids.valor_main.text = f'{v_m:.2f}'.replace('.', ',')

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        self.show_data()

    def on_pre_leave(self):
        Window.unbind(on_keyboard = self.voltar)
        self.ids.total_gastos.text = ''
        self.ids.gastos.clear_widgets()

    def atualizar_rst(self):

        # trying open file gastos.txt  if not exists the variable the file will be creat with space in white
        try:
            arquiv = self.ler_valor('gastos.txt')
        except FileNotFoundError or TypeError:
            arquiv = 0


        # Create and showing thes division ofs percentagen and aditioning in label
        # Criando e Mostrando as divisões das porcentagen e adicionando no label
        try:
            percentual_main = float(self.percentuais() * int(self.main_porcentagen) / 100)
            percentual_sobra = float(self.percentuais() - percentual_main)
            self.ids.label_main.text = f'{self.main_porcentagen} %'
            self.ids.label_sobra.text = f'{100 - int(self.main_porcentagen)} %'
        except TypeError:
            pass

        if arquiv == None:
            arquiv = 0

        percentual_gasto_main = float((int(self.main_porcentagen) * int(arquiv)) / 100)
        percentual_gasto_sobra = float(arquiv - percentual_gasto_main)

        self.ids.porc_gasto.text = f""" 
                
        [size=20dp][b][color=#7f2f00ff]{self.main_porcentagen}%[/color]   =  {percentual_gasto_main:.2f}[/b][/size] R$

        [size=20dp][b][color=#7f2f00ff]{100 - int(self.main_porcentagen)}%[/color]  =  {percentual_gasto_sobra:.2f}[/b][/size] R$
                
                
        [b][color=#7f2f00ff]Total[/color][/b]: R$ {arquiv:.1f}""".replace('.',',')

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

    def deletar(self,*args):
        texto =( self.root_bt.ids.texto.text).replace(',','.')
        try:
            # Excluindo dos arquivos eventos e gastos
            self.ids.gastos.remove_widget(self.root_bt)

            # Limpando as listas
            self.lista_eventos.clear()
            self.lista_gastos.clear()

            ler_eventos = open(self.dados_usuario+'arq_eventos.txt','r')
            for eventos in ler_eventos:
                self.lista_eventos.append(eventos)

            # geting the position of file
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
                self.lista_gastos.append(float(valor))
            ler_gastos.close()

            del(self.lista_gastos[pos_eventos])

            add_gastos = open(self.dados_usuario+'gastos.txt','w')
            for valor in self.lista_gastos:
                add_gastos.write(f'{str(valor)}\n')

            soma = sum(self.lista_gastos)
            self.ids.total_gastos.text = f'Total gastos: {str(float(soma))}'

        except ValueError:
            pass
        except FileNotFoundError:
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


class ControleVerbaApp(MDApp):
    def build(self):
        Builder.load_string(open('verba.kv', encoding='utf-8').read())
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'BlueGray'
        self.theme_cls.accent_palette = 'Blue'


        return Gerenciador()


if __name__ == '__main__':
    ControleVerbaApp().run()
