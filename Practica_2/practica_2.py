

import sqlite3 as sq
import csv 
import os

PATH = 'Practica_2/'

class DBTool():
    def __init__(self):
        self.users = []
        """
                     USER 1                  USER 2                  USER 3          ...        
        [ [DICT_OF_IDMOVIE_RATING],[DICT_OF_IDMOVIE_RATING],[DICT_OF_IDMOVIE_RATING]...]
        
        """
        self.ratingTable = []
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
        
        self.GetUsers()
        
    def ClearDb(self):
        self.cur.execute("DELETE FROM Links")
        self.con.commit()
        self.cur.execute("DELETE FROM Movies")
        self.con.commit()
        self.cur.execute("DELETE FROM Ratings")
        self.con.commit()
        self.cur.execute("DELETE FROM Tags")
        self.con.commit()
        self.cur.execute("DELETE FROM Ratings_prepared")
        self.con.commit()
        print("Database fully cleared...")
        
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
                self.cur.executemany("INSERT INTO Tags(userId, movieId, tag, timestamp) VALUES (?,?,?,?);",to_db)
        
        self.con.commit()
        
    def GetUsers(self):
        self.cur.execute("SELECT userId FROM ratings")
        aux = self.cur.fetchall()
        for user in aux:
            self.users.append(user[0])
        self.users = sorted(list(dict.fromkeys(self.users)))
    def GetMoviesRatings(self):
                
        #gets ratings from db
        self.cur.execute("SELECT userId,movieId,rating FROM ratings")
        aux = self.cur.fetchall()
        self.ratingTable = aux
        
        #gets current base matrix setup
        userIdCounter = 1
        data = {}
        currentUserData = []
        matrix = []
        for group in self.ratingTable:
            
            if group[0] == userIdCounter:
                data['movie_rating'] = group[1],group[2]
                currentUserData.append(data.copy())
                data.clear()      
                if group == self.ratingTable[len(self.ratingTable)-1]:
                    matrix.append(currentUserData.copy())
                              
            else: 
                matrix.append(currentUserData.copy())
                currentUserData.clear()
                data.clear()
                userIdCounter+=1
                data['movie_rating'] = group[1],group[2]
                currentUserData.append(data.copy())
        self.ratingTable = matrix
        
        #gets the media from each user rating
        userIdCounter = 1
        usersRatingsMid = []
        for group in self.ratingTable: 
            userMid = 0
            for dictio in group:
                film, rating = list(dictio.values())[0]
                userMid += rating
                
            usersRatingsMid.append(userMid/len(group))    
             
        
        #creates the new matrix with rating values based on the usersRatingMid (current - usersRatingMid)
        for group in self.ratingTable: 
            for dictio in group:
                film, rating = list(dictio.values())[0]
                dictio['movie_rating'] = film, rating - usersRatingsMid[self.ratingTable.index(group)]
        
        # creates a table with the new rating values based on the usersRatingsMid         
        sqltuple = []
        print("Iserting into Ratings_prepared...")
        for group in self.ratingTable: 
            for dictio in group:
                film, rating = list(dictio.values())[0]
                tup = (self.ratingTable.index(group)+1,film,rating)
                sqltuple.append(tup)
                
        q = """INSERT INTO Ratings_prepared (userId,movieId,rating) VALUES (?,?,?)"""
        self.cur.executemany(q,sqltuple)
        self.con.commit()
        
            
        
    def Sim(self, idOne,idTwo): 
        pass  
        # topratingA = [] 
        # topratingB = []
        # top = 0
        # for group in self.ratingTable: 
        #     for dictio in group:
        #         film, rating = list(dictio.values())[0]
        #         if film == idOne: 
        #             topratingA.append(rating)
        #             print("A",dictio)
        #         elif film == idTwo:
        #             topratingB.append(rating)
        #             print("B",dictio)
        # print(len(topratingA))
        # print(len(topratingB))
        # for i in len(topratingA):
        #     pass             
                    
        
        
    def Exists(self,table):
        self.cur.execute(f"SELECT COUNT(*) from {table}")
        aux = self.cur.fetchone()
        if int(aux[0]) > 0:
            return True
        else: 
            return False


class Predict():
    #hacer una lista con todos los usuarios
    #hacer una lista con todas las peliculas que el usuario ^ seleccionado no haya visto 
    def __init__(self, movieTitle):
        pass
                       
        
class main():    
    database = DBTool()
    
    database.GetMoviesRatings()
    