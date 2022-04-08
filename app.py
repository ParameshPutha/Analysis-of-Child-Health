from flask import Flask
import pickle
from flask import render_template
from flask import request
model=pickle.load(open('model.pkl','rb'))
model1=pickle.load(open('model1.pkl','rb'))

# application
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/id' , methods = ['POST'])
def id():
    id = int(request.form['Diff_Type'])
    if id == 0:
        return render_template("Emotional.html")
    else:
        return render_template("Behavioural.html")

 # , methods = ['POST']
@app.route('/Behavioural' , methods = ['POST'])
def Behavioural():
    GoingToSchool = int(request.form['GoingToSchool'])
    age = int(request.form['age'])
    SportsDaysInWeek = int(request.form['SportsDaysInWeek'])
    ConcentraionDays = int(request.form['ConcentraionDays'])
    EnoughPlayTime = int(request.form['EnoughPlayTime'])
    RelaxSpace = int(request.form['RelaxSpace'])
    SchoolWork = int(request.form['SchoolWork'])
    InTouchWithFamily = int(request.form['InTouchWithFamily'])
    IntouchWithFriends  = int(request.form['IntouchWithFriends'])
    sleeptime = float(request.form['sleeptime'])
    output = model.predict([[GoingToSchool, age, SportsDaysInWeek, ConcentraionDays, EnoughPlayTime, RelaxSpace, SchoolWork, InTouchWithFamily, IntouchWithFriends, sleeptime]])

    if output == 1:
        output = "Child has Borderline Behavioural Difficulties"
    elif output == 2:
        output = "Child has Significant Behavioural Difficulties"
    else:
        output = "Child Behaviour is as Expected"

    print(output)
    return render_template('Behavioural.html', output = output)

@app.route('/Emotional' , methods = ['POST'])
def Emotional():
    GoingToSchool = int(request.form['GoingToSchool'])
    AnotherChildHome  = int(request.form['AnotherChildHome'])
    SportsDaysInWeek = int(request.form['SportsDaysInWeek'])
    EnoughPlayTime = int(request.form['EnoughPlayTime'])
    RelaxSpace = int(request.form['RelaxSpace'])
    SchoolWork = int(request.form['SchoolWork'])
    Health  = int(request.form['Health'])
    School = int(request.form['School'])
    ImGoodAtThings = int(request.form['ImGoodAtThings'])
    InTouchWithFamily = int(request.form['InTouchWithFamily'])
    output = model1.predict([[GoingToSchool, AnotherChildHome, SportsDaysInWeek, EnoughPlayTime, RelaxSpace, SchoolWork, Health, School, ImGoodAtThings,InTouchWithFamily]])

    if output == 1:
        output = "Child as Borderline Emotional Difficulties"
    elif output == 2:
        output = "Child has Significant Emotional Difficulties"
    else:
        output = "Child emotion is as Expected"

    print(output)
    return render_template('Emotional.html', output = output)


if __name__ == "__main__":
    app.run(debug=True)
