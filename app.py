from typing import final
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import sklearn

app = Flask(__name__)
model = pickle.load(open('RF.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')



def preprocess(features):
    x = features[0]
    x = x.split(',')
    x = np.array(x).reshape(1,-1)
    return x.astype(float)



@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''

    int_features = [x for x in request.form.values()]
    size = len(int_features)

    final_features = preprocess(int_features)

    prediction = model.predict(final_features)

    output = int(prediction[0])

    if output == 0:
        output = 'MALICIOUS CONNECTION ALERT. DOS ATTACK DETECTED!'
    
    if output == 1:
        output = 'The connect is SAFE.'

    if output == 2:
        output = 'MALICIOUS CONNECTION ALERT. PROBING ATTACK DETECTED!'

    if output == 3:
        output = 'MALICIOUS CONNECTION ALERT. ROOT2LOCAL ATTACK DETECTED!'

    if output == 4:
        output = 'MALICIOUS CONNECTION ALERT. USER2ROOT ATTACK DETECTED!'

    # if output == 'Succesful':
    #     output = "Passed All Checks. Your Code has NO DEFECTS!"
    
    # else:
    #     output = "DEFECTS FOUND! Please Recheck the Module."


    return render_template('index.html', prediction_text='{}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)
