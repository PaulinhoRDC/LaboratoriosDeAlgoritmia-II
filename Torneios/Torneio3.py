'''
Neste torneio pretende-se que implemente um programa que ajude um arquiteto a
planear os prédios a construir num bairro.

Um bairro de dimensão N é uma matriz quadrada com N x N lotes de iguais dimensões.
Em cada lote deve ser construído um prédio. As alturas dos prédios variam entre
1 e N, sendo que em cada linha e coluna do bairro as alturas dos prédios devem ser
todas diferentes. Alguns lotes podem já ter um prédio previamente construído.

Para além destas retrições, o arquiteto tem que respeitar algumas regras de
visibilidade: para cada coluna e para cada linha podem ser indicados quantos
prédios devem ser visíveis em cada uma das direcções.

Considere por exemplo o seguinte esquema para um bairro de dimensão N = 4.

    3 . . 1
    v v v v
. > . . . . < .
. > . 4 . . < 2
. > . . . . < .
1 > . . . 3 < .
    ^ ^ ^ ^
    . . 2 .

Dois dos lotes deste bairro já têm prédios constuídos (de alturas 4 e 3). Na primeira
coluna só podem estar visíveis 3 prédios quando olhando de Norte para Sul. Na terceira
coluna só podem estar visíveis 2 prédios quando olhando de Sul para Norte. Na quarta
coluna só pode estar visível um prédio quando olhando de Norte para Sul. Na segunda
linha só podem estar visíveis 2 prédios quando olhando de Este para Oeste. Finalmente,
na quarta linha só pode estar visível um prédio quando olhando de Oeste para Este.

O programa deve calcular um possível projeto para o bairro, nomeadamente as alturas dos
prédios a construir em cada lote, que respeite todas as restrições dadas. Só serão dados
problemas onde tal é possível. Pode existir mais do que um projeto que satisfaz todas as
restrições, podendo neste caso ser devolvido qualquer um deles.

A função a implementar recebe 5 parâmetros:
- m é uma matriz quadrada (representada por uma lista de listas) que descreve quais os
  prédios já existentes. Se um lote estiver vazio a lista irá conter um None na posição
  respectiva.
- t é uma lista com as restrições de visibilidade para as colunas, quando olhando de Norte
  para Sul. Se não existir restrição para uma determinada coluna existirá um None na
  posição respectiva.
- b é uma lista com as restrições de visibilidade para as colunas, quando olhando de Sul
  para Norte. Se não existir restrição para uma determinada coluna existirá um None na
  posição respectiva.
- l é uma lista com as restrições de visibilidade para as linhas, quando olhando de Oeste
  para Este. Se não existir restrição para uma determinada linha existirá um None na
  posição respectiva.
- r é uma lista com as restrições de visibilidade para as linhas, quando olhando de Este
  para Oeste. Se não existir restrição para uma determinada linha existirá um None na
  posição respectiva.

A função deverá devolver uma matriz quadrada (representada por uma lista de listas) com as
alturas projetadas para todos os lotes.
'''

def okT (m,i,j,t):
    max = 0
    c = t[j]
    visiveis = 0
    numeroNone = 0

    if (m[0][j]) != None:
        if (len(m[0]) - m[0][j] +1) < c : return False

    for ii in range (0,len(m),1):
        if m[ii][j] == None:
            numeroNone += 1
        elif m[ii][j] >= max:
            max = m[ii][j]
            visiveis += 1


    if numeroNone == 0 and visiveis > c : return False
    if visiveis + numeroNone >= c : return True
    return False


def okB (m,i,j,b):
    max = 0
    c = b[j]
    visiveis = 0
    numeroNone = 0

    if (m[len(m[0])-1][j]) != None:
        if (len(m[0]) - m[len(m[0])-1][j] +1) < c : return False

    for ii in range (len(m)-1,-1,-1):
        if m[ii][j] == None:
            numeroNone += 1
        elif m[ii][j] >= max:
            max = m[ii][j]
            visiveis +=1



    if numeroNone == 0 and visiveis > c : return False
    if visiveis + numeroNone >= c : return True
    return False



def okL(m,i,j,l):
    max = 0
    c = l[i]
    visiveis = 0
    numeroNone = 0

    if (m[i][0]) != None:
        if (len(m[0]) - m[i][0] +1) < c : return False


    for jj in range (0,len(m),1):
        if m[i][jj] == None:
            numeroNone += 1
        elif m[i][jj] >= max:
            max = m[i][jj]
            visiveis += 1



    if numeroNone == 0 and visiveis > c : return False
    if visiveis + numeroNone >= c : return True
    return False



def okR (m,i,j,r):
    max = 0
    c = r[i]
    visiveis = 0
    numeroNone = 0

    if (m[i][len(m[0])-1]) != None:
        if (len(m[0]) -m[i][len(m[0])-1] +1) < c : return False

    for jj in range (len(m)-1,-1,-1):
        if m[i][jj] == None:
            numeroNone += 1
        elif m[i][jj] >= max:
            max = m[i][jj]
            visiveis += 1



    if numeroNone == 0 and visiveis > c : return False
    if visiveis + numeroNone >= c : return True
    return False



def notBefore(m,i,j,x):
    if x in m[i]:
        return False
    for k in range (0,i+1):
        if m[k][j] == x:
            return False
    return True



def ok(m,x,i,j,t,b,l,r):

    m[i][j] = None
    if ( not notBefore(m,i,j,x)): return False

    m[i][j] = x
    if t[j] != None:
        if(not okT(m,i,j,t)):
            m[i][j] = None
            return False


    if b[j] != None:
        if(not okB(m,i,j,b)):
            m[i][j] = None
            return False

    if l[i] != None:
        if(not okL(m,i,j,l)):
            m[i][j] = None
            return False

    if r[i] != None:
        if(not okR(m,i,j,r)):
            m[i][j] = None
            return False

    m[i][j] = None

    return True




def complete (m):
    for linha in m:
        if None in linha:
            return False
    return True

def extensions (m,xx,yy,t,b,l,r):

    return [x for x in range (1,len(m)+1) if ok(m,x,xx,yy,t,b,l,r)]




def colocaMaisAlto(m,t,b,l,r):
    tamanho = len(m[0])

    while (1 in t):
        i = t.index(1)
        t[i] = None
        m[0][i] = tamanho


    while(1 in b):
        i = b.index(1)
        b[i] = None
        m[tamanho-1][i] = tamanho


    while(1 in l):
        i = l.index(1)
        l[i] = None
        m[i][0] = tamanho


    while(1 in r):
        i = r.index(1)
        r[i] = None
        m[i][tamanho-1] = tamanho




def projeto(m,t,b,l,r):
    colocaMaisAlto (m,t,b,l,r)
    if projetoAux(m,t,b,l,r,0,0):
        return m


def proximo (m,antX,antY):
    f = 0

    if m[antX][antY] != None:
        if antY == len(m)+1:
            if m[antX+1][0] == None:
                return  antX+1,0
            if m[antX][antY+1]:
                return antX,antY+1
    for i in range(0,len(m)):
        if f==0:
            for j in range(0,len(m)):
                if m[i][j] == None:
                    xx,yy = i,j
                    f = 1
                    break
        else:
            break
    return xx,yy

def projetoAux(m,t,b,l,r,antX,antY):
    if m[len(m)-1][len(m)-1] != None and complete(m):
        return True


    x,y = proximo (m,antX,antY)
    ll = extensions(m,x,y,t,b,l,r)
    m[x][y] = None


    for elem in ll:
        m[x][y] = elem
        if projetoAux(m,t,b,l,r,x,y): return True
        m[x][y] = None

    return False
