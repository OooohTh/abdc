# IDENTIFIQUE-SE NA LINHA ABAIXO
__author__ = "name = André Mogarro Duarte Pires Sá, number = ist1109904"

from dataclasses import dataclass
from math import sin, cos, sqrt, radians, asin, floor

#Earth radius.
ER = 6371.0
#Earth Circumference.
EC = 40075.0

@dataclass
class Connection:
    iata_origin: str #Código IATA do aeroporto de origem.
    iata_destination:str #Código IATA do aeroporto de chegada.
    kms: int #Distância entre os aeroportos.

COORD_LIMIT = 180

@dataclass
class Coordinates:
    lat : float #Latitude.
    lon : float #Longitude.

@dataclass
class Airport:
    name: str  #Nome da cidade mais próxima do aeroporto.
    country: str   #Nome do país do aeroporto.
    iata: str  #Código IATA do aeroporto.
    coord: Coordinates #Coordenada (latitude e longitude) do aeroporto.
    outgoing: dict[str,Connection] #Dicionário das ligações desde o aeroporto até a outros aeroportos.
                                     #As keys do dicionário são os códigos IATA dos aeroportos de chegada,
                                     #e os valores são as ligações em si.

@dataclass
class AirMap:
    name: str  #Nome do Airmap.
    num_airports: int  #Numero de aeroportos no Airmap.
    num_connections: int   #Numero de ligações no Airmap.
    airports: dict[str,Airport]    #Dicionário que liga os códigos IATA dos aeroportos do Airmap aos aeroportos em si.


def check_string(string:str) -> bool:
    """Verifica se um input é uma string não vazia."""
    if isinstance(string,str) and string:
        return True
    return False


def check_iata(iata:str) -> bool:
    """Verifica se um input é um código iata válido (3 letras maiúsculas)."""
    if check_string(iata) and len(iata)==3 and iata.upper()==iata and iata.isalpha():
        return True
    return False


def haversine_formula(lat1:float, lat2:float, lon1:float, lon2:float) -> int:
    """Calcula a distância entre dois pontos no globo de acordo com a fórmula de Haversine."""
    return floor(2*ER*asin(sqrt((sin((lat2-lat1)/2))**2+(cos(lat1)*cos(lat2)*(sin((lon2-lon1)/2))**2))))


def new_airmap(name:str) -> AirMap:
    """Cria um novo Airmap."""
    return AirMap(name=name,num_airports=0,num_connections=0,airports={})


def new_coordinates(lat:float, lon:float) -> (Coordinates|None):
    """Cria um novo conjunto de coordenadas desde que a latitude dada esteja entre -90 e 90 e que a longitude dada esteja entre -180 e 180."""
    if -90<=lat<=90 and -180<=lon<=180:
        return Coordinates(lat=lat,lon=lon)
    return None


def new_airport(name:str,country:str,iata:str,coo:Coordinates) -> (Airport|None):
    """Cria um novo aeroporto desde que o nome, o país, e o código iata sejam válidos. Caso contrário, devolve 'None'."""
    if check_string(name) and check_string(country) and check_iata(iata):
        return Airport(name,country,iata,coo,{})
    return None


def add_airport(w:AirMap,a:Airport)->(int|None):
    """Adiciona um aeroporto 'a' ao Airmap 'w', e devolve o número de de aeroportos no Airmap 'w' após a adição, desde que o aeroporto não estivesse já no Airmap.
    Caso contrário, devolve 'None'."""
    if a.iata not in w.airports and a.outgoing=={}:
        w.airports[a.iata]=a
        w.num_airports+=1
        return w.num_airports
    return None


def new_connection(origin:str, destination:str, kms:int) -> (Connection|None):
    """Cria e devolve uma ligação entre dois aeroportos, desde que o código IATA dos aeroportos de
    partida e de chegada seja válido e que a distância entre eles seja menor que metade da
    circunferência da Terra. Caso contrário, devolve 'None'."""
    if check_iata(origin) and check_iata(destination) and 0<kms<EC/2:
        return Connection(origin,destination,kms)
    return None

def compute_distance(a1:Airport,a2:Airport) -> int:
    """Calcula e devolve a distância entre dois aeroportos."""
    lat1=radians(a1.coord.lat)
    lat2=radians(a2.coord.lat)
    lon1=radians(a1.coord.lon)
    lon2=radians(a2.coord.lon)
    distance=haversine_formula(lat1,lat2,lon1,lon2)
    return distance


def add_connection(w:AirMap,s:str,d:str)->(int|None):
    """Cria uma ligação entre dois aeroportos de um Airmap 'w': um aeroporto de partida,
    representado pelo código IATA 's', e um aeroporto de chegada, representado pelo código IATA 'd'.
    Adiciona a ligação criada ao dicionário de ligações do aeroporto de partida,
    desde que os argumentos cumpram determinadas condições."""
    if s in w.airports and d in w.airports: #A funçao verifica que ambos os códigos IATA dados se encontram presentes no dicionário de aeroportos do Airmap 'w'
        if d not in w.airports[s].outgoing: #A função verifica que o código IATA 'd' não está no dicionário de ligações do aeroporto de partida.
            distance=compute_distance(w.airports[s],w.airports[d])
            connection=new_connection(s,d,distance)
            w.airports[s].outgoing[d]=connection
            w.num_connections+=1
            return w.num_connections
    #Caso alguma das verificações anteriores seja falsa, a função devolve 'None'
    return None

def route_distance(w:AirMap,route:list[str]) -> (int|None):
    """Verifica se 'route' é um trajeto válido. Se for devolve a distância total percorrida nesse trajeto. Se não, devolve 'None'."""
    totaldistance=0
    Used_Airports=set({})
    for i in range(len(route)):
        if i!=len(route)-1: #Se route[i] for o último elemento de route, o próximo passo não é efetuado
            if route[i+1] in w.airports[route[i]].outgoing and route[i+1] not in Used_Airports: #Verifica se existe uma ligação no Airmap 'w' entre o aeroporto cujo código iata é route[i] e o aeroporto cujo código iata é route [i+1], e se o aeroporto de destino já tinha sido utilizado
                #Adiciona a distância entre os aeroportos representados pelo código IATA 'route[i]' e 'route [i+1]'
                distance=w.airports[route[i]].outgoing[route[i+1]].kms
                totaldistance+=distance
                Used_Airports.add(route[i])
            else:
                return None
    return totaldistance


def near_hops(w:AirMap,a:Airport,hops:int) -> (set[str]|None):
    """A função devolve um set de aeroportos que estão acessíveis ao aeroporto 'a' com um determinado número de hops."""
    if hops>=0: #A função verifica que o número de hops não é negativo
        airports_to_check={a.iata} #Cria-se um set para os aeroportos cujas connections vão ser verificadas nos for loops abaixo
        airports_to_check_next={a.iata} #Neste set vão estar os aeroportos de destino das connections dos aeroportos do set 'airports_to_check'
        for i in range (hops): #Este loop corre um número de vezes igual ao número de hops
            for airport in airports_to_check: 
                for iatas in w.airports[airport].outgoing:
                    airports_to_check_next.add(iatas)
            airports_to_check.update(airports_to_check_next)
        return airports_to_check
    return None

def near_distance(w:AirMap,a:Airport,radius_kms:int) -> (set[str]|None):
    """A função devovlve um set de aeroportos do Airmap 'w' que esteja a menos de 'radius_km' do aeroporto 'a'."""
    if radius_kms>=0:
        #Aqui define-se o set já com o elemento a, pois este tem sempre de conter a, mas se o raio de procura fosse 0,
        #o aeroporto a não estaria contido no set, pois a função só acrescenta os aeroportos com uma distância inferior
        #ao raio de procura
        near_airports_set={a.iata}
        for airport_iata in w.airports: #Este loop verifica para cada aeroporto no Airmap 'w' se estão a uma distância menor que o raio de procura de 'a'.
            if airport_iata!=a.iata and compute_distance(a,w.airports[airport_iata])<radius_kms:
                 near_airports_set.add(airport_iata) #Se a distância a 'a' for menor que o raio de procura, o aeroporto é adicionado a este set, que é devolvido no final da função
        return near_airports_set
    return None