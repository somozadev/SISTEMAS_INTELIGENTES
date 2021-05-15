#database at: https://we.tl/t-hHBB5Kmdgc

import sqlite3 as sq
import csv 
import math as m
from sqlite3.dbapi2 import DatabaseError
import time
import concurrent.futures

PATH = 'Practica_2/'

class DBTool():
    def __init__(self):
        self.users = [] #610 users in total
        self.movies = [] #9742 films in total
        self.ratingTable = []
        """
                     USER 1                  USER 2                  USER 3          ...        
        [ [DICT_OF_IDMOVIE_RATING],[DICT_OF_IDMOVIE_RATING],[DICT_OF_IDMOVIE_RATING]...]
        
        """
        self.con = sq.connect(PATH + 'database.db')
        self.cur = self.con.cursor()
        linksFile ='links.csv'
        moviesFile = 'movies.csv'
        ratingFile = 'ratings.csv'
        tagsFile = 'tags.csv'
        
        # self.ClearDb()
        
        if self.Exists("Links") == False:    
            self.UploadCsv(linksFile)
        if self.Exists("Movies") == False:   
            self.UploadCsv(moviesFile)
        if self.Exists("Ratings") == False:   
            self.UploadCsv(ratingFile)
        if self.Exists("Tags") == False:   
            self.UploadCsv(tagsFile)        
        
        self.GetUsers()
        self.GetMovies()
        self.GetMoviesRatings()
        
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
    
    def GetMovies(self):
        self.cur.execute("SELECT movieId FROM Movies")
        aux = self.cur.fetchall()
        for movie in aux:
            self.movies.append(movie[0])
        self.movies = sorted(list(dict.fromkeys(self.movies)))
    
    def Exists(self,table):
        self.cur.execute(f"SELECT COUNT(*) from {table}")
        aux = self.cur.fetchone()
        if int(aux[0]) > 0:
            return True
        else: 
            return False
        
        
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
        
        if self.Exists("Ratings_prepared") == True:   
            return   
        
        #gets the media from each user rating
        userIdCounter = 1
        usersRatingsMid = []
        first = True
        for group in self.ratingTable: 
            userMid = 0
            for dictio in group:
                film, rating = list(dictio.values())[0]
                userMid += rating
            if first == True:
                input((userMid, userMid/len(group)))
                first = False
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
                
        q = """INSERT INTO Ratings_prepared (userId,movieId,ratingmid) VALUES (?,?,?)"""
        self.cur.executemany(q,sqltuple)
        self.con.commit()
    #calcula la raiz de la suma cuadrada de los elementos dados
    def GetBottomSqrt(self, filmWithRating):
            square_filmWithRating = [rating**2 for rating in filmWithRating]
            filmSqr_searched = m.sqrt(sum(square_filmWithRating))
            return filmSqr_searched
    
    #la sqrt esta perfecta, falta la suma de arriba. para ello hay que recoger una tabla de todos los usuarios y los ratings que hayan o no dado para las 2 peliculas de la query...
    def Sim(self, idSearch, filmAskedSim):
        
        start = time.perf_counter()
        print(f"Calculating Similitud for {idSearch}, please wait...")
        con = sq.connect(PATH + 'database.db')
        cur = con.cursor()
        cur.execute(f"SELECT ratingmid FROM Ratings_prepared WHERE movieId == {idSearch};")
        aux = cur.fetchall()
        filmWithRating = [l[0] for l in aux]
        # print("Films: ",filmWithRating)
        
        # print("filmLen_searched: ", len(filmWithRating))
        filmSqr_searched = self.GetBottomSqrt(filmWithRating)
        # print("filmSqr_searched: ", filmSqr_searched) #sqrt1
        
        for movie in self.movies:
            if movie != self.movies[self.movies.index(idSearch)]:
                filmNextId = movie
                cur.execute(f"SELECT ratingmid FROM Ratings_prepared WHERE movieId == {filmNextId};")
                aux = cur.fetchall()
                filmNeighbour = [l[0] for l in aux]        

                filmSqr_neighbour = self.GetBottomSqrt(filmNeighbour)
                bottomCos = filmSqr_searched * filmSqr_neighbour

                #Coge las 2 querys de las 2 movieId con sus usrs ratings
                cur.execute(f"SELECT userId, ratingmid FROM Ratings_prepared WHERE (movieId == {idSearch}) ORDER BY userId ASC;")
                aux1 = cur.fetchall()
                m1 = [l for l in aux1]
                cur.execute(f"SELECT userId, ratingmid FROM Ratings_prepared WHERE (movieId == {filmNextId}) ORDER BY userId ASC;")
                aux2 = cur.fetchall()
                m2 = [l for l in aux2]

                #all users related within both querys
                currusers = []
                for user,movie in aux1: 
                    currusers.append(user)
                for user,movie in aux1:
                    if currusers.__contains__(user) == False:
                        currusers.append(user)

                resultm = []

                for usr in currusers:
                    resultm.append((usr,None,None))
                resultm = [list(tup) for tup in resultm]

                #resultm is the result matrix of both moviesID and all of the users
                for i in resultm:
                    if resultm.index(i) < len(aux1):
                        i[1] = 0
                        for urs,rnq in aux1:    
                            if urs == i[0]: #
                                i[1] = rnq   
                    else:
                        i[1] = 0
                    if resultm.index(i) < len(aux2):   
                        i[2] = 0       
                        for urs,rnq in aux2:           
                            if urs == i[0]:
                                i[2] = rnq
                    else:
                        i[2] = 0

                topCos = sum([(rateA * rateB) for userId,rateA,rateB in resultm])
                
                if bottomCos != 0:
                    sim = topCos/bottomCos
                else:
                    sim = 0
                    
                # print("bottomCos", bottomCos)     
                # print("topCos",topCos)
                # print(f"SIM of {idSearch} and {filmNextId}",sim)
                filmAskedSim.append((filmNextId,sim))
        end = time.perf_counter()
        print(f"Similitud for {idSearch} calulated in {round(end-start,2)} (sg)")
        cur.execute(f"CREATE TABLE sim{str(idSearch)} (movieId integer, sim numeric);")
        con.commit()
        cur.executemany(f"INSERT INTO sim{str(idSearch)} (movieId, sim) VALUES (?,?);",filmAskedSim)
        con.commit()
        return filmAskedSim
    
class Predict():
    #hacer una lista con todos los usuarios
    #hacer una lista con todas las peliculas que el usuario ^ seleccionado no haya visto 
    def GetPredict(self):
        return self.predict
    
    def GetUserNotSeenMovies(self):        
        notSeen = self.database.movies.copy()
        for nots in self.userMoviesSeen:
            if self.database.movies.count(nots) > 0:
                notSeen.pop(nots)
                
        return notSeen        
                    
    def __init__(self, userId, movieId, database):
        start = time.perf_counter()
        self.predict = 0
        self.userId = userId
        self.database = database
        self.movieId = movieId
        
        #database.ratingTable[userId-1] : all ratings for current user as list of dicts of tuples
        #database.ratingTable[userId-1][0] : first dict of tuple
        #list(database.ratingTable[userId-1][0].values()) : array length1 of tuple
        #list(database.ratingTable[userId-1][0].values())[0] : tuple
        
        self.userMoviesSeen = []
        usermoviesRating = []
        for ratings in database.ratingTable[userId-1]:
            movie,rating = list(ratings.values())[0]
            self.userMoviesSeen.append(movie)
            usermoviesRating.append(rating)
        
        filmRelateds = []
        filmSims = []
        database.cur.execute(f"SELECT * FROM sim{movieId}")
        returner = database.cur.fetchall()
        for movId,sim in returner:
            filmRelateds.append(movId)
            filmSims.append(sim)
        
        topSum = 0
        botSum = 0
        for filmId in filmRelateds:
            added = False
            for userFilmSeenId in self.userMoviesSeen:
                if userFilmSeenId > filmId or added == True:
                    break
                if filmId == userFilmSeenId:
                    topSum += usermoviesRating[self.userMoviesSeen.index(userFilmSeenId)] * filmSims[filmRelateds.index(filmId)]
                    botSum += filmSims[filmRelateds.index(filmId)]
                    added = True
                    
                elif self.userMoviesSeen[-1] == userFilmSeenId:
                    topSum += 0
                    botSum += filmSims[filmRelateds.index(filmId)]
                    added = True
        self.predict = topSum/botSum
        
        database.cur.execute(f"SELECT title FROM Movies WHERE movieId == {movieId}")
        title = database.cur.fetchall()[0][0]
        print(f"User: {userId} \nMovie: {title} \nPrediction: {self.predict} ")     
        end = time.perf_counter()
        
        print(f"\n Compute time: {end-start} (sg)")
            
        
def concurrentFillup(database):       
    database.movies = database.movies[190:]
    print(len(database.movies))
    cuantity = int(len(database.movies) / 4)
    print(len(database.movies) / 4) #2388 cada uno hara un cacho de 2388 pelis
    marcos = database.movies[0:cuantity]
    luis = database.movies[cuantity:cuantity*2]
    jesus = database.movies[cuantity*2:cuantity*3]
    mati = database.movies[cuantity*3:]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for movie in marcos: 
            filmAskedSim = []
            futures.append(executor.submit(database.Sim, movie, filmAskedSim))
        for future in concurrent.futures.as_completed(futures):
            print(f"thread {future} finished")
            
    
class main():    
    database = DBTool()
    Predict(1,2,database).GetUserNotSeenMovies()