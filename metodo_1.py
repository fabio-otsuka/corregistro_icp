

import numpy as np


from math import factorial
from math import sqrt


# Combinacao Simples
# C(n,p) - n elementos combinados p a p
# C(n,p) = n!/p!*(n-p!)
# 4 pontos
# crio uma array com 4 casas, cada uma ocupada por um vetor (vetores dos pontos)
# array([[- - -], [- - -], [- - -], [- - -]])

# Faco as combinacoes distribuindo os pontos
# array([[1 2 3], [1 2 4], [1 3 4], [2 3 4]])

S = [[117.7,174.3,-230.1],[243.4,180.8,-230.4],[189.0,108.2,-145.8],[189.2,230.3,-116.2]]
Simagem = [[6.0,126.0,69.0],[144.0,127.0,69.0],[80.0,50.0,136.0],[76.0,177.0,186.0]]

#def comb(S):
a = []
b = []
n=len(S)
N = factorial(n)
P = factorial(3)
NP = factorial(n - 3)
C = N / (P * NP)
l=0
for i in range(0,C-2):
    for j in range (i+1,C-1):
        for k in range(j+1,C):
            a.insert(l,[S[i],S[j],S[k]])
            b.insert(l,[Simagem[i],Simagem[j],Simagem[k]])
            l=l+1


#print a[0][0][0]
#print b[0][0][0]


#####################################################################################################
# Criar uma base para cada tripla de pontos e calcular o erro associado a cada uma
e = []
for i in range(0,C):
    #Fiduciais da img
    #self.M, self.q1, self.Minv = db.base_creation(a[i][0],
    #                                           a[i][1],
    #                                           a[i][2])
    #FIducias do rastreador
    #self.N, self.q2, self.Ninv = db.base_creation(b[i][0],
    #                                           b[i][1],
    #                                           b[i][2])

    p1 = np.array(a[i][0])
    p2 = np.array(a[i][1])
    p3 = np.array(a[i][2])
    img1 = np.array(b[i][0])
    img2 = np.array(b[i][1])
    img3 = np.array(b[i][2])

    sub1 = p2 - p1
    sub2 = p3 - p1
    sub3 = img2 - img1
    sub4 = img3 - img1
    lamb1 = (sub1[0] * sub2[0] + sub1[1] * sub2[1] + sub1[2] * sub2[2]) / np.dot(sub1, sub1)
    lamb2 = (sub3[0] * sub4[0] + sub3[1] * sub4[1] + sub3[2] * sub4[2]) / np.dot(sub3, sub3)

    q1 = p1 + lamb1 * sub1
    q2 = img1 + lamb2 * sub3
    g1 = p1 - q1
    g2 = p3 - q1
    gimg1 = img1 - q2
    gimg2 = img3 - q2

    if not g1.any():
        g1 = p2 - q1

    g3 = np.cross(g2, g1)
    gimg3 = np.cross(gimg2, gimg1)

    g1 = g1 / sqrt(np.dot(g1, g1))
    g2 = g2 / sqrt(np.dot(g2, g2))
    g3 = g3 / sqrt(np.dot(g3, g3))

    gimg1 = gimg1 / sqrt(np.dot(gimg1, gimg1))
    gimg2 = gimg2 / sqrt(np.dot(gimg2, gimg2))
    gimg3 = gimg3 / sqrt(np.dot(gimg3, gimg3))

    M = np.matrix([[g1[0], g1[1], g1[2]],
                    [g2[0], g2[1], g2[2]],
                    [g3[0], g3[1], g3[2]]])

    N = np.matrix([[gimg1[0], gimg1[1], gimg1[2]],
                    [gimg2[0], gimg2[1], gimg2[2]],
                    [gimg3[0], gimg3[1], gimg3[2]]])

    q1.shape = (3, 1)
    q2.shape = (3, 1)
    q1 = np.matrix(q1.copy())
    q2 = np.matrix(q2.copy())
    Minv = M.I
    Ninv = M.I


    ponto1 = np.array(b[i][0])
    ponto1.shape = (3,1)
    ponto1 = np.matrix(ponto1.copy())
    ponto2 = np.matrix(b[i][1])
    ponto2.shape = (3,1)
    ponto2 = np.matrix(ponto2.copy())
    ponto3 = np.matrix(b[i][2])
    ponto3.shape = (3,1)
    ponto3 = np.matrix(ponto3.copy())

    imagem1 = np.array(q1 + (Minv * N) * (ponto1 - q2))
    imagem2 = np.array(q1 + (Minv * N) * (ponto2 - q2))
    imagem3 = np.array(q1 + (Minv * N) * (ponto3 - q2))

    ED1=np.sqrt((((imagem1[0]-a[i][0][0])**2) + ((imagem1[1]-a[i][0][1])**2) +((imagem1[2]-a[i][0][2])**2)))
    ED2=np.sqrt((((imagem2[0]-a[i][1][0])**2) + ((imagem2[1]-a[i][1][1])**2) +((imagem2[2]-a[i][1][2])**2)))
    ED3=np.sqrt((((imagem3[0]-a[i][2][0])**2) + ((imagem3[1]-a[i][2][1])**2) +((imagem3[2]-a[i][2][2])**2)))

    FRE = float(np.sqrt((ED1**2 + ED2**2 + ED3**2)/3))
    e.insert(i,[FRE])

####################################################################################################################
# Comparar cada erro, e entao selecionar o menor, associado aos pontos fiduciais

for i in range(0,C):
    for j in range(0,C-1):
        if e[j] > e[j+1]:
            aux=e[j+1]
            e[j+1] = e[j]
            e[j]= aux

            aux = a[j + 1]
            a[j+1] = a[j]
            a[j] = aux

            aux = b[j + 1]
            b[j+1] = b[j]
            b[j] = aux

# selecionar entao a[0], b[0] e e[0]
###############################################################################################################
print a[0]
print b[0]
print e[0]

print a[1]
print b[1]
print e[1]

print a[2]
print b[2]
print e[2]

print a[3]
print b[3]
print e[3]
