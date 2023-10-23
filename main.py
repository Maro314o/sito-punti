from flask import Flask, render_template

app = Flask(__name__)

# Lista di studenti con nomi e punteggi
students = [
    {"name": "Alice", "score": 90},
    {"name": "Bob", "score": 85},
    {"name": "Charlie", "score": 78},
]

@app.route('/')
def student_list():
    return render_template('index.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
