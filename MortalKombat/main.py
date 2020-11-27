#ecoding: utf-8
import kivy
kivy.require('1.9.1')

# Testing github with pycharm

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.animation import Animation

class Gerenciador(ScreenManager):
    pass

class Menu(Screen):

    def on_pre_enter(self): #Éssa função é para mostrar o Popup quando apertardo o botão ESQ
        Window.bind(on_request_close=self.confirmar)

    def confirmar(self,*args,**kwargs):

        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        botoes = BoxLayout(spacing=10)
        pop = Popup(title='Deseja realmente sair?', content=box, size_hint=(None,None),
                    size=(180,180))
        imag = Image(source='icones/atencao.png')
        bt_sim = Botao(text='Sim',on_release=App.get_running_app().stop)
        bt_nao = Botao(text='Não', on_release=pop.dismiss)

        box.add_widget(imag)
        botoes.add_widget(bt_sim)
        botoes.add_widget(bt_nao)

        box.add_widget(botoes)

        anim_pop = Animation(size=(300,180), duration=.2, t="out_back")
        anim_pop.start(pop)

        anim_bt_sim = Animation(color=(0,0,0,1)) + Animation(color=(1,1,1,1))
        anim_bt_sim.start(bt_sim)
        anim_bt_sim.repeat = True

        pop.open()
        return True


class Competitivo(Screen):
    pass

class Botao(ButtonBehavior,Label):
    cor = ListProperty([.3,.3,.3,1])
    cor2 = ListProperty([0,0,0,1])

    def __init__(self,**kwargs):
        super(Botao,self).__init__(**kwargs)
        self.atualizar()

    def on_size(self,*kwargs):
        self.atualizar()
    def on_pos(self,*kwargs):
        self.atualizar()

    def on_cor(self,*args):
        self.atualizar()

    def on_press(self,*args):
        self.cor,self.cor2 = self.cor2,self.cor

    def on_release(self,*args):
        self.cor,self.cor2 = self.cor2,self.cor

    def atualizar(self):
        self.canvas.before.clear()
        with self.canvas.before:
            # Color(rgba=(.3,.3,.3,1))
            Color(rgba=self.cor)
            Ellipse(size=(self.height,self.height),
                    pos=(self.x,self.y))
            Ellipse(size=(self.height,self.height),
                    pos=(self.x+self.width-self.height,self.y))
            Rectangle(size=(self.width-self.height,self.height),
                      pos=(self.x+self.height/2.0, self.y))




class Game(Screen):
    lista_nome1 = list()
    lista_nome2 = list()
    lb_posicao = 1
    step = list()
    valida = 0
    pos2 = 0
    cont = 0
    retroceder_uma_vez = 0

    def __init__(self, **kwargs):
        super(Game,self).__init__(**kwargs)
        self.l_nome1 = Game.lista_nome1
        self.l_nome2 = Game.lista_nome2
        self.l_step = Game.step
        self.valida = Game.valida   # Para validar o botão "VS"
        self.pos2 = Game.pos2
        self.cont = Game.cont
        self.voltar_uma = Game.retroceder_uma_vez
        self.lb_posicao  = Game.lb_posicao
        self.step_cont = Game.cont

    def add_lista(self):
        """
        Adicionando os nomes na lista e apagando o nomes que foram escritos caixa de entrada "write_nome"
        :return:
        """
        if self.ids.entrada.text.capitalize().strip() in self.l_nome2 or self.ids.entrada.text.capitalize().strip() in self.l_nome1:
            self.ids.lb_entrada.text = str(self.ids.entrada.text.capitalize().strip() + ' já extende a lista de oponentes')
        elif self.ids.entrada.text != '':
            self.l_nome2.append(self.ids.entrada.text.capitalize().strip())
            self.ids.lb_entrada.text = 'Digite os nome dos jogadores'
            if len(self.l_nome1) > 0:
                self.ids.lb_entrada.text = self.ids.entrada.text.capitalize().strip() + ' Adicionado a fila'
        if len(self.ids.entrada.text) <= 0:
            self.ids.lb_entrada.text = 'Não foi digitado nenhum nome'
        if self.valida > 0:
            self.ids.quant_jogador.text = str(len(self.l_nome2) + 1)
            # self.lb_nome3["text"] = self.l_nome2[self.lb_posicao]
        else:
            self.ids.quant_jogador.text = str(len(self.l_nome2))
        self.ids.entrada.text = ''

    def destribui_nome(self):
        """
        Colocando os nomes nos botões de celeção
        :return:
        """
        if self.valida < 1:  # Aqui valida o botão "VS" para ser usado somente no começo da destribuição dos jogadore
            if len(self.l_nome2) > 2:
                self.l_nome1 = self.l_nome2[0]      #lista_nome1 recebendo a primeira posição da lista_nome2
                del(self.l_nome2[0])                #deletando o nome da lista_nome2 que foi passado pára para a lista_nome1
                self.ids.nome1.text = str(self.l_nome1)
                self.ids.nome2.text = str(self.l_nome2[0])
                self.ids.lb_nome3.text = self.l_nome2[1] # Mostrando o proximo jogador
                self.ids.quant_jogador.text = str(len(self.l_nome2)+1)
                self.valida +=1
            else:
                self.ids.lb_entrada.text = 'Digite pelomenos 3 nomes'

    # Logicá do programa de entradas de nomes
    def passando_nome1(self):
        # if self.step_cont == 1:
        #     self.cont = self.step_cont
        # else:
        #     self.step_cont = self.cont  # STEP_CONT RECEBE O CONTADOR DE VITÓRIA PARA REPOSICIONAR O ULTIMO RESULTADO DA VITORIA
        if self.ids.nome1.text != "Primeiro nome":
            self.pos2 += 1
            self.ids.lb_cont.text = str(self.cont)
            if self.ids.check_vitoria.active:  # celetor para ativar ou desativar o contador de vitórias
                self.cont += 1
                self.ids.lb_vitoria.text = 'Vitoria Ligada'
            else:
                self.ids.lb_vitoria.text = 'Vitoria pausada'
            if self.pos2 >= len(self.l_nome2):
                self.pos2 = 0
            self.lb_posicao = self.pos2
            self.ids.lb_cont.text = str(self.cont)
            self.lb_posicao += 1
            if self.lb_posicao >= len(self.l_nome2):
                self.lb_posicao = 0
            self.ids.nome2.text = str(self.l_nome2[self.pos2])
            self.ids.lb_nome3.text = self.l_nome2[self.lb_posicao]
        else:
            self.ids.lb_entrada.text = 'Caixa primeiro nome vázio!'
        self.step = ''
        self.voltar_uma = 0
        self.step_cont = self.cont  # STEP_CONT RECEBE O CONTADOR DE VITÓRIA PARA REPOSICIONAR O ULTIMO RESULTADO DA VITORIA

    def passando_nome2(self):
        if self.ids.nome2.text != "Segundo nome":
            self.step = self.l_nome2[self.pos2]
            self.l_nome2[self.pos2] = self.l_nome1
            self.l_nome1 = self.step
            self.pos2 += 1
            self.lb_posicao +=1

            self.cont = 1
            if self.ids.check_vitoria.active:
                self.cont = 1
                self.ids.lb_vitoria.text = 'Vitoria Ligada'
            else:
                self.ids.lb_vitoria.text = 'Vitoria Pausada'
            if self.pos2 >= len(self.l_nome2):
                self.pos2 = 0
            if self.lb_posicao >= len(self.l_nome2):
                self.lb_posicao = 0
            self.ids.lb_nome3.text = str(self.l_nome2[self.lb_posicao])
            self.ids.lb_cont.text = str(self.cont)
            self.ids.nome1.text = str(self.l_nome1)
            self.ids.nome2.text = str(self.l_nome2[self.pos2])
        else:
            self.ids.lb_entrada.text = 'Caixa segundo nome vázio!'
        self.voltar_uma = 0

    def retroceder(self):
        if len(self.l_nome2) > 0:
            if self.voltar_uma == 0:
                self.voltar_uma += 1
                if self.pos2 == 0:  # se a pos2 voltar para o zero ele ira receber o ultimo numero da lista que era oque esta
                    self.pos2 = len(self.l_nome2)-1
                else:
                    self.pos2 -= 1
                if self.lb_posicao == 0:
                    self.lb_posicao = len(self.l_nome2)-1
                else:
                    self.lb_posicao -= 1

                if len(self.step) > 0:
                    self.l_nome1 = self.l_nome2[self.pos2]
                    self.l_nome2[self.pos2] = self.step
                    self.step = ''
                    self.cont = self.step_cont
                    self.cont += 1
                    self.ids.nome1.text = str(self.l_nome1)
                    self.ids.nome2.text = str(self.l_nome2[self.pos2])
                    self.ids.lb_nome3.text = str(self.l_nome2[self.lb_posicao])
                else:
                    self.ids.nome2.text = str(self.l_nome2[self.pos2])
                    self.ids.lb_nome3.text = str(self.l_nome2[self.lb_posicao])
                self.cont -= 1
                self.ids.lb_cont.text = str(self.cont)
        else:
            self.ids.lb_entrada.text = 'Sem nome na lista'

    def deleta(self):
        if self.ids.entrada.text != '':
            if self.ids.entrada.text.capitalize() not in self.l_nome2:
                self.ids.lb_entrada.text = str(self.ids.entrada.text.capitalize() +' nome não estende a lista de jogadore')
            posicao = self.l_nome2.index(self.ids.entrada.text.capitalize())
            del (self.l_nome2[posicao])
            self.ids.lb_entrada.text = str(self.ids.entrada.text.capitalize() + ' Removido da lista')
            self.ids.entrada.text = ''
            self.ids.quant_jogador.text = str(len(self.l_nome2) + 1)
            if self.lb_posicao >= len(self.l_nome2):
                self.lb_posicao = 0
            self.ids.lb_nome3.text = self.l_nome2[self.lb_posicao]

    def lb_check(self):
        if self.ids.check_vitoria.active:
            self.ids.lb_vitoria.text = 'Vitoria Ligada'
        else:
            self.ids.lb_vitoria.text = 'Vitoria Pausada'
    #=========== Eventos de teclado ===========================
    def on_pre_enter(self):
        Window.bind(on_keyboard=self.salvar)

    def salvar(self,window,key,*args):
        if key == 13:
            self.add_lista()
        if key == 27:
            App.get_running_app().root.current = 'Menu'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.salvar)

    def sair(self):
        Menu().confirmar()


class MkApp(App):
    def build(self):
        return Gerenciador()

MkApp().run()
