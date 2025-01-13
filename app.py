from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import plotly.graph_objects as go
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
        # print(df)
        print(list(df.columns))
        session['data'] = df.to_dict()
        return render_template("data2.html", col=list(df.columns))
    
@app.route('/p', methods=['GET'])
def printSTH():
    df_dict = session['data']
    return df_dict

@app.route('/plot', methods=['POST'])
def user_plot():
    x = request.form["X"]  # x 是Student ID
    y = request.form["Y"]  # y 是English
    df_data = pd.DataFrame.from_dict(session['data'])
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = list(df_data[x]),
            y = list(df_data[y]),
            mode = "lines+markers"
        )
    )
    fig.update_layout(
        title = f"{x} vs {y} "
    )
    fig.write_html("templates/test_plot.html") 
    return render_template("test_plot.html")
    # return jsonify({x:list(df_data[x]),y:list(df_data[y])})
    



if __name__ == '__main__':
    app.run(debug = True)