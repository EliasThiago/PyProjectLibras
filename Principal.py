import cv2 #OpenCV - responsavel pela webcam/processamento de imagem/Comparacao de imagem
import os # abrir o manual 
import time #time delay usado na webcam
import gtk
import ctypes #mensagem de erro
from Tkinter import Tk #Objeto responsavel pela janela: abrir imagem/salvar imagem
from tkFileDialog import askopenfilename,asksaveasfilename #Construtor de abrir imagem/salvar imagem
from threading import Thread #Uso de Thread para o funcionamento da webcam 
from matplotlib import pyplot as plt
from cv2 import imread
gtk.gdk.threads_init()
#Criando a Classe do Programa
class Principal(object):
    def __init__(self):     
    #Carregar o arquivo XML gerado pelo Glade.
        builder = gtk.Builder() #Primeiramente criamos uma inst?ncia da classe
        builder.add_from_file("Interface.glade") #Fun??o para carregar o arquivo
    #Obtendo o widget window1 nossa janela principal
        self.window = builder.get_object("window_one")
    #Inserir o icone da janela    
        self.window = builder.get_object("window_one")
    #Obtendo o widget text_entry 
        self.text_area = builder.get_object("text_entry")
    #Obtendo a caixa de mensagem de erro message dialog
        self.about= builder.get_object("window_help")
    #Obtendo o widget de evento      
        self.image_box = builder.get_object("image_box") 
    #Obtendo  o widget de referente ao campo de imagem Gtk.image
        self.imagecam = builder.get_object ("campoimagem")
        self.imagecam.set_from_file("Libras.jpg") #setando a imagem de entrada do campo aonde sao reproduzidas as imagens
    #Variavel de selecao dentro do radio button
        self.RadioButt = 0 #disponivel no inicio abrir a imagem
    #variavel de aquisicao de foto e inicio de analise
        self.Analise = 0 
        self.threadflag = 0
    #variavel auxiliar para salvar 
        self.varsave = 0
        self.count = 0 
        self.cont = 0
        self.t = 0
        self.c = True
    #Exibindo a janela do programa
        self.window.show()
        builder.connect_signals({
        #Definindo direcionando e criando as acoes                         
                            "gtk_main_quit": gtk.main_quit,
                            #Sinal da janela principal, conectada a funcao
                            #do gtk que fecha o programa tanto referencia na janela principal
                            "on_imagemenuiteminfo_activate":self.on_imagemenuiteminfo_activate,                        
                            #Sinal da janela principal, conectada a funcao
                            #do gtk que chama o arquivo de texto com o manual
                            "on_imagemenuitemcor_activate":self.on_imagemenuitemcor_activate,
                            #Sinal do radio button Imagem, nele uma variavel RadioButt recebera valor 0    
                            "on_radioButtImg_activate":self.on_radioButtImg_activate,
                            #Sinal do radio button Web, nele uma variavel RadioButt recebera valor 1 
                            "on_radioButtWeb_activate":self.on_radioButtWeb_activate,
                            #Sinal do botao que faz receber a imagem 
                            "on_botaoselecionar_activate":self.on_botaoselecionar_activate,
                            #Sinal do botao que faz a analise da imagem
                            "on_analise_image":self.on_analise_image,
                            "on_analise_activate":self.on_analise_activate,
                            #Sinal do botao que faz receber o audio da palavra na area de texto
                            "on_reprod_audio_activate":self.on_reprod_audio_activate,
                            #Sinal do botao que salva a imagem
                            "on_save_image":self.on_save_image,
                            #Sinal da abertura do manual
                            "on_open_menu":self.on_open_menu,
        })
    #Criando as funcoes de acao de botao
    def thread_gtk(self):
        """Funcao responsavel pelas threads da webcam""" 
        # changed this function. Improved threading.
        self.thrd = Thread(target=self.show_image, name = "GTK thread")
        self.thrd.daemon = True
        self.thrd.start()
    def on_open_menu (self, widget):
        """Funcao para abrir o manual"""       
        #Executa o arquivo em pdf filename que e referente ao manual de uso
        os.startfile('manual.docx')
    def on_imagemenuiteminfo_activate(self, widget):
        """Funcao para exibir a Janela Sobre do programa"""
        #Executando a Janela Sobre
        self.about.run()
        #Ativando a opcao fechar da Janela Sobre
        self.about.hide()
    def on_imagemenuitemcor_activate(self, widget):
        """Funcao para exibir o manual do programa"""
        #Executando a Janela Sobre
        self.window_color.run()
        #Ativando a opcao fechar da Janela Sobre
        self.window_color.hide()    
    def on_radioButtImg_activate(self, widget):
        """Funcao responsavel pelo RadioButton"""
        self.RadioButt = 0
    def on_radioButtWeb_activate(self, widget):
        """Funcao responsavel pelo RadioButton"""
        self.RadioButt = 1
        
    def on_botaoselecionar_activate(self, widget):
        """Funcao responsavel pelo RadioButton"""
        
        if self.count == 1:
            self.camera.release()
            self.c = True
            self.count = 0
        if self.RadioButt == 1:
            self.camera = cv2.VideoCapture(0)
            self.count = 1
            if not self.threadflag:
                app.thread_gtk()                   # gtk.main() only once (first time)
                app.threadflag=0                     # change flag
        else:
            self.c = False
            root = Tk()
            root.iconbitmap(default='favicon.ico')
            root.withdraw()
            self.file = askopenfilename(filetypes=[("JPEG", "*.jpg; *.jpe; *.jpeg; *.jfif"),
                                 ("Bitmap Files","*read().bmp; *.dib"),
                                 ("PNG", "*.png"),
                                 ("TIFF", "*.tiff; *.tif")],initialdir = 'C:\\',multiple = False,title = "Abrindo imagens..")
            
            self.imagecam.set_from_file(self.file)    
            self.varsave = 1 
    def show_image(self):
        """Funcao responsavel pelo RadioButton"""
        time.sleep(1)
        self.retval, imagem = self.camera.read()
        self.varsave = 0
        if self.retval == False:
            ctypes.windll.user32.MessageBoxA(0, 'Nao ha cameras inseridas em seu computador!!', 'Erro camera', 0)
        else:
            self.c = True
            time.sleep(0.6)#tempo de espera para ativacao da webcam
            while self.c:
                retorno, self.imagem = self.camera.read()
                cv2.rectangle(self.imagem,(449,336),(192,144), (230, 230, 230), 3)
                img_pixbuf = gtk.gdk.pixbuf_new_from_data(self.imagem.tostring(),gtk.gdk.COLORSPACE_RGB,False,8,640,480,640*3)
                self.imagecam.set_from_pixbuf(img_pixbuf)
                self.imagecam.show()
                self.window.show_all() 
                time.sleep(0.4)
                if self.cont == 1:
                    self.t = self.t +1
                    self.imagecam.set_from_file("num/numero" + str(self.t) +".jpg")
                    self.imagecam.show()
                    self.window.show_all() 
                    time.sleep(0.6)   
                    self.imagecam.show()
                    self.window.show_all() 
                    if self.t == 4:
                        self.t = 0 
                        retorno, imagem = self.camera.read()
                        self.img_pixbuf = gtk.gdk.pixbuf_new_from_data(imagem.tostring(),gtk.gdk.COLORSPACE_RGB,False,8,640,480,640*3)
                        self.imagecam.set_from_pixbuf(self.img_pixbuf)
                        self.imagecam.show()
                        self.window.show_all() 
                        self.cont = 0
                        self.im = imagem
                        self.camera.release()
                        self.on_analise_image(imagem)
                        self.c = False
            

    def on_save_image(self, widget):
        """Funcao para salvar imagem"""
        root = Tk()
        root.iconbitmap(default='favicon.ico')
        root.withdraw()
        FileSave = asksaveasfilename(filetypes=[("JPEG", "*.jpg; *.jpe; *.jpeg; *.jfif"),],
                                        initialdir = 'C:\\',title = "Salvando a imagem..",
                                        initialfile = "*.jpg")
        if self.varsave == 1: 
            self.output_img = cv2.imread(self.file,1)
            self.varsave = 0
            cv2.imwrite(FileSave,self.output_img)
        else:
            #criar uma logica para salvar imagens tiradas da webcam
            cv2.imwrite(FileSave,self.im)
            self.varsave = 0
            
    def on_analise_activate (self, widget):
        """Funcao responsavel pela analise"""  
        if self.RadioButt == 1:
            self.cont = 1 
        else:
            self.text_area.set_text('ANALISANDO!!')
            imagem = cv2.imread(self.file)
            self.on_analise_image(imagem)
            
                 
    def on_analise_image (self,widget):
        """Funcao responsavel pela analise"""     
        p=0
        z = widget
        cv2.imwrite('temp.jpg',z)
        z = cv2.imread('temp.jpg',0)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl1 = clahe.apply(z) 
        cv2.imwrite('temp.jpg',cl1)
        z = cv2.imread('temp.jpg')
        ret1,thresh1 = cv2.threshold(cv2.cvtColor(cv2.GaussianBlur(z, (3,3),0 ),cv2.COLOR_BGR2GRAY),70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        sift = cv2.SIFT()
        kp1,des1=sift.compute(thresh1,cv2.FeatureDetector_create("Dense").detect(thresh1))
        lista1 = []
        lista2 =[]
        for y in xrange(1, 6):#5 sinais
            self.text_area.set_text("ANALISANDO CICLO NUMERO "+ str(y)+"....")
            start = time.time()
            for x in range(1, 8):#total de 7 imagens por sinal]
                z = cv2.imread('caracter/'+str(y)+'-'+str(x)+'.jpg') # imagens de treino 
                ret1,thresh2 = cv2.threshold(cv2.cvtColor(cv2.GaussianBlur(z,(1,1),0),cv2.COLOR_BGR2GRAY),70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
                kp2,des2=sift.compute(thresh2,cv2.FeatureDetector_create("Dense").detect(thresh2))
                matches = cv2.FlannBasedMatcher(dict(algorithm = 0, trees = 10), dict(checks = 10)).knnMatch(des1,des2,k=2)#algorithm = FLANN_INDEX_KDTREE
                good = []
                for m,n in matches:
                    if m.distance < 0.1*n.distance:
                        good.append(m)
                lista2.insert(x,len(good))
            print time.time() - start;
            lista2.remove(min(lista2))
            lista2.remove(max(lista2))
            lista1.insert(y, sum(lista2)/5)
            print lista1
            print 
            if (sum(lista2)/5) <= 25: #SCORE comparacao
                p = p + 1
                if p == 5:
                    y = 6
                    p=0
                    self.text_area.set_text('PRONTO!! NAO E UM SINAL!!')
                    return
            lista2 =[]
        w = lista1.index(max(lista1)) + 1
        self.text_area.set_text('A IMAGEM CORRESPONDE AO NUMERAL: ' + str(w))
        w = 0
    def on_reprod_audio_activate (self, widget):
        """Funcao para rodar o audio"""
        #modificar esta parte
if __name__ == "__main__":
    #Criando uma instancia do Programa
    app = Principal()
    gtk.main()
    
