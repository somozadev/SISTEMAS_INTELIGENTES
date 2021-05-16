#database at: https://we.tl/t-BCPGggIkuw

import sqlite3 as sq
import csv 
import math as m
from sqlite3.dbapi2 import DatabaseError
import time
import concurrent.futures
import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3
from types import prepare_class


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
    
class Ranking():
    def __init__(self, userId, n, simLimit, slider, debugger, database):
        self.n = n
        self.userId = userId
        self.simLimit = simLimit
        movies = Predict(userId,1,database).GetUserNotSeenMovies()
        self.predictions = []
        self.rankTime = 0
        for movie in movies[:slider]:
            pred = Predict(userId,movie,database)
            debugger['text'] = f"{movies.index(movie)}/{slider}"
            debugger.update()
            print(f"{movies.index(movie)}/{len(movies)} with {pred.PrintTimer()}")
            self.predictions.append((movie,pred.GetPredict()))
            self.rankTime+=pred.GetValueTimer()
        self.GetRankingBySimLimit()
        self.Sort()
        
    def Sort(self):
        print("pre",self.predictions)
        self.predictions = sorted(self.predictions, key=lambda x: x[1])
        self.predictions.reverse()
        print("post",self.predictions)
    def GetRankTime(self):
        return self.rankTime
    def GetRankingByN(self):
        return self.predictions[:self.n]
    def GetRankingBySimLimit(self):
        aux = self.predictions.copy()
        for movie,ranked in aux:
            if ranked < self.simLimit * 5: #si el umbral es .75 y la nota max es 5 : ranked debe valer al menos 3.75
                self.predictions.remove((movie,ranked)) 

            
        # return self.GetRankingByN()
            
class Predict():
    def GetPredict(self):
        return self.predict
    def PrintResult(self):
        print(self.result)
        print("\n",self.timer)
    def PrintTimer(self):
        return(self.timer)
    def GetValueTimer(self):
        return self.valueTimer
    def GetUserNotSeenMovies(self):        
        notSeen = self.database.movies.copy()
        for nots in self.userMoviesSeen:
            if notSeen.count(nots) > 0:
                notSeen.remove(nots)
                    
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
        if botSum == 0:
            self.predict = 0
        else:
            self.predict = topSum/botSum
        if self.predict <= 0: 
            self.predict = 0
        elif self.predict > 5: 
            self.predict = 5
            
        
        database.cur.execute(f"SELECT title FROM Movies WHERE movieId == {movieId}")
        title = database.cur.fetchall()[0][0]
        self.result = (f"User: {userId} \nMovie: {title} \nPrediction: {self.predict} ")     
        end = time.perf_counter()
        self.valueTimer = end-start
        self.timer = (f"Compute time: {end-start} (sg)")
        # input(self.result)

class Visuals():
    
    def __init__(self, users,database):
        self.users = users
        self.database = database
                
        
        # Creating tkinter window
        self.MakeVisuals()
        
    def UpdateMovieLabel(self,event):
        self.user = int(self.id2choosen.current())+1
        p = Predict(self.user,1,self.database)        
        userSeenMovies = p.GetUserNotSeenMovies()
        self.peliculachoosen['values'] = (userSeenMovies)
        self.peliculachoosen.set(userSeenMovies[0])
        
    def RecomCallback(self):        
        print(int(self.peliculachoosen.get()))
        p = Predict((int(self.id2choosen.current()) + 1),int(self.peliculachoosen.get()),self.database).GetPredict()
        p = round(p,2)
        print("Score:" + str(p))
        self.predRes['text'] = ("Score:" + str(p))
    
    def PredictCallback(self): 
        self.treeview.delete(*self.treeview.get_children())
        print("n",self.n.get())
        print("simlim",self.simlim.get())  
        self.debugger['text'] = ">> Calculating..."
        r = Ranking((int(self.idchoosen.current()) + 1),int(self.n.get()),float(self.simlim.get()),int(self.slider.get()),self.debugger,self.database)
        tops = r.GetRankingByN()
        
        for top in tops: 
            self.treeview.insert('', 'end',values=( str(top[0]) , str(top[1]) ))



    
    def MakeVisuals(self):
        
        window = tk.Tk()
        window.title('Mi Recomendador')
        window.geometry('900x650')


        # label text for title
        ttk.Label(window, text = "RECOMENDACIONES",
                background = 'green', font = ("Times New Roman", 15, UNDERLINE)).grid(column = 0, row = 1, 
                padx =10, pady = 10)


        # label usuario
        ttk.Label(window, text = "Selecciona un usuario: ",
        		font = ("Times New Roman", 15)).grid(column = 0,
        		row = 2, padx =10, pady = 10)

        # Combobox IDusuario
        n = tk.StringVar()
        self.idchoosen = ttk.Combobox(window, width = 10, textvariable = n)


        # label items del ranking 
        ttk.Label(window, text = "Items del ranking: ",
        		font = ("Times New Roman", 15)).grid(column = 0,
        		row = 3, padx =20, pady = 10)

        # input ranking 
        self.n = ttk.Entry(window, width = 5)
        self.n.insert(-1,'5')
        self.n.grid(row = 3, column = 1)

        # label umbral de similitud 
        ttk.Label(window, text = "Umbral de similitud: ",
        		font = ("Times New Roman", 15)).grid(column = 2,
        		row = 3, padx =20, pady = 20)


        # input similitud 
        self.simlim = ttk.Entry(window, width = 5)
        self.simlim.insert(-1,'0.75')
        self.simlim.grid(row = 3, column = 3)


        # button recomendar 
        tk.Button(window, command= self.PredictCallback, text='Recomendar').grid(row=2, column=4, sticky=tk.W, pady=4)
        
        self.slider = tk.Scale(window, width= 20,length=300, from_=0, to=9510, orient=HORIZONTAL)
        self.slider.grid(row=4,column=2)
        self.debugger = ttk.Label(window, text = ">> ", font = ("Times New Roman", 15))
        self.debugger.grid(column = 0, row = 4, padx =20, pady = 10)

        
        # label ranking
        ttk.Label(window, text = "Ranking: ",
        		font = ("Times New Roman", 15)).grid(column = 2,
        		row = 5, padx =10, pady = 30)
        
        # Set the treeeview, tabla

        columns = ('#1', '#2')
        tree = ttk.Treeview(window, columns=columns, show='headings')

        tree.heading('#1', text='ID.Item')
        tree.heading('#2', text='Prediccion')

        tree.column('#1', stretch=tk.YES)
        tree.column('#2', stretch=tk.YES)

        tree.grid(row=6, column=2, sticky='nsew', padx =10, pady = 10)
        self.treeview = tree
        
        
        
        
        
        
        
        
        # label usuario2
        ttk.Label(window, text = "Selecciona un usuario: ",
        		font = ("Times New Roman", 15)).grid(column = 0,
        		row = 7, padx =10, pady = 10)

        # Combobox IDusuario2
        n = tk.StringVar()
        self.id2choosen = ttk.Combobox(window, width = 10, textvariable = n)

        # Label Selecciona Pelicula
        ttk.Label(window, text = "Selecciona una pelicula: ",
        		font = ("Times New Roman", 15)).grid(column = 0,
        		row = 8, padx =10, pady = 10)

        # Combobox Pelicula
        n = tk.StringVar()
        self.peliculachoosen = ttk.Combobox(window, width = 10, textvariable = n)
        
        # button predecir 
        tk.Button(window, text='Predecir', command= self.RecomCallback).grid(row=7, column=3)
        # label prediction
        self.predRes = ttk.Label(window, text = "Score: ",
        		font = ("Times New Roman", 15))
        self.predRes.grid(column = 2,row = 7, padx =10, pady = 10)
        
        # List ID usuarios combobox
        self.idchoosen['values'] = (self.users)
        self.idchoosen.set(self.users[0])
        self.idchoosen.grid(column = 1, row = 2)
        self.idchoosen.current()


        # List ID2 usuarios combobox
        self.id2choosen['values'] = (self.users)
        self.id2choosen.set(self.users[0])
        self.id2choosen.grid(column = 1, row = 7)
        self.id2choosen.current()
        self.id2choosen.bind('<<ComboboxSelected>>',self.UpdateMovieLabel) #(peliculachoosen,id2choosen.current())

    
        
        # List ID2 usuarios combobox
        self.peliculachoosen['values'] = ()

        self.peliculachoosen.grid(column = 1, row = 8)
        self.peliculachoosen.current()

        
        window.mainloop()



            
def checkForIssues(database):
        
    movies = database.movies
    database.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'sim%';")
    sims = database.cur.fetchall()
    currents = []
    for sim in sims: 
        currents.append(int(sim[0].strip("sim")))
    missing =list(set(movies) - set(currents))
    print(len(missing))
    print((missing))
    
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = []
    #     for movie in missing: 
    #         filmAskedSim = []
    #         futures.append(executor.submit(database.Sim, movie, filmAskedSim))
    #     for future in concurrent.futures.as_completed(futures):
    #         print(f"thread {future} finished")
    
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
    # Ranking(1,5,0.78,database).GetRankingByN()
    
    Visuals(database.users, database)

    