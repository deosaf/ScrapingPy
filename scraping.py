#Importar las librerias
from ast import Return
import requests
import lxml.html as html
import pandas as pd

url_padre='https://books.toscrape.com/index.html'
root_url='https://books.toscrape.com/'
#Listado de expresiones xpath
links_categorias='//ul[@class="nav nav-list"]/li//ul/li/a/@href'
titulo='//article[@class="product_pod"]//h3/a/text()'
precio='//div[@class="product_price"]/p[@class="price_color"]/text()'

#Requests

r=requests.get(url_padre)
home=r.content.decode('utf-8')
parser=html.fromstring(home)
categorias_url=parser.xpath(links_categorias)
categorias_url=[root_url+x for x in categorias_url]

r=requests.get(categorias_url[1])
home=r.content.decode('utf-8')
parser=html.fromstring(home)
titulos_book=parser.xpath(titulo)
precios=parser.xpath(precio)
#print(titulos_book, precios)

#Generar funciones de scraper

def get_urls(url_padre):
    root_url='https://books.toscrape.com/'
    links_categorias='//ul[@class="nav nav-list"]/li//ul/li/a/@href'

    r=requests.get(url_padre)
    home=r.content.decode('utf-8')
    parser=html.fromstring(home)
    categorias_url=parser.xpath(links_categorias)
    categorias_url=[root_url+x for x in categorias_url]
    return categorias_url

def parser_content(url):
    contenido_dic={}
    r=requests.get(url)
    home=r.content.decode('utf-8')
    parser=html.fromstring(home)
    if r.status_code==200:
        #Obtener titulos de libro
        titulo='//article[@class="product_pod"]//h3/a/text()'
        titulos_book=parser.xpath(titulo)
        contenido_dic['Book Title']=titulos_book
        #Obtener los precios
        precio='//div[@class="product_price"]/p[@class="price_color"]/text()'
        precios=parser.xpath(precio)
        contenido_dic['Book Price']=precios
    return contenido_dic

link_entregar=get_urls(url_padre)
len(link_entregar)
data=[]
for indx,i in enumerate(link_entregar):
    #print(f'Se esta scrapeando la pag n° {indx}')
    data.append(parser_content(i))
    #print(data)


#Generar DataFrame
df=pd.DataFrame()
for j in data:
    df_uno=pd.DataFrame(j)
    df=pd.concat([df,df_uno])
print(df)