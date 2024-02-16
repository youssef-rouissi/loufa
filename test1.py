from flask import Flask,redirect,url_for,render_template
import urllib.request
import json
import os
import ssl
from flask import request
app=Flask(__name__)


@app.route("/")
def home():
    return "7anouta"

@app.route("/ind")
def index():
    return render_template("index.html",hola="xxxxx")


@app.route("/log",methods=["POST","GET"])
def login():
    if request.method == "POST":
        n1=request.form["number1"]
        n2=request.form["number2"]
        n3=request.form["number3"]
        n4=request.form["number4"]
        print(n1)
        return redirect(url_for("predict",n1=n1,n2=n2,n3=n3,n4=n4))
    else:
        return render_template("login.html")


@app.route('/ekhdem_bras_omek/<n1>/<n2>/<n3>/<n4>', methods=['POST','GET'])
def predict(n1,n2,n3,n4):
   def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
      if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
         ssl._create_default_https_context = ssl._create_unverified_context

   allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
   data =  {    
  "input_data": {
    "columns": [n1,n2,n3,n4,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22],
    "index": [0],
    "data": [
            [20000,2,2,1,24,2,2,-1,-1,-2,-2,3913,3102,689,0,0,0,0,689,0,0,0,0]
            ]
                },
  "params": {}
}

   body = str.encode(json.dumps(data))

   url = 'https://credit-endpoint-13f0abdd.eastus2.inference.ml.azure.com/score'
# Replace this with the primary/secondary key or AMLToken for the endpoint
   api_key = 'vbGeQ2jQ2PJdJsgGLOzPNIvhbHvCURWw'
   headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'credit-defaults-model-1' }

   req = urllib.request.Request(url, body, headers)

   try:
       response = urllib.request.urlopen(req)
       result = response.read()
       print(result)
       return(result)
   except urllib.error.HTTPError as error:
       print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
       print(error.info())
       print(error.read().decode("utf8", 'ignore'))
    



if __name__=="__main__":
    app.run(debug = True)