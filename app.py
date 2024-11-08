from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

@app.route("/", methods = ['POST','GET'])
def index():
    if request.method =='POST':
        task_content = request.form['content']
        new_task = ToDo(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "Please try again. The server is not working right now."
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template("index.html", tasks = tasks)

    

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id
    
@app.route("/delete/<int:id>")
def delete(id):
    task_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There is a problem. Try again later."

@app.route("/update/<int:id>", methods = ["GET", "POST"])
def update(id):
    task = ToDo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There is an issue updating the task"
    else:
        return render_template("update.html", task = task)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug= True)