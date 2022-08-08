from flask import Flask, render_template, request, abort, Response



app = Flask(__name__)





@app.route('/')
def index():

        return render_template('pages/upload.html')

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
    # if request.method == 'POST':
        # df = pd.read_csv(request.files.get('file'),encoding = "utf-8")
        # df_json = json.loads(df.to_json(orient='records'))
        # response = dbHandler.insertData(df_json)
        # print ("response",response)
        # message = response["msg"]
        # return render_template('pages/upload.html', message=message)
    # return render_template('pages/upload.html')
    
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

        
      
        

    
@app.route('/authenticate/<authType>', methods=['POST'])
def authenticate(authType):
    try:
        if authType == "login":
            print("******")
            username = request.form['user_id']
            password = request.form['password']
            response = dbHandler.loginCheck(username,password)
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