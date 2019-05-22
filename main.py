from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import Post, User
from app import app, db

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]

        if len(username) < 3 or len(username) > 20:
            flash("Your username must be 3-20 characters long.", "username_error")
            return redirect("/signup")
        if len(password) < 3 or len(password) > 20:
            flash("Your password must be 3-20 characters long.", "password_error")
            return redirect("/signup")
        if password != verify:
            flash("Passwords do not match.", "verify_error")
            return redirect("/signup")

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session["username"] = username
            return redirect('/newpost')
        else:
            flash("User already exists, sign in to access your account.")
            return redirect("/login")
            
    return render_template("signup.html", title="Blogz")    
        


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'password_error')
        
    return render_template("login.html", title="Blogz")

@app.route("/")
def index():
    users = User.query.all()
    return render_template("home.html", users=users)

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/login")

@app.route("/blogs", methods=["GET", "POST"])
def blog():

    blog_post = request.args.get("id")
    user_param = request.args.get("user")
    
    if user_param is not None:
        blog_owner = User.query.filter_by(username=user_param).first()
        blogs = blog_owner.posts
        return render_template("blogs.html", title="Blogz", blogs=blogs, name="My Blogs")
        

    if blog_post is not None:
        blog = Post.query.filter_by(id=blog_post).first()
        return render_template("blog_page.html", title="Blogz", blog=blog)
    
    blogs = Post.query.all()
    return render_template("blogs.html", title="Blogz", blogs=blogs, name="Blog Feed")
        

@app.route("/newpost", methods=["GET", "POST"])
def new_post():
    blog_owner = User.query.filter_by(username=session['username']).first()
    if request.method == 'POST':
        blog_title = request.form["title"]
        blog_body = request.form["body"]
        
        if blog_body and not blog_title:
            flash("Please make sure you enter a title for your blog post.", "title_error")
            return render_template("new_post.html", title="Blogz", blog_body=blog_body)
        if blog_title and not blog_body:
            flash("Please make sure you enter a body for your blog post.", "body_error")
            return render_template("new_post.html", title="Blogz", blog_title=blog_title)

        if not blog_title or not blog_body:
            flash("Please make sure you enter a title for your blog post.", "title_error")
            flash("Please make sure you enter a body for your blog post.", "body_error")
            return render_template("new_post.html", title="Blogz")

        new_post = Post(blog_title, blog_body, blog_owner)
        db.session.add(new_post)
        db.session.commit()
        post_id = new_post.id
   
        return redirect("/blogs?" + "id=" + str(post_id))

    blogs = Post.query.all()
    return render_template('new_post.html', title="Blogz")
    

if __name__ == "__main__":
    app.run()