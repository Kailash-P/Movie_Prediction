from flask import Flask, jsonify, json, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
# CORS(app, resources={r"/": {"origins": "*"}})
CORS(app)
# print(__name__)

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

# app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app, resources={r"/predict": {"origins": "http://127.0.0.1:5000"}})
@app.route('/predict', methods=['POST'])
# @crossdomain(origin='localhost',headers=['Content- Type','Authorization'])
# @cross_origin() 
def hello_world():
    print('api called')
    print (request.is_json)
    content = request.get_json()
    df=pd.DataFrame.from_dict(content, orient='index',columns=['imdbId', 'title', 'releaseYear', 'releaseDate', 'genre', 'writers', 'actors', 'directors', 'sequel'])
    return jsonify({"probability":1})

if __name__ == '__main__':
    app.run(port=5000)
