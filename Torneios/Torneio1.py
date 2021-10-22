'''
Neste problema pretende-se calcular a rota que um carteiro deve fazer para
entregar encomendas num bairro.

O carteiro quer tentar aliviar peso o mais depressa possível, pelo que tenta
sempre ir primeiro (pelo caminho mais rápido) ao maior prédio do bairro,
continuando depois as entregas pela ordem de tamanhos.

O mapa do bairro é dado por uma lista de blocos rectangulares 2D, dados pelas
coordenadas do canto inferior esquerdo e superior direito, sendo que quaisquer
dois ou mais blocos que se toquem (ou intersectem) pertencem ao mesmo prédio.
Se existirem dois prédios com o mesmo tamanho, o carteiro visita primeiro o que
começou a ser definido primeiro no mapa.

O carteiro pode deixar as encomendas de um prédio em qualquer posição que lhe
seja adjacente. Se houver duas posições de um prédio à mesma distância mais
curta, o carteiro dá  prioridade à que estiver mais à esquerda, e, em caso
de empate neste critério, então escolhe a que estiver mais para baixo.

Se um prédio não for acessível então é ignorado, passando o carteiro ao
próximo.

A função a implementar recebe o ponto onde o carteiro começa a visita e o mapa
do bairro. Deve devolver a sequência de pontos onde terá que deixar as encomendas,
intercalada pela respectiva distância.
'''

'''
Pontos de interesse:

1º: Tenta sempre ir primeiro (pelo caminho mais rápido) ao maior prédio!
2º: Se dois blocos ou mais se intersetam, considera-se o mesmo prédio!
3º: Se existirem dois prédios com o mesmo tamanho, vai ao primeiro definido primeiro no mapa!
4º: O carteiro pode deixar as encomendas em qualquer posição adjacente ao prédio!
5º: Se houver duas posições de um prédio à mesma distância opta pela mais à esquerda! (Em caso de empate, a mais em baixo!)
6º: Se um prédio não for acessível então é ignorado, passando o carteiro ao próximo!
7º: Deve devolver a sequência de pontos onde terá que deixar as encomendas, intercalada pela respectiva distância.

    A nossa ideia foi no inicio criar uma lista de listas de predios (contendo os pontos deles) assim como uma lista de lista dos pontos adjacentes
a esses ordenada pela mesma ordem
    Depois juntamos essa lista de lista de predios em uma e criamos assim uma lista de obstaculos chamada "notPath"
    Para fazer a pesquisa precisamos de um dicionario como se fosse um grafo, cujas keys sao os tamanhos dos predios(quantidade de pontos)
e as chaves é uma lista de listas contendo os pontos de entrega desses tais predios chamada deliveryPointDic
    Depois utilizamos uma pesquisa BF e sempre que encontravamos uma distancia minima e o seu respetivo destino de entrega, adicionamos isso
á lista de retorno isto feito da função path
'''


def rota(inicio,blocos):

    #se nao tivermos blocos continuamos no mesmo sitio
    if blocos==[]:
        return [inicio]

    #Vamos criar uma lista de listas com cada predio sendo cada uma das listas um predio (lbuildings)

    lbuildings,adjList = Buildings(blocos)
    lbuildings,adjList = Buildings2(blocos,lbuildings,adjList)

    #este set é para nos guiar como se fossem os "obstaculos" vamos juntar todas as listas
    #do do prediosList num só set
    notPath = set()
    for predio in lbuildings:
        notPath.update(predio)

    #deliveryPointList vai ser um dicionario, as chaves vão ser os tamanhos dos diferentes predios
    #Os tamanhos sao dados pelo numero de pontos de cada um
    #e os valores vao ser uma lista de listas onde tem os varios pontos de entrega dos predios com esse tamanho(chave)
    deliveryPointDic = deliveryPoints(lbuildings,adjList)

    #esta vai ser a lista final de retorno gerada pela funçao caminhos
    ret = path(inicio,deliveryPointDic,notPath)
    return ret




#Esta Função dá-nos um set com todos os pontos adjacentes a um prédio

def buildingAdj (building):
    adj = set()
    for x,y in building:
        if (x+1,y) not in building:
            adj.add((x+1,y))

        if (x-1,y) not in building:
            adj.add((x-1,y))

        if (x,y+1) not in building:
            adj.add((x,y+1))

        if (x,y-1) not in building:
            adj.add((x,y-1))
    return adj



#Esta funçao dá return a uma lista de listas com os pontos de cada predio
#E uma lista de listas pela mesma ordem com os pontos adjacentes a cada predio


def Buildings (blocos):
    buildingsList = []
    adjList = []

    for b in blocos:                          #para cada par de coordenadas dos blocos
        newBuilding = set()                   #vamos criar um set com os pontos dum novo predio
        x1,y1,x2,y2 = b
        for x in range(x1,x2+1):              #vamos percorrer os x
            for y in range(y1,y2+1):          #vamos percorrer os y
                newBuilding.add((x,y))        #adicionamos cada par de pontos
        adj = buildingAdj(newBuilding)        #vamos ver os adjacentes dele
        i=0                                   #contagem
        existe=0                              #flag se ja existe algum predio com um ponto em comum


        # este ciclo while é para juntar predios em comum que se tocam ainda, aqui nao vemos quando um predio depois junta 2
        #enquanto nao chegarmos ao fim da lista de predios que ja achamos e ainda nao encontrar-mos nenhum com pontos em comum

        while (i<len(buildingsList) and existe==0):
            for ponto in newBuilding:                                       #para os pontos do novo predio
                if ponto in buildingsList[i] or ponto in adjList[i] :       #se algum deles coincidir com os pontos de outro predio ou os pontos adjacentes a outro predio
                    existe = 1                                              #colocamos a flag a 1
                    buildingsList[i].update(newBuilding)                    #vamos adicionar ao predio que tem os pontos em comum com este novo predio os pontos deste novo predio
                    adjList[i]=buildingAdj(buildingsList[i])                #e os adjacentes tambem
                    break                                                   #e paramos para aumentar a eficiencia
            i+=1                                                            #avançamos para o proximo predio na lista
        if existe==0:                                                       #se nao existir
            buildingsList.append(newBuilding)                               #colocamos o novo predio no fim da lista
            adjList.append(adj)                                             #e os adjacentes tambem

    return buildingsList,adjList                                            #no final damos return á lista de predios de dos adjacentes


#precisamos desta funçao para fazer uma segunda travessia pois quando no final vem um novo predio que junta 2 nós nao consideramos na funçao em cima

def Buildings2(blocos,buildingsList,adjList):
    used = []
    retBuildings, retAdj = [] , []

    for i in range ( 0 , len(buildingsList)):     #percorremos os edificios
        group = buildingsList[i].copy()     #precisamos de copy neste caso senao vamos ficar com apontador
        adj = adjList[i].copy()             #precisamos de copy neste caso senao vamos ficar com apontador
        for j in range ( i + 1 , len ( buildingsList )):              #percorremos os edificios á frente do i
            flag = 0                                                    #flag quando encontrar um adjacente vamos parar de percorrer (para aumentar eficiencia)
            for p in buildingsList[i]:

                if p in adjList[j] and  j not in used and flag == 0:    #se existe um ponto adjacente ao predio j e o j ainda nao foi usado com outro vamos juntar
                    group.update ( buildingsList[j] )
                    adj.update ( adjList[j] )
                    adj = adj - ( buildingsList[i] & adjList[j])        #tirar os adjacentes repetidos
                    adj = adj - ( buildingsList[j] & adjList[i])        #tirar os adjacentes repetidos
                    used.append ( j )
                    flag = 1

        if i not in used:                                               #se ele nao toca noutros vai ser um predio na lista final
            retBuildings.append ( group )
            retAdj.append ( adj )

    return retBuildings,retAdj



#esta funcao dá-nos os proximos "saltos" que o carteiro pode fazer
#apenas nos dá os proximos 4 saltos, como se fosse funçao do cavalo do treino 2
#vai ser usada como funçao auxiliar da Path que está mais embaixo

def nextAux (point,notPath):
    adjPoints = set()
    x,y= point
    if (x+1,y) not in notPath:
        adjPoints.add((x+1,y))

    if (x-1,y) not in notPath:
        adjPoints.add((x-1,y))

    if (x,y+1) not in notPath:
        adjPoints.add((x,y+1))

    if (x,y-1) not in notPath:
        adjPoints.add((x,y-1))
    return adjPoints


#esta funçao vai calcular o minimo caminho para entregar o proximo pedido justamente com o ponto de entrega destino
#vai ser usada como funçao auxiliar da Path que está mais embaixo


def nextBuildingAux (Start, Buildings, notPath):

    distDic ={}            # dicionario das distancias
    distDic[Start]=0

    minPath = float("inf")       #menor caminho encontrado ate aqui
    dest = (float("inf"),float("inf"))    # destino do menor caminho encontrado ate aqui

    queue = [Start]
    v = Start

    #continuamos enquanto tivermos elementos na queue(proximas posiçoes para ver)
    #e tivermos andado menos que 50 passo (foi a maneira que arranjamos para testar inacessiveis)
    #pensamos em usar um algoritmo por cores para testar ciclos mas não conseguimos implementar

    while queue and distDic[v] < 50:
        v = queue.pop(0)
        if v in Buildings:
            if minPath > distDic[v]:         # se encontrarmos um novo caminho melhor, vamos guardar-lo
                minPath = distDic[v]         # a distancia dele
                dest = v                        # e o destino dele

            # caso for o mesmo comprimento do menor caminho anterior testamos pelo X mais á esquerda
            elif minPath == distDic[v] and v[0] < dest[0]:
                dest = v

            # se o x mais á esquerda tambem for igual, testamos pelo Y mais em baixo
            elif minPath == distDic[v] and v[0] == dest[0] and v[1] < dest[1]:
                dest=v


        nextPaths = nextAux (v,notPath)             #aqui vamos procurar os proximos caminhos possiveis
        for n in nextPaths:                         #para cada caminho possivel
            if n not in distDic:                    #se n ainda nao tiver sido visitado
                distDic[n]=distDic[v]+1             #a distancia dele vai ser a distancia ate agora +1
                queue.append(n)                     #e colocamos na queue para depois o visitar

    return minPath,dest




#algoritmo principal que nos vai dar return ao caminho total
#utilizamos uma travessia BF em largura, esta funçao usa as 2 funçoes auxiliares em cima declaradas
#Com o intuito de ficarmos a saber qual a rota final a ser tomada pelo carteiro
#A funçao vai usar o ponto inicial, o dicinario deliveryPointDic que tem tamanhos dos predios como keys e os seus pontos de entrega como valores
#e também a notPath que é a lista dos obstáculos

def path (start, deliveryPointDic, notPath):
    point = start
    finalPath = [start]
    while deliveryPointDic:
        t=max(deliveryPointDic.keys())                                              #vamos aos predio/predios maiores
        for buildingDeliveryPoints in deliveryPointDic[t]:                          #para cada edificio com esse tamanho
            if point not in buildingDeliveryPoints:                                  #se o ponto não for zona de entrega ainda vamos procurar um caminho ate a zona de entrega
                dist,point=nextBuildingAux (point, buildingDeliveryPoints, notPath)  #chamada auxiliar para nos dar distancia e caminho para o proximo predio
                if (dist != float("inf")):                                           #se for inf quer dizer que é inacessivel por isso nao colocamos
                    finalPath.append(dist)
                    finalPath.append(point)
        deliveryPointDic.pop(t)                                                     #ja vimos todos os predios com este tamanho
    return finalPath



#esta funçao dá-nos todos os pontos possíveis de entrega

def deliveryPoints (buildingsList,adjList):
    ret = {}
    for i in range(0,len(buildingsList)):
        t=len(buildingsList[i])
        if t not in ret:
            ret[t]=[]
        ret[t].append(adjList[i])
    return ret
