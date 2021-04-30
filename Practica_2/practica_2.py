import PySimpleGUI as sg
import sqlite3 as sq
import csv 
import os
PATH = 'e:/CARRERA/4ºCARRERA/2º CUATRI/Sistemas Inteligentes y representacion del conocimiento/SISTEMAS_INTELIGENTES/Practica_2/'



# layout = [[sg.Text("Hello ")], [sg.Button("Ok")]]
# window = sg.Window(title="APP",layout=layout, margins=(100,50))
# while True:
#     event, values = window.read()
#     if event == "Ok" or event == sg.WINDOW_CLOSED:
#         break
# window.close()

class DBTool():
    def __init__(self):
        self.con = sq.connect(PATH + 'database.db')
        self.cur = self.con.cursor()
        linksFile ='links.csv'
        moviesFile = 'movies.csv'
        ratingFile = 'ratings.csv'
        tagsFile = 'tags.csv'
        self.ClearDb()
        self.UploadCsv(linksFile)
        self.UploadCsv(moviesFile)
        self.UploadCsv(ratingFile)
        self.UploadCsv(tagsFile)        
        self.con.commit()
        
    def ClearDb(self):
        self.cur.execute("DELETE FROM Links")
        self.cur.execute("DELETE FROM Movies")
        self.cur.execute("DELETE FROM Ratings")
        self.cur.execute("DELETE FROM Tags")
        print("Database fully cleared...")
        self.con.commit()
        
    def UploadCsv(self,csvFile):
        with open(PATH + csvFile,'r',errors="ignore") as r: 
            dr = csv.DictReader(r)
            if csvFile == 'links.csv':
                print('Iserting into links...')
                to_db = [(i['movieId'],i['imdbId'],i['tmdbId']) for i in dr]
                self.cur.executemany("INSERT INTO Links(movieId, imdbId, tmdbId) VALUES (?,?,?);",to_db)

            elif csvFile == 'movies.csv':
                print('Iserting into movies...')
                to_db = [(i['movieId'],i['title'],i['genres']) for i in dr]
                self.cur.executemany("INSERT INTO Movies(movieId, title, genres) VALUES (?,?,?);",to_db)

            elif csvFile == 'ratings.csv':
                print('Iserting into rating...')
                to_db = [(i['userId'],i['movieId'],i['rating'],i['timestamp']) for i in dr]
                self.cur.executemany("INSERT INTO Ratings(userId, movieId, rating, timestamp) VALUES (?,?,?,?);",to_db)

            elif csvFile == 'tags.csv':
                print('Iserting into tags...')
                to_db = [(i['userId'],i['movieId'],i['tag'],i['timestamp']) for i in dr]
                self.cur.executemany("INSERT OR IGNORE INTO Tags(userId, movieId, tag, timestamp) VALUES (?,?,?,?);",to_db)


    
class main():
    database = DBTool()
    
    
    