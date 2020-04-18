from flask import Flask, request, make_response, jsonify
import requests

app = Flask(__name__)
## TODO: STEP 1 
APIKEY = "ce197cabec4ead4b74f8ee45264180a8" # Place your API KEY Here... 
#"8a81d247d650cb16469c4ba3ceb7d265"

# **********************
# UTIL FUNCTIONS : START
# **********************

def getjson(url):
    resp =requests.get(url)
    return resp.json()

def getWeatherInfo(location):
    API_ENDPOINT = f"http://api.openweathermap.org/data/2.5/weather?APPID={APIKEY}&q={location}"
    data = getjson(API_ENDPOINT)
     
    weatherinfo = data["weather"][0]["description"]
        
    return weatherinfo
    
def getTempInfo(location):
    API_ENDPOINT = f"http://api.openweathermap.org/data/2.5/weather?APPID={APIKEY}&q={location}"
    data = getjson(API_ENDPOINT)
    
    tempinfo = data["main"]["temp"]
    
    return tempinfo

def getWindInfo(location):
    API_ENDPOINT = f"http://api.openweathermap.org/data/2.5/weather?APPID={APIKEY}&q={location}"
    data = getjson(API_ENDPOINT)
    
    windinfo = data["wind"]["speed"]
    
    return windinfo

def getWindDir(location):
    #based on 8 point compass, where each segment is 45 degree. example: direction North is from degrees 337.5 to 22.5 (exact north is 0)
    API_ENDPOINT = f"http://api.openweathermap.org/data/2.5/weather?APPID={APIKEY}&q={location}"
    data = getjson(API_ENDPOINT)
    
    winddir = ""
    winddeg = data["wind"]["deg"]
    
    if winddeg <= 22.5 and winddeg >= 0 or winddeg >= 337.5 and winddeg <=360:
        winddir = "north"
    elif winddeg <= 67.5 and winddeg > 22.5:
        winddir = "north-east"
    elif winddeg <= 112.5 and winddeg > 67.5:
        winddir = "east"
    elif winddeg <= 157.5 and winddeg > 112.5:
        winddir = "south-east"
    elif winddeg <= 202.5 and winddeg > 157.5:
        winddir = "south"
    elif winddeg <= 247.5 and winddeg > 202.5:
        winddir = "south-west"
    elif winddeg <= 292.5 and winddeg > 247.5:
        winddir = "west"
    elif winddeg <= 337.5 and winddeg > 292.5:
        winddir = "north-west"
        
    return winddir

    
# **********************
# UTIL FUNCTIONS : END
# **********************

# *****************************
# Intent Handlers funcs : START
# *****************************


def getWeatherIntentHandler(loc):
    """
    Get location parameter from dialogflow and call the util function `getWeatherInfo` to get weather info
    """
    weather = getWeatherInfo(loc)
       
    return f"Currently in {loc.title()}, it is {weather}."

def getTempIntentHandler(loc):
    """
    Get location parameter from dialogflow and call the util function `getTempInfo` to get temperature info
    """
    temp = getTempInfo(loc)
       
    return f"The temperature in {loc.title()} is {temp} Kelvin or {temp-273.15:.{4}} degree Celsius."

def getWindIntentHandler(loc):
    """
    Get location parameter from dialogflow and call the util function `getWindInfo` and getWindDirInfo to get wind info
    """
    windspeed = getWindInfo(loc)
    winddirection = getWindDir(loc)
       
    return f"The windspeed in {loc.title()} is {windspeed} knots and is blowing in a {winddirection} direction."

# ***************************
# Intent Handlers funcs : END
# ***************************


# *****************************
# WEBHOOK MAIN ENDPOINT : START
# *****************************
@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req["queryResult"]["intent"]["displayName"]
    
    if intent_name == "GetWeatherIntent":
        loc = req["queryResult"]["parameters"]["loc"]
        resp_text = getWeatherIntentHandler(loc)
        
    elif intent_name == "GetTempIntent":
        loc = req["queryResult"]["parameters"]["loc"]
        resp_text = getTempIntentHandler(loc)
    
    elif intent_name == "GetWindIntent":
        loc = req["queryResult"]["parameters"]["loc"]
        resp_text = getWindIntentHandler(loc)    
    
    else:
        resp_text = "Unable to find a matching intent. Try again."

    #resp = {
    #    "fulfillmentText": resp_text
    #}
    
    return make_response(jsonify({'fulfillmentText': resp_text}))

# ***************************
# WEBHOOK MAIN ENDPOINT : END
# ***************************

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)