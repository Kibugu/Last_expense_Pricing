from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('pricing_rf.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Channel = request.form['Channel']
        benefit =int(request.form['benefit'])
        Claim_ratio =float(request.form['Claim_ratio'])
        Population=int(request.form['Population'])
        Average_age=float(request.form['Average_age'])
       #Famsize = request.form['Famsize']
        Occupation = request.form['Occupation']
        Single_multiple = request.form['Single_multiple']
        Month=int(request.form['Month'])

        Channel=request.form['Channel']
        if(Channel=='bancassurance'):
            Channel=0
        elif (Channel==' Agency '):
            Channel = 1
        elif (Channel=='Brokers'):
            Channel = 2
        else:
            Channel = 3

        Single_multiple=request.form['Single_multiple']
        if(Single_multiple=='Single'):
            Single_multiple=0
        else:
            Single_multiple = 1

        Occupation = request.form['Occupation']
        if (Occupation == 'Welfare'):
            Occupation = 0
        else:
            Occupation = 1

        Famsize = request.form['Famsize']
        if(Famsize == 'Extended'):
            Famsize = 0
        else:
            Famsize = 1


        prediction = model.predict([[Channel,benefit,Population,Average_age,Claim_ratio,Occupation,Famsize,Single_multiple,Month]])
        output = round(prediction[0],2)
        if output < 0:
            return render_template('index.html',prediction_texts="Sorry you cannot generate a quote due to insufficient data")
        else:
            return render_template('index.html',prediction_text="The rate applicable for this welfare / employees is {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)