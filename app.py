from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'k57yhhZpvHaiu5xSWVMY5uxZfBYdGI20'

db = SQLAlchemy(app)

#TODO: Create Blog Database Model
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blogTitle = db.Column(db.String(100), nullable=False)
    blogContent = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime())
    
    def __init__(self, blogTitle, blogContent):
        self.blogTitle = blogTitle
        self.blogContent = blogContent
        self.created_at = datetime.datetime.now()

#TODO: Create User Message Database Model        
class UserInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime())
    
    def __init__(self, name, email, content):
        self.name = name
        self.email = email
        self.content = content
        self.posted_at = datetime.datetime.now()

@app.route('/')
def index():
    blogs = Blog.query.order_by(desc(Blog.created_at)).all()
    return render_template("index.html", blogs=blogs)

@app.route('/create', methods=['GET', 'POST'])
def createBlog():
    if request.method == 'POST':
        blogTitle = request.form.get('blogTitle')
        blogContent = request.form.get('blogContent')
        newBlog = Blog(blogTitle=blogTitle, blogContent=blogContent)
        db.session.add(newBlog)
        db.session.commit()
        return redirect('/')
    return render_template('createBlog.html')

@app.route('/<int:id>/view')
def viewBlog(id):
    blog = Blog.query.get(id)
    return render_template('viewBlog.html', blog=blog)

@app.route('/<int:id>/editBlog', methods=['GET', 'POST'])
def editBlog(id):
    editBlog = Blog.query.get(id)
    if request.method == 'POST':
        editBlog.blogTitle = request.form.get('blogTitle')
        editBlog.blogContent = request.form.get('blogContent')
        db.session.commit()
        return redirect('/')
    return render_template('editBlog.html', blog=editBlog)

@app.route('/getMessage', methods=['GET', 'POST'])
def getMessage():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        newInteraction = UserInteraction(name=name, email=email, content=message)
        db.session.add(newInteraction)
        db.session.commit()
        return redirect('/')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
