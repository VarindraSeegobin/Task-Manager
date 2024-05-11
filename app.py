from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasklist.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_description = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    def __repr__(self):
        return '<Task %r' % self.task_description

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        task = Task(task_description = task_content)
         
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue."
    else:
        tasks = Task.query.order_by(Task.id).all()
        return render_template('index.html', tasks = tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    tasktodel = Task.query.get_or_404(id)
    try:
        db.session.delete(tasktodel)
        db.session.commit()
        return redirect('/')
    except:
        return "Error deleting task."
    
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Task.query.get(id)
    if request.method == 'POST':
        task.task_description = request.form['update']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "error"
    else:
        return render_template('update.html', task=task)
if __name__ == "__main__":
    app.run(debug=True)
