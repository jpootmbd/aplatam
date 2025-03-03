###################
##1.-IMPORTS    ###
###################

import requests as r
import json as json
import mysql.connector
from datetime import datetime

##########################
##2.-CONEXION MYSQL    ###
##########################
conexion=mysql.connector.connect(user='root',password='',host='127.0.0.1',database='aplatam',port='3306')
cursor=conexion.cursor()


############################################
##3.-CONSUMO API E INSERCION DE DATOS    ###
############################################
#step1#
args={'q':'bitcoin','apiKey':'ff9ab8a61e0b4c718d6edf43fe2eaa4a'} #se agrega diccionario de parametros
#url='https://newsapi.org/v2/everything?q=bitcoin&apiKey=ff9ab8a61e0b4c718d6edf43fe2eaa4a'
url='https://newsapi.org/v2/everything?'
response=r.get(url,params=args) #validar la url enviada
#print(response.url)
#step2#
if response.status_code==200:
    #content=response.content
    #print(content)
    #step3#
    response_json=json.loads(response.text)
    #step4#
    cursor=conexion.cursor()
    cursor.execute('TRUNCATE TABLE noticias_temp')
    cursor.execute('TRUNCATE TABLE cat_source')
    cursor.execute('TRUNCATE TABLE cat_author')
    cursor.execute('TRUNCATE TABLE noticias')
    cursor.execute('TRUNCATE TABLE abt_noticias_resumen')
    conexion.commit()
    #step 5#
    for field_dict in response_json['articles']:
        #print(field_dict['author'])
        #print(field_dict['source']['name'])
        #print(field_dict['publishedAt'])

        author=field_dict['author']
        if author is None:
            author='Sin author'
        source_name=field_dict['source']['name']
        published_date=datetime.strptime(field_dict['publishedAt'][:10],"%Y-%m-%d")
        #print(type(published_date)) se valida el tipo de dato
        
        nuevo_registro=(author,source_name,published_date) #se crea una tupla con los parametros del query

        query='''INSERT INTO noticias_temp (author,source_name,published_date)
                   VALUES (%s,%s,%s);'''
        cursor.execute(query,nuevo_registro)

#creación catálogo de datos
#step 6#
query='''INSERT INTO cat_source (source_name) 
           SELECT DISTINCT source_name 
           FROM aplatam.noticias_temp;'''
cursor.execute(query)
#step 7#
query='''INSERT INTO cat_author (author) 
           SELECT DISTINCT author 
           FROM aplatam.noticias_temp;'''
cursor.execute(query)

#se crea la tabla nosmalizada
#step 8#
query='''INSERT INTO noticias (id_author,id_source_name,published_date)
         SELECT ca.id AS id_author
               ,cs.id AS id_source_name
               ,nt.published_date
           FROM aplatam.noticias_temp AS nt
             LEFT JOIN cat_author AS ca
                    ON nt.author=ca.author
             LEFT JOIN cat_source AS cs 
                    ON nt.source_name=cs.source_name;'''
cursor.execute(query)

#se crea tabla de analítica básica sobre los datos de noticias
#step 9#
query='''INSERT INTO abt_noticias_resumen( id_author
                                          ,id_source_name
										  ,total_news
										  ,min_published_date
										  ,max_published_date
										  ,published_date)
         SELECT n.id_author
               ,n.id_source_name
               ,COUNT(*) AS total_news
               ,MIN(published_date) AS min_published_date
               ,MAX(published_date) AS max_published_date
               ,n.published_date 
           FROM noticias AS n
           GROUP BY n.id_author
                   ,n.id_source_name
                   ,n.published_date;'''
cursor.execute(query)
#step 10#
conexion.commit() #SE CONFIRMAN LOS CAMBIOS EN LA BASE DE DATOS
conexion.close()  #SE CIERRA LA CONEXION