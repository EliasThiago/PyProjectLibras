import cv2
import numpy as np
from matplotlib import pyplot as plt
from numpy import median

# Variaveis principais  
FLANN_INDEX_KDTREE = 0
REGARDING_DISTANCE = 0.1
SCORE = 10
# recebimento da imagem a ser analisada 

sift = cv2.SIFT()
t=0
d=0
lista1 = []
lista2 = []
for y in xrange(1, 6):#5 sinais
    for w in xrange(1, 8):
        img1 = cv2.imread('caracter/'+str(y)+'-'+str(w)+'.jpg') # 
        im = cv2.GaussianBlur(img1,(5,5),0) #filtro Desfoque baseado na diferenca gaussiana
        gray1 = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
#Binarizando a imagem
        ret,thresh1 = cv2.threshold(gray1,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) 
#criacao do objeto SIFT
    
#Definindo que ele sera denso (hibridismo do modelo SIFT) 
        dense=cv2.FeatureDetector_create("Dense")
        kp=dense.detect(thresh1)
        kp1,des1=sift.compute(thresh1,kp)
    
        for x in range(1, 31):#total de 7 imagens por sinal 
            z = cv2.imread('falsa/'+str(x)+'.jpg') # imagens de treino 
            img = cv2.GaussianBlur(z,(5,5),0)
            gray2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret1,thresh2 = cv2.threshold(gray2,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
#O metodo proposto e capaz de fornecer um mapa exato e denso de pontos homologos (variacao do metodo Sift)
            dense=cv2.FeatureDetector_create("Dense")
            kp=dense.detect(thresh2)
            kp2,des2=sift.compute(thresh2,kp)
# O metodo dict() permite transformar listas de tuplas em dicionarios
# trees: O numero de arvores-kd paralelas que podem ser usadas. Bons valores estao no intervalo [1..16]
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 10) 
# Ele especifica o numero de vezes que as arvores devem ser percorridas
            search_params = dict(checks = 50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(des1,des2,k=2)
# Armazenando todas as boas correspondencias de acordo com o teste de razao de Lowe
            good = []
            for m,n in matches:
# rejeitadas todas as correspondencias em que a relacao de distancia for superior a 0.7 u.d.
                if m.distance < REGARDING_DISTANCE*n.distance:
                    good.append(m)
            lista1.insert(x,len(good))
            
        lista2.insert(w,(sum(lista1)/30))
        print lista2
        lista1 =[]
        print
v = sum(lista2)/35