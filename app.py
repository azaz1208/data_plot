from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import pandas as pd

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        return render_template("data.html")
    elif request.method == 'POST':
        rt_content = {}
        rt_content["Your name!"] = request.form["user_name"]
        rt_content["Your choose!"] = request.form["type"]
        f = request.files["user_file"]
        rt_content["Your file is!"] = f.filename
        df = pd.read_excel(f)
        print(df)
        print(list(df.columns))
        session['data'] = df.to_dict()
        return render_template("data2.html", col=list(df.columns))
    
@app.route('/p', methods=['GET'])
def printSTH():
    df_dict = session['data']
    return df_dict

@app.route('/plot', methods=['POST'])



if __name__ == '__main__':
    app.run(debug= True)