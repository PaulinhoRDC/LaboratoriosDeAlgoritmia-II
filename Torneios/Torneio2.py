'''
Neste torneio pretende-se que implemente uma função que processa uma mensagem.

A mensagem é constituída por vários blocos de letras separados por ';'.

Cada bloco é recebido num formato comprimido: um número seguido de uma
sequência entre parêntesis significa que essa sequência é repetida o número
de vezes indicado.

A função deve começar por descomprimir os blocos e filtrar os blocos vazios.

Depois deve filtrar os blocos que concordam com um padrão que também é parâmetro
da função processa. Um bloco concorda com um padrão se for possível obtê-lo a partir
do padrão substituindo cada caracter '?' por uma letra e cada caracter '*' por um
número arbitrário de letras. Por exemplo, 'aabxaxb' concorda com o padrão 'a*?b',
enquanto que 'ab' já não.

Depois de filtrar a função deve introduzir redundância na mensagem, repetindo
alguns blocos. Deve escolher os blocos a repetir por forma a maximizar o
número total de caracteres da mensagem, mas garantindo que nunca repete dois
blocos consecutivos.

Finalmente a função deve voltar a comprimir os blocos resultantes, com o cuidado
de comprimir o máximo possível.
'''


'''
Função que basicamente aborda todos os objetivos para resolver o problema pretendido
Chama tanto a função "unzip" como a "correctPattern", "repeat" e "zip"!!!
Assim como  tambem separa as mensagens nos ";" filtra as mensagens vazias e coloca
novamente numa unica mensagens juntanto com ";"
'''

def processa(mensagem,padrao):
    if mensagem == '':
        return ''


    '''
    separar e meter numa lista
    '''
    listaMensagensComprimida = mensagem.split(";")

    '''
    descomprimir e filtrar as vazias
    '''

    if "" in listaMensagensComprimida:
        listaMensagensComprimida.remove("")

    listaExtenso = []

    for i in range(0,len(listaMensagensComprimida)):
        cm=listaMensagensComprimida[i]
        dm=unzip(cm)
        listaExtenso.append(dm)

    '''
    filtrar as mensagens que cumprem o padrao
    '''

    l=[]

    for mensagem in listaExtenso:
        if correctPattern(mensagem,padrao):
            l.append(mensagem)


    '''
    repetir para a maior len possivel
    '''
    l=repeat(l)

    '''
    comprimir
    '''
    l = zip(l)

    #juntamos a lista como uma string com ";"
    l = ";".join(l)

    return  l


'''
Função criada para comprimir a mensagem na menor length possível!
Utiliza uma auxiliar "zipAux" para apoio neste objetivo pretendido!
"ZipAux" utiliza ainda outra  função auxiliar "quantasVezes",
para `que seja possível obter o resultado pretendido!
'''

def zip (mensagemTotal):
    listaFinal = []
    dic = {}
    dic2 ={}
    for mensagem in mensagemTotal:                       #comprimir todas
        if mensagem not in dic:
            mensagemComprimida = zipAux(mensagem,dic2)
            dic[mensagem] = mensagemComprimida             #memorization
        else:
            mensagemComprimida = dic[mensagem]             #se ja tivermos feito
        listaFinal.append(mensagemComprimida)
    return listaFinal

'''
cria um dicionario de dicionarios com a primeira chave sendo indices, a segunda padroes e o valor é o numero de repetiçoes de tal padrao nesse indice
'''

def zipAux(mensagem,c):
    d={}
    d[-1]=''
    d[0]=mensagem[0]
    for index in range(1,len(mensagem)):
        pattern=mensagem[index]
        repeticoes=1
        indice=index-1
        comp=d[indice]+pattern
        for j in range(index,int(index/2),-1):
            if index==j:
                pattern=mensagem[index]
                ind=index-len(pattern)
            else:
                pattern=mensagem[j:index+1]
                ind=index-len(pattern)
            f=1
            rep=1
            par=0
            t=j-len(pattern)
            while t>=0 and f==1:
                if mensagem[t:t+len(pattern)]==pattern:
                    ind-=len(pattern)
                    t-=len(pattern)
                    rep+=1
                else:
                    f=0

            #compressao para lista final

            if pattern not in c:
                if pattern in d:
                    c[pattern]=d[pattern]
                elif len(pattern)>5:                            #menor que 5 nao vale a pena
                    c[pattern]=zipAux(pattern,c)
                else:
                    c[pattern]=pattern
            pattern=c[pattern]
            if len(comp)>(len(d[ind])+len(pattern)+3) :        #so colocamos no final se comprimido for melhor
                padrao=pattern
                repeticoes=rep
                indice=ind
                comp=d[indice]+ str(repeticoes)+'('+padrao+')'
        d[index]=comp
    return d[len(mensagem)-1]


'''
quantas vezes o padrao se vai repetir naquela mensagem a partir do indice 0
'''

def timesPattern (mensagem,pattern):
    jump = len(pattern)
    end = len(mensagem)
    ac = 0
    i = 0

    while (i <= end):
        if (mensagem[i:i+jump] == pattern):
            ac += 1
            i += jump
        else:
            break
    return ac

'''
Função criada com o intuito de meter por extenso a mensagem!
'''

def unzip (string):
    numeroParentecesAtual = 0
    lista = []
    lista.append('')           #para nao estar vazia e dar erro no pop
    r=[]
    r.append(1)
    index = 0
    c = ""

    while index < len ( string ):

        if string[index].isdigit():
            c+=string[index]
            index+=1

        elif string[index] == '(':
            r.append ( int (c) )
            numeroParentecesAtual += 1
            c = ""
            lista.append('')
            index+=1

        elif string[index] ==')':
            p=lista.pop()
            nr=r.pop()
            numeroParentecesAtual-=1
            lista[numeroParentecesAtual]+=nr*p
            index+=1

        else:
            lista[numeroParentecesAtual]=lista[numeroParentecesAtual]+string[index]
            index+=1

    return lista[0]

'''
Função criada com o intuito de criar uma filtração
de todos os blocos que cumprem padrão!
'''
def correctPattern(strr, pattern):

    n = len (strr)
    m = len ( pattern )


    if (m == 0):
        return (n == 0)


    lookup = [[False for i in range(m + 1)] for j in range(n + 1)]

    lookup[0][0] = True


    for j in range(1, m + 1):
        if (pattern[j - 1] == '*'):
            lookup[0][j] = lookup[0][j - 1]

    for i in range(1, n + 1):
        for j in range(1, m + 1):

            if (pattern[j - 1] == '*'):
                lookup[i][j] = lookup[i][j - 1] or lookup[i - 1][j]

            elif (pattern[j - 1] == '?' or strr[i - 1] == pattern[j - 1]):
                lookup[i][j] = lookup[i - 1][j - 1]

            else:
                lookup[i][j] = False

    return lookup[n][m]

'''
Função criada com o objetivo de repetir blocos de forma a maximizar tamanho!
Esta função utiliza uma função auxiliar "indexrepeat", para saber
o índice dos bloco a repetir!
'''

def indexrepeat(lst):

    if len ( lst ) == 1:
        return [0]

    l = []
    d = {}

    l.append(lst[0])
    d[0] = [0]

    if lst[1] > lst[0]:

        l.append(lst[1])
        d[1] = [1]

    else:

        l.append(lst[0])
        d[1] = [0]


    for i in range ( 2 , len(lst)):

        if l[i-1] > l[i-2] + lst[i]:

            l.append(l[i-1])
            d[i] = d[i-1].copy()

        if l[i-1] <= l[i-2] + lst[i]:

            l.append( l[i-2] + lst[i])
            d[i] = d[i-2].copy()
            d[i].append ( i )

        if lst[i] > l[i]:

            l.append(lst[i])
            d[i] = [i]

    return d[len(lst) - 1]


def repeat (listademensagens):

    ans = []

    l = indexrepeat (list (map (lambda t : len ( t ) , listademensagens)))

    for i in range (len (listademensagens)):

        if i in l :

            ans.append (listademensagens[i])
            ans.append (listademensagens[i])

        else:

            ans.append (listademensagens[i])

    return ans
