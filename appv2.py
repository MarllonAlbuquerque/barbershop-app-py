import kivy
from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from datetime import datetime
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import textfield
from kivymd.uix.fitimage import FitImage
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.pickers.datepicker import BaseDialogPicker
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.pickers import MDDatePicker 
from kivymd.uix.pickers.datepicker import BaseDialogPicker
kivy.config.Config.set('graphics','resizable', False)
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from datetime import datetime
from kivy.animation import Animation
from kivymd.uix.list import OneLineListItem
from kivymd.uix.card import MDCardSwipe
from kivy.properties import StringProperty
from datetime import date
import calendar
import mysql.connector
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton



class JanelaPrincipal(ScreenManager):

    #Tela do Admin, lista de cortes agendados
    def remove_item(self, instance):
        app = App.get_running_app()
        app.root.get_screen('ScreenAdm').ids['md_list'].remove_widget(instance)

    def admin(self):
        app = App.get_running_app()
        con = mysql.connector.connect(host='localhost', database='logdb',user='root',password='admin')
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM admintb")
        res = cursor.fetchall()
        print(res)
        for i in res:
            app.root.get_screen('ScreenAdm').ids['md_list'].add_widget(
                SwipeToDeleteItem(text=f"{i}")
            )

    #------------------------------------------------------------------------------------------

    #Tela 3, Pega a data escolhida
    def on_save(self, instance, value, date_range):
        app = App.get_running_app()
        app.root.get_screen('ScreenThree').ids['datalb'].text =str(value)

    def sdp(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()
    #------------------------------------------------------------------------------------

    #Tela 1, Validação do login
    def validacao(self):
        app = App.get_running_app()
        email = app.root.get_screen('ScreenOne').ids['email'].text
        senha = app.root.get_screen('ScreenOne').ids['senha'].text
        con = mysql.connector.connect(host='localhost', database='logdb',user='root',password='admin')
        if not email or not senha:
            self.dialog = MDDialog(title="Campos Vazios",
                                   radius=[20, 20, 20, 20],
                                   md_bg_color=(.87, .74, .61, 1),)
            self.dialog.open()
        else:
            cursor = con.cursor()
            cursor.execute(f"SELECT email,senha FROM logtb WHERE email ='{email}'and senha = '{senha}'")
            res = cursor.fetchall()
            if len(res)!=0:  #Verifica se o retorno contém alguma linha
                print('Email e senha Já Cadastrado')
                app.root.current="ScreenThree"
                app.root.transition.direction = "up"
                cursor.execute(f"SELECT nome FROM logtb WHERE email ='{email}'and senha = '{senha}'")
                x = str(cursor.fetchall()).replace("[","").replace("]","").replace("(","").replace(")","").replace("'","").replace(",","")
                app.root.get_screen('ScreenThree').ids['nomelb'].text=x
                
            else:
                print('Email e senha não cadastrado')
                self.dialog = MDDialog(title="Senha ou Email incorreto",
                                   radius=[20, 20, 20, 20],
                                   md_bg_color=(.87, .74, .61, 1),
                                   )
                self.dialog.open()
                cursor.close()
    #---------------------------------------------------------------

    def salvarcad(self):
        app = App.get_running_app()
        nome = app.root.get_screen('ScreenTwo').ids['nomeid'].text
        email = app.root.get_screen('ScreenTwo').ids['emailid'].text
        senha = app.root.get_screen('ScreenTwo').ids['senhaid'].text
        senha2 = app.root.get_screen('ScreenTwo').ids['senhaid2'].text

        if not nome or not email or not senha or not senha2:
            self.dialog = MDDialog(title="Campos Vazios",
                                   radius=[20, 20, 20, 20],
                                   md_bg_color=(.87, .74, .61, 1),)
            self.dialog.open()

        elif senha != senha2:
            self.dialog = MDDialog(title="Senhas Diferentes",
                                   radius=[20, 20, 20, 20],
                                   md_bg_color=(.87, .74, .61, 1),)
            self.dialog.open()

        else:
            con = mysql.connector.connect(host='localhost', database='logdb',user='root',password='admin')
            if con.is_connected():
                cursor = con.cursor()
                cursor.execute(f"insert into logtb(nome,email,senha) VALUES ('{nome}','{email}','{senha}')")
                con.commit()
                print(cursor.rowcount, "Gravação feita na tabela logtb")
                cursor.close()
                self.dialog = MDDialog(title="Cadastro Realizado!",
                                   radius=[20, 20, 20, 20],
                                   md_bg_color=(.87, .74, .61, 1),)
                self.dialog.open()
            else:
                print("Não Conectado!")
    def preocupado(self):
        app = App.get_running_app()
        if app.root.get_screen('ScreenThree').ids['datalb'].text != "Data: Hoje":
            print("passou")
            dataesc = app.root.get_screen('ScreenThree').ids['datalb'].text
            con = mysql.connector.connect(host='localhost', database='logdb',user='root',password='admin')
            cursor = con.cursor()
            cursor.execute(f"SELECT hora FROM admintb WHERE data = '{dataesc}'")
            x = str(cursor.fetchall()).replace("[","").replace("]","").replace("(","").replace(")","").replace("'","").replace(",","")
            horas = ['07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
            cm=0
            fn=5
            restart = True
            while restart:
                restart = False  
                for i in horas:
                    for a in range(20):
                        if i == x[cm:fn]:
                            print(f"Iguais {i} == {x[cm:fn]}")
                            app.root.get_screen('ScreenFour').ids[f"{i}"].line_color=(1, 0, 0, 1)
                            app.root.get_screen('ScreenFour').ids[f"{i}"].text_color=(1, 0, 0, 1)
                            cm = fn+1
                            fn = fn+6
                            restart = True 
                            break
        else:{
            print("é igual")
    }
        
        

    def ocupado(self):
        app = App.get_running_app()
        con = mysql.connector.connect(host='localhost', database='logdb',user='root',password='admin')
        data = app.root.get_screen('ScreenThree').ids['datalb'].text
        cursor = con.cursor()
        cursor.execute(f"SELECT hora FROM admintb")
        x = str(cursor.fetchall()).replace("[","").replace("]","").replace("(","").replace(")","").replace("'","").replace(",","")
        horas = ['07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
        cm=0
        fn=5
        restart = True
        while restart:
            restart = False  
            for i in horas:
                for a in range(20):
                    if i == x[cm:fn]:
                        print(f"Iguais {i} == {x[cm:fn]}")
                        app.root.get_screen('ScreenFour').ids[f"{i}"].line_color=(1, 0, 0, 1)
                        app.root.get_screen('ScreenFour').ids[f"{i}"].text_color=(1, 0, 0, 1)
                        cm = fn+1
                        fn = fn+6
                        restart = True 
                        break 

    def salvarbd(self):
        app = App.get_running_app()
        nome = app.root.get_screen('ScreenThree').ids['nomelb'].text
        hora = app.root.get_screen('ScreenThree').ids['horalb'].text
        data = app.root.get_screen('ScreenThree').ids['datalb'].text
        corte = app.root.get_screen('ScreenThree').ids['cortelb'].text
        con = mysql.connector.connect(host='localhost', database='logdb',user='root',password='admin')
        if con.is_connected():
            cursor = con.cursor()
            cursor.execute(f"insert into admintb(data,hora,nome,corte) VALUES ('{data}','{hora}','{nome}','{corte}')")
            con.commit()
            print(cursor.rowcount, "Gravação feita na tabela admintb")
            cursor.close()
            self.dialog = MDDialog(title="Registro Salvo!",
                                   radius=[20, 20, 20, 20],
                                   md_bg_color=(.87, .74, .61, 1),)
            self.dialog.open()

            app.root.get_screen('ScreenFour').ids[f"{hora}"].line_color=(0, 0, 0, 1)
            app.root.get_screen('ScreenFour').ids[f"{hora}"].text_color=(0, 0, 0, 1)
        else:
            print("Não Conectado!")
            self.dialog = MDDialog(title="Erro de Banco de Dados",
                                   radius=[20, 20, 20, 20],
                                   md_bg_color=(.87, .74, .61, 1),)
            self.dialog.open()

        


class ScreenOne(Screen):
    pass
class ScreenTwo(Screen):
    pass
class ScreenThree(Screen):
    pass
class ScreenFour(Screen):
    pass
class ScreenFive(Screen):
    pass
class ScreenSix(Screen):
    pass
class ScreenAdm(Screen):
    pass



class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()

class Example(MDApp):
    dialog = None


class main(MDApp):


    def build(self):
    
        Window.size = (400,628)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        return Builder.load_file('./appv2.kv')  
main().run()