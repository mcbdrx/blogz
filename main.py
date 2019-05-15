from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "y3723483984hg"

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route("/blogs", methods=["GET", "POST"])
def blog():
    blogs = Post.query.all()

    blog_post = request.args.get("id")

    if blog_post is not None:
        blog = Post.query.filter_by(id=blog_post).first()
        return render_template("blog_page.html", title="Build-A-Blog", blog=blog)

    return render_template("blogs.html", title="Build-A-Blog", blogs=blogs)
        
    

@app.route("/newpost", methods=["GET", "POST"])
def index():
    
    if request.method == 'POST':
        blog_title = request.form["title"]
        blog_body = request.form["body"]

        if blog_body and not blog_title:
            flash("Please make sure you enter a title for your blog post.", "title_error")
            return render_template("index.html", title="Build-A-Blog", blog_body=blog_body)
        if blog_title and not blog_body:
            flash("Please make sure you enter a body for your blog post.", "body_error")
            return render_template("index.html", title="Build-A-Blog", blog_title=blog_title)


        if not blog_title or not blog_body:
            flash("Please make sure you enter a title for your blog post.", "title_error")
            flash("Please make sure you enter a body for your blog post.", "body_error")
            return render_template("index.html", title="Build-A-Blog")


        new_post = Post(blog_title, blog_body)
        db.session.add(new_post)
        db.session.commit()
        post_id = new_post.id

        return redirect("/blogs" + "?id=" + str(post_id))

    blogs = Post.query.all()
    return render_template('index.html', title="Build-A-Blog")
    





if __name__ == "__main__":
    app.run()