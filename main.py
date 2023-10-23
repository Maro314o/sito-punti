from flask import Flask, render_template
import json
app = Flask(__name__)
database_name='data/punti.json'
parametri=['Nome','Cognome','Email','Punti']
with open(database_name, 'r') as file:
    studenti = json.load(file)
print(studenti)





@app.route('/')
def student_list():
    return render_template("index.html", students=studenti)

if __name__ == '__main__':
    app.run()
