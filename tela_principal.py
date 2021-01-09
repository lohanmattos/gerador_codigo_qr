#Importando a Biblioteca PyQt5
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

#Importando a nossa tela principal feito no qtdesigner
from gui_qrcode import *

#Importanto as bibliotecas que vamos usar
import pyqrcode
from pathlib import Path
import png
import os



class Tela(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.verifica_caminho()
        self.ui.pushButton_gerar.clicked.connect(self.verifica)
        self.ui.pushButton_carregar_arquivo.clicked.connect(self.abrir_arquivo)
        self.ui.pushButton_gerar_arquivo.clicked.connect(self.gerar_arquivo_qr)
        self.lista_codigos_carregados = []

        self.ui.menuSobre.triggered.connect(self.menssagem_sobre)
     

    def menssagem_sobre(self, item):

        menssagem_texto = ("""Principais Funções:
        1 - Gerar a partir da entrada digitada pelo usuário; ou
        2 - Gerar a partir de uma lista de códigos, que será um arquivo carregado com extensão *.txt 
        
        Os arquivos gerados são salvos na pasta Imagens QR CODE, que será criada quando a aplicação for executada.
        Esta pasta está localizada na pasta principal do usuário. 

        No Windows por Exemplo:
        C:-Users-seu_usuario-Imagens Qr CODE """)
    

        self.menssagem = QMessageBox()
        self.menssagem.setWindowTitle("Sobre o Aplicativo QrCode 1.0")
        self.menssagem.setText("""Esse Aplicativo foi elaborado por: Lohan Amendola - Jan/2021""")
        self.menssagem.setIcon(QMessageBox.Question)
        self.menssagem.setDetailedText(menssagem_texto)
        self.retorno = self.menssagem.exec_()


#Função que verifica se o diretorio existe. 
    def verifica_caminho(self):
        self.caminho = str(Path.home())
        self.diretorio = (self.caminho + '/Imagens QR CODE')

        if not os.path.exists(self.diretorio):
            os.mkdir(self.diretorio)

#Função que gera o arquivo *.png atraves do input do usuário.
    def gerar_text_qr(self):
            code = pyqrcode.create(self.ui.lineEdit_input.text())
            code.png(file=self.diretorio +'/'+ self.ui.lineEdit_input.text() + '.png', scale=8)
            self.ui.label_status_1.setText('O código %s foi gerado com sucesso' % self.ui.lineEdit_input.text())
            self.ui.lineEdit_input.clear()
#Função que verifica se o usuario digitou um nome para o arquivo  
    def verifica(self):
        input_texto = self.ui.lineEdit_input.text()
        if input_texto == '':
            self.ui.label_status_1.setText('Preenha o nome do arquivo')

        else:
            self.gerar_text_qr()

#Função abrir arquivo
    def abrir_arquivo(self):
        self.file,_ = QFileDialog.getOpenFileName(self, "Abrir um arquivo de Texto", "C://", "Arquivo de Texto (*.txt)")
        self.ui.lineEdit_arquivo_carregado.setText(self.file)

#Gerar os códigos através do arquivo carregado
    def gerar_arquivo_qr(self):
        try:
            file = open(self.file)
            for ler in file.readlines():
                retirar_espacos = ler.split()
                for read in retirar_espacos:
                    self.lista_codigos_carregados.append(read)

            #Criando a String nome do arquivo carregado
            self.nome_arquivo = self.file.split('/')
            self.nome = self.nome_arquivo[(len(self.nome_arquivo) - 1)]

            #Percorrendo a lista de codigos carregados e a cada interação do lopp for criando um arquivo *.png com os códigos lidos.           
            for codigos in self.lista_codigos_carregados:
                code = pyqrcode.create(codigos)
                code.png(file=self.diretorio +'/'+ codigos + '.png', scale=8)
                self.ui.label_status_2.setText('O arquivo %s foi gerado com sucesso' % self.nome)

            #Fecha o arquivo aberto      
            file.close()
            self.ui.lineEdit_arquivo_carregado.clear()

        except AttributeError:
            self.ui.label_status_2.setText("Antes de Gerar, abra um arquivo.")


#Inicia a Aplicação 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    t = Tela()
    t.show()
    sys.exit(app.exec_())

