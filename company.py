from flask import Flask, render_template, request, abort, Response
#from flask import jsonify
#import pandas as pd
#from flask_cors import CORS
#from werkzeug.utils import secure_filename
#import json,traceback,os.path
#from flask_ngrok import run_with_ngrok
#import sys
#import requests
#import urllib.request


app = Flask(__name__)

#run_with_ngrok(app)
#NEWS_API_KEY = "02045abef4484928879964f30d14957a"

# cross origin

#CORS(app, resources={r"*": {"origins": "*"}})



@app.route('/')
def index():

        return render_template('pages/upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('file'),encoding = "utf-8")
        df_json = json.loads(df.to_json(orient='records'))
        response = dbHandler.insertData(df_json)
        print ("response",response)
        message = response["msg"]
        return render_template('pages/upload.html', message=message)
    return render_template('pages/upload.html')
    
@app.route('/getWeather', methods=['GET', 'POST'])
def getWeather():
    city = 'Toronto'
    API_KEY = 'cc691fccc58b46484c30d4dd69ba84c2'
    print(city)
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
    response = requests.get(URL)
    print(response)
    if response.status_code == 200:
        # getting data in the json format
        data = response.json()
        print(data)
        # getting the main dict block
        main = data['main']
        # getting temperature
        temperature = main['temp']
        # getting the humidity
        humidity = main['humidity']
        # getting the pressure
        pressure = main['pressure']
        # weather report
        report = data['weather']
        print(f"{city:-^30}")
        print(f"Temperature: {temperature}")
        print(f"Humidity: {humidity}")
        print(f"Pressure: {pressure}")
        print(f"Weather Report: {report[0]['description']}")
    else:
        # showing the error message
        print("Error in the HTTP request")
    return data

    
@app.route('/displaySentiment', methods=['GET', 'POST'])
def displaySentiment():
        
        sen_wordCloud = dbHandler.getSentiment()
        print(sen_wordCloud)
        # url = "https://newsapi.org/v1/articles?source=bbc-news&apiKey="+NEWS_API_KEY

        # # call the api
        # response = requests.get(url)
        # #print("response",response)

        # # get the data in json format
        # result = response.json()
        # print("result",result)
        # # all the news articles are listed under 'articles' key
        # # we are interested in the description of each news article
        # sentences = ""
        # for news in result['articles']:
            # description = news['description']
            # sentences = sentences + " " + description
        # print("sentences",sentences)

        # # split sentences into words
        # words = word_tokenize(sentences)
        # #print("words",words)
        # # get stopwords
        # stop_words = set(stopwords.words('english'))

        # # remove stopwords from our words list and also remove any word whose length is less than 3
        # # stopwords are commonly occuring words like is, am, are, they, some, etc.
        # words = [word for word in words if word not in stop_words and len(word) > 3]

        # # now, get the words and their frequency
        # words_freq = Counter(words)

        # # JQCloud requires words in format {'text': 'sample', 'weight': '100'}
        # # so, lets convert out word_freq in the respective format
        # words_json = [{'text': word, 'weight': count} for word, count in words_freq.items()]
        #print("words_json",words_json)
        # now convert it into a string format and return it
        return json.dumps(sen_wordCloud)
        
        
@app.route('/displayPositive', methods=['GET', 'POST'])
def displayPositive():
        
        pos_wordCloud = dbHandler.getPositive()
        
        print("emo analyse")
        return json.dumps(pos_wordCloud)
        
@app.route('/displayNegative', methods=['GET', 'POST'])
def displayNegative():
        
        neg_wordCloud = dbHandler.getNegative()
        
        print("emo analyse")
        return json.dumps(neg_wordCloud)
        
@app.route('/sentimentDistribution', methods=['GET', 'POST'])
def sentimentDistribution():
        
        response = dbHandler.sentimentDistribution()
        print(response)
        return json.dumps(response)
    
@app.route('/authenticate/<authType>', methods=['POST'])
def authenticate(authType):
    try:
        if authType == "login":
            print("******")
            username = request.form['user_id']
            password = request.form['password']
            response = dbHandler.loginCheck(username,password)
        elif authType == "train":
            print("******")
            response = dbHandler.trainModel()
        elif authType == "logout":
            response={
                "status":True,
                "msg":"Logged out succesfully"
            }

    except Exception as e:
        print(e)
        response = {
            "status":False,
            "msg":"[error] occured while authenticating user"
        }
    print ("response",response)
    return jsonify(response=response)


    
    

if __name__ == '__main__':
    app.run()