from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import app

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
now = datetime.now()
format = now.strftime('%Y-%m-%d')
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(200),nullable = False)
    date = db.Column(db.String(50), default = format)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title} - {self.date}"


@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        t = request.form['title']
        d = request.form['desc']
        todo = Todo(title = t, desc = d)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html', var = alltodo)

@app.route('/delete/<int:id>')
def delete(id):
    dlt = Todo.query.filter_by(id=id).first()
    db.session.delete(dlt)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)