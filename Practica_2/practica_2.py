

import sqlite3 as sq
import csv 
import os

PATH = 'e:/CARRERA/4ºCARRERA/2º CUATRI/Sistemas Inteligentes y representacion del conocimiento/SISTEMAS_INTELIGENTES/Practica_2/'

class DBTool():
    def __init__(self):
        self.users = []
        self.con = sq.connect(PATH + 'database.db')
        self.cur = self.con.cursor()
        linksFile ='links.csv'
        moviesFile = 'movies.csv'
        ratingFile = 'ratings.csv'
        tagsFile = 'tags.csv'
        self.ClearDb()
        if self.Exists("Links") == False:    
            self.UploadCsv(linksFile)
        if self.Exists("Movies") == False:   
            self.UploadCsv(moviesFile)
        if self.Exists("Ratings") == False:   
            self.UploadCsv(ratingFile)
        if self.Exists("Tags") == False:   
            self.UploadCsv(tagsFile)        
        self.con.commit()
        self.GetUsers()
        
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
    def GetUsers(self):
        self.cur.execute("SELECT userId FROM ratings")
        aux = self.cur.fetchall()
        for user in aux:
            self.users.append(user[0])
        self.users = sorted(list(dict.fromkeys(self.users)))
    def Exists(self,table):
        self.cur.execute(f"SELECT COUNT(*) from {table}")
        aux = self.cur.fetchone()
        if int(aux[0]) > 0:
            return True
        else: 
            return False
        
        
class main():    
    database = DBTool()
    
    