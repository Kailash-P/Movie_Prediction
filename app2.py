from flask import Flask, jsonify, json, request
from flask_cors import CORS
from sklearn import linear_model
import pandas as pd

movieMap = {1:'Disaster', 2:'Flop',3:'Below Average',4:'Average',5:'Semi Hit',6:'Hit',7:'Super Hit',8:'Blockbuster',9:'All-Time Blockbuster'}

app = Flask(__name__)
print(__name__)
CORS(app)
books = [
    {
        'name': 'Green eggs',
        'price': '1.2'
    }
]
data = {
  "data": [
    "tt2251552",
    "Challo Driver",
    "2012",
    "20-07-2012",
    "Comedy",
    "Vickrant Mahajan",
    "Vickrant Mahajan | Kainaz Motivala | Prem Chopra | Deepak Arora",
    "Vickrant Mahajan",
    "0"
  ]
}
#df=pd.DataFrame.from_dict(data, orient='index',columns=['imdbId', 'title', 'releaseYear', 'releaseDate', 'genre', 'writers', 'actors', 'directors', 'sequel'])
#df.info(verbose=True)
#print(df)
@app.route('/predict', methods=['POST'])
def hello_world():
    print('api called')
    print (request.is_json)
    content = request.get_json()
    testMovies=pd.DataFrame.from_dict(content, orient='index',columns=['imdbId', 'title', 'releaseYear', 'releaseDate', 'genre', 'writers', 'actors', 'directors', 'sequel'])
    print(testMovies.writers)
    actorsSelected = loadActors()
    directorsSelected = loadDirectors()
    movies = pd.read_csv("D:\Files\Project\Movie_Prediction\MovieDetails_train.csv")
    moviesSelected  = movies[['imdbId','title','genre','actors','directors','sequel','hitFlop']]
    movieDir = loadMovies(moviesSelected)
    movieTrainFinal = getTrainData(actorsSelected,directorsSelected,movieDir)
    movieTest = testMovies[['imdbId','title','genre','actors','directors','sequel']]
    movieTestDir = getTestMovie(movieTest)
    movieTestFinal = getTestData(actorsSelected,directorsSelected,movieTestDir)
    prediction = predictRating(movieTrainFinal,movieTestFinal)
    print(movieMap[prediction])
    return jsonify({"Prediction":movieMap[prediction],"Rating":prediction})

def loadActors():
    actors = pd.read_csv("D:\Files\Project\Movie_Prediction\BollywoodActorRanking.csv")
    actorsSelected = actors[['actorName','movieCount','normalizedMovieRank','googleHits','normalizedRating']]
    actorsSelected =actorsSelected.dropna()
    actorsSelected_obj = actorsSelected.select_dtypes(['object'])
    actorsSelected[actorsSelected_obj.columns] = actorsSelected_obj.apply(lambda x: x.str.strip())
    return actorsSelected

def loadDirectors():
    directors = pd.read_csv("D:\Files\Project\Movie_Prediction\BollywoodDirectorRanking.csv")
    directorsSelected = directors[['directorName','movieCount','normalizedMovieRank','googleHits','normalizedGoogleRank','normalizedRating']]
    directorsSelected = directorsSelected.dropna()
    directorsSelected_obj = directorsSelected.select_dtypes(['object'])
    directorsSelected[directorsSelected_obj.columns] = directorsSelected_obj.apply(lambda x: x.str.strip())
    directorsSelected = directorsSelected.rename(columns={'movieCount': 'dirmovieCount','normalizedMovieRank' :'dirnormalizedMovieRank','googleHits' :'dirgoogleHits','normalizedGoogleRank':'dirnormalizedGoogleRank','normalizedRating':'dirnormalizedRating'})
    return directorsSelected

def loadMovies(moviesSelected):
    moviesSplit = moviesSelected.actors.str.split('|').apply(pd.Series)
    moviesSplit.index = moviesSelected.set_index(['imdbId','title','genre','directors','sequel','hitFlop']).index
    newMovies = moviesSplit.stack().reset_index(['imdbId','title','genre','directors','sequel','hitFlop'])
    newMovies = newMovies.rename(columns={0: 'actor'})
    dirSplit =  newMovies.directors.str.split('|').apply(pd.Series)
    dirSplit.index = newMovies.set_index(['imdbId','title','genre','actor','sequel','hitFlop']).index
    movieDir = dirSplit.stack().reset_index(['imdbId','title','genre','actor','sequel','hitFlop'])
    movieDir = movieDir.rename(columns={0: 'director'})
    movieDir['genre'] =movieDir['genre'].str.replace(' ','')
    genre=movieDir.genre.str.get_dummies()
    movieDir[genre.columns]=genre[genre.columns]
    movieDir = movieDir.drop('genre',axis=1)
    movieDir_obj = movieDir.select_dtypes(['object'])
    movieDir[movieDir_obj.columns] =movieDir_obj.apply(lambda x: x.str.strip())
    movieDir = movieDir.dropna()
    return movieDir

def getTestMovie(moviesSelected):
    moviesSplit = moviesSelected.actors.str.split(',').apply(pd.Series)
    moviesSplit.index = moviesSelected.set_index(['imdbId','title','genre','directors','sequel']).index
    newMovies = moviesSplit.stack().reset_index(['imdbId','title','genre','directors','sequel'])
    newMovies = newMovies.rename(columns={0: 'actor'})
    dirSplit =  newMovies.directors.str.split(',').apply(pd.Series)
    dirSplit.index = newMovies.set_index(['imdbId','title','genre','actor','sequel']).index
    movieDir = dirSplit.stack().reset_index(['imdbId','title','genre','actor','sequel'])
    movieDir = movieDir.rename(columns={0: 'director'})
    movieDir['genre'] =movieDir['genre'].str.replace(' ','')
    genre=movieDir.genre.str.get_dummies()
    movieDir[genre.columns]=genre[genre.columns]
    movieDir = movieDir.drop('genre',axis=1)
    movieDir_obj = movieDir.select_dtypes(['object'])
    movieDir[movieDir_obj.columns] =movieDir_obj.apply(lambda x: x.str.strip())
    movieDir = movieDir.dropna()
    return movieDir

def getTrainData(actorsSelected,directorsSelected,movieDir):
    movieActorRatingUpdated  = pd.merge(movieDir,actorsSelected[actorsSelected.columns],left_on = 'actor',right_on = 'actorName',how = 'inner')
    movieDirRatingUpdated  = pd.merge(movieActorRatingUpdated,directorsSelected[directorsSelected.columns],left_on = 'director',right_on = 'directorName',how = 'inner')
    movieDirRatingUpdated = movieDirRatingUpdated.dropna()
    movieDirRatingUpdated = movieDirRatingUpdated.drop(movieDirRatingUpdated[['actor','actorName','director','directorName']],axis =1)
    movieFinal=movieDirRatingUpdated.groupby(['imdbId','title', 'sequel', 'hitFlop', 'Action', 'Adventure',
       'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama',
       'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
       'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War'])['movieCount',
       'normalizedMovieRank', 'googleHits', 'normalizedRating',
       'dirmovieCount', 'dirnormalizedMovieRank', 'dirgoogleHits',
       'dirnormalizedGoogleRank', 'dirnormalizedRating'].max().reset_index()
    return movieFinal

def getTestData(actorsSelected,directorsSelected,movieDir):
    movieActorRatingUpdated  = pd.merge(movieDir,actorsSelected[actorsSelected.columns],left_on = 'actor',right_on = 'actorName',how = 'inner')
    movieDirRatingUpdated  = pd.merge(movieActorRatingUpdated,directorsSelected[directorsSelected.columns],left_on = 'director',right_on = 'directorName',how = 'inner')
    movieDirRatingUpdated = movieDirRatingUpdated.dropna()
    movieDirRatingUpdated = movieDirRatingUpdated.drop(movieDirRatingUpdated[['actor','actorName','director','directorName']],axis =1)
    movieDirRatingUpdated = movieDirRatingUpdated[['imdbId', 'title', 'sequel', 'movieCount', 'normalizedMovieRank', 'googleHits', 'normalizedRating', 'dirmovieCount', 'dirnormalizedMovieRank', 'dirgoogleHits', 'dirnormalizedGoogleRank', 'dirnormalizedRating']]
    movieFinal=movieDirRatingUpdated.groupby(['imdbId','title', 'sequel'])['movieCount',
       'normalizedMovieRank', 'googleHits', 'normalizedRating',
       'dirmovieCount', 'dirnormalizedMovieRank', 'dirgoogleHits',
       'dirnormalizedGoogleRank', 'dirnormalizedRating'].max().reset_index()
    return movieFinal

def predictRating(movieTrainFinal,movieTestFinal):
    X_train = movieTrainFinal[['normalizedMovieRank','normalizedRating','dirnormalizedMovieRank','dirnormalizedRating']]
    y_train = movieTrainFinal.hitFlop
    X_test = movieTestFinal[['normalizedMovieRank','normalizedRating','dirnormalizedMovieRank','dirnormalizedRating']]
    lm = linear_model.LinearRegression()
    model = lm.fit(X_train, y_train)
    predictions = lm.predict(X_test)
    return int(round(predictions[0]))

if __name__ == '__main__':
    app.run(port=8080)
