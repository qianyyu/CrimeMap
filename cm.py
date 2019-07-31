
#------------------------------------------------------------------------------------------------------------------------------
# Program Description:
#   This assignment aims to write a Countdown Timer. that reads in a time in seconds,
# counts down that time to zero, and then quits. The timer has the following format:
# `mm:nn` and will update in place.The application is quited when 'q' is pressed or 
# time`00:00` is reached.
#------------------------------------------------------------------------------------------------------------------------------
import folium
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv,sqlite3
import os
from datetime import timedelta
from flask import Flask 
from flask import request,render_template

global page_q2,page_q3,page_q4
page_q2 = 1
page_q3 = 1
page_q4 = 1
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=timedelta(seconds = 1)
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/index', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/q2', methods=['GET'])
def q2():
  return render_template('q2.html')

@app.route('/q2', methods=['GET','POST'])
def q2_run():
    global page_q2
    connection = sqlite3.connect('a4-sampled.db')
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    number = request.form['n']
    #  The query amis to show N-most populous neighborhoods with their population count
    query =  '''SELECT p.Neighbourhood_Name, c.Latitude, c.Longitude,p.CANADIAN_CITIZEN+p.NON_CANADIAN_CITIZEN+p.NO_RESPONSE
                FROM population p, coordinates c 
                WHERE p.Neighbourhood_Name=c.Neighbourhood_Name
                AND c.LATITUDE != 0 AND c.Longitude!=0
                AND p.CANADIAN_CITIZEN+p.NON_CANADIAN_CITIZEN+p.NO_RESPONSE != 0
                order by p.CANADIAN_CITIZEN+p.NON_CANADIAN_CITIZEN+p.NO_RESPONSE desc limit ?;'''
    number = [number]

    cursor.execute(query,number)
    rows = cursor.fetchall()
    m = folium.Map(
        location=[53.5444,-113.323], 
        zoom_start=11,
    )
    for row in rows:
        folium.Circle(
            location=[row[1], row[2]], # location
            popup= row[0]+" <br> Population: "+str(row[3]),# popup text
            radius= row[3]/10, # size of radius in meter
            color= 'crimson', # color of the radius
            fill= True, # whether to fill the map
            fill_color= 'crimson' # color to fill with
        ).add_to(m)

    # The query amis to show N-least populous neighborhoods with their population count
    query =  '''SELECT p.Neighbourhood_Name, c.Latitude, c.Longitude,p.CANADIAN_CITIZEN+p.NON_CANADIAN_CITIZEN+p.NO_RESPONSE
                from population p, coordinates c 
                WHERE p.Neighbourhood_Name=c.Neighbourhood_Name
                AND c.LATITUDE != 0 AND c.Longitude!=0
                AND p.CANADIAN_CITIZEN+p.NON_CANADIAN_CITIZEN+p.NO_RESPONSE != 0
                order by p.CANADIAN_CITIZEN+p.NON_CANADIAN_CITIZEN+p.NO_RESPONSE asc limit ?;'''
    cursor.execute(query,number)
    rows = cursor.fetchall()
    for row in rows:
        folium.Circle(
            location=[row[1], row[2]], # location
            popup= row[0]+" <br> Population: "+str(row[3]),# popup text
            radius= row[3]/10, # size of radius in meter
            color= 'crimson', # color of the radius
            fill= True, # whether to fill the map
            fill_color= 'crimson' # color to fill with
        ).add_to(m) 
    m.save('./templates/q2-output-'+str(page_q2)+'.html')
    page_q2+=1
    return render_template('q2-output-'+str(page_q2-1)+'.html')



@app.route('/q3', methods=['GET'])
def q3():
    return render_template('q3.html')
@app.route('/q3', methods=['GET','POST'])
def question3():
    global page_q3
    connection = sqlite3.connect('a4-sampled.db')
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    start_year = request.form['s_year']
    end_year = request.form['e_year']
    crime_type = request.form['crime_type']
    n = request.form['n']
    # The query aims to show (in a map) the Top-N neighborhoods and their crime count where the given 
    # crime type occurred most within the given range. 
    query =  '''SELECT cor.Neighbourhood_Name, cor.Latitude, cor.Longitude,SUM(c.Incidents_Count)
                from crime_incidents c, coordinates cor
                WHERE cor.Neighbourhood_Name=c.Neighbourhood_Name
                AND Year >= ? AND Year <= ?
                AND Crime_Type == ?
                AND cor.Latitude!=0 AND cor.Longitude != 0
                GROUP BY c.Neighbourhood_Name
                order by SUM(c.Incidents_Count) desc'''
    n = int(n)
    start_year = int(start_year)
    end_year = int(end_year)
    print(crime_type)
    data = [start_year,end_year,crime_type]
    cursor.execute(query,data)
    rows = cursor.fetchall()
    m = folium.Map(
        location=[53.5444,-113.323], 
        zoom_start=11,
    )
    index = 1
    if(n>=1):
        for row in rows:
            folium.Circle(
                location=[row[1], row[2]], # location
                popup= row[0]+" <br> Incidents_Count: "+str(row[3]),# popup text
                radius= row[3], # size of radius in meter
                color= 'crimson', # color of the radius
                fill= True, # whether to fill the map
                fill_color= 'crimson' # color to fill with
            ).add_to(m)
            if(n <= 1):
                break
            if(index >= n and previous!=row[3]):
                break
            previous = row[3]    
            index+=1
    m.save('./templates/q3-output-'+str(page_q3)+'.html')
    page_q3+=1
    return render_template('q3-output-'+str(page_q3-1)+'.html')




@app.route('/q4', methods=['GET'])
def q4():
    return render_template('q4.html')
@app.route('/q4', methods=['GET','POST'])
def question4():

    global page_q4
    connection = sqlite3.connect('a4-sampled.db')
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    start_year = request.form['s_year']
    end_year = request.form['e_year']
    n = request.form['n']
    n = int(n)
    start_year = int(start_year)
    end_year = int(end_year)
    # The query aims to show (in a map) the Top-N neighborhoods and their crime count where the given 
    # crime type occurred most within the given range. 
    query =  '''SELECT p.Neighbourhood_Name, c.Latitude, c.Longitude,CAST(SUM(cc.Incidents_Count) AS DOUBLE) /(p.CANADIAN_CITIZEN+p.NON_CANADIAN_CITIZEN+p.NO_RESPONSE) as ratio,SUM(cc.Incidents_Count), p.CANADIAN_CITIZEN+p.NON_CANADIAN_CITIZEN+p.NO_RESPONSE
                FROM population p, coordinates c,crime_incidents cc
                WHERE p.Neighbourhood_Name=c.Neighbourhood_Name
                AND cc.Neighbourhood_Name=c.Neighbourhood_Name AND p.Neighbourhood_Name=cc.Neighbourhood_Name
                AND c.LATITUDE != 0 AND c.Longitude!=0
                AND p.CANADIAN_CITIZEN+p.NON_CANADIAN_CITIZEN+p.NO_RESPONSE != 0
                AND Year >= ? AND Year <= ?
                GROUP BY c.Neighbourhood_Name
                ORDER BY ratio desc limit ?;'''
    data = [start_year,end_year,n]
    cursor.execute(query,data)
    rows = cursor.fetchall()
    m = folium.Map(
        location=[53.5444,-113.323], 
        zoom_start=11,
    )
    for row in rows:
        query = '''SELECT SUM(cc.Incidents_Count), Crime_type
                    from crime_incidents cc
                    where cc.Neighbourhood_Name = ?
                    GROUP BY Crime_type
                    order by SUM(cc.Incidents_Count) desc limit 1;'''
        data = [row[0]]
        cursor.execute(query,data)
        ans = cursor.fetchone()
        folium.Circle(
            location=[row[1], row[2]], # location
            popup= row[0]+"<br>"+ans[1]+" <br> Incidents_Ratio: "+str(row[3]),# popup text
            radius= row[3]*800, # size of radius in meter
            color= 'crimson', # color of the radius
            fill= True, # whether to fill the map
            fill_color= 'crimson' # color to fill with
        ).add_to(m)
    m.save('./templates/q4-output-'+str(page_q4)+'.html')
    page_q4+=1
    return render_template('q4-output-'+str(page_q4-1)+'.html')


if __name__ == '__main__':
    app.run()