import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)



app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://xhvmkrpm:{os.getenv("SQL_ACESS")}@castor.db.elephantsql.com/xhvmkrpm'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

class Posts(db.Model):
	__tablename__='posts'
	id = db.Column(db.Integer, primary_key=True)
	header = db.Column(db.String(20))
	subtitles = db.Column(db.String(500))
	category = db.Column(db.String(25))
	content = db.Column(db.String(1000))
	time_created = db.Column(db.String(100))
	updated = db.Column(db.Boolean, default=False)

db.create_all()


# Basic Routing Area
@app.route("/")
def home():
	posts = Posts.query.all()
	return render_template("views/index.html", posts=posts)

@app.route("/contact")
def contact():
	return render_template("views/contact.html")


@app.route("/about")
def about():
	return render_template("views/about.html")

@app.route("/post")
def post():
	posts = Posts.query.all()
	return render_template("views/post.html", posts=posts)

@app.route("/post/update/<int:posts_id>", methods=["POST", "GET"])
def post_update(posts_id):
	posts = Posts.query.get(posts_id)

	return render_template("views/update.html", posts=posts)


@app.route("/post-something")
def admin():
	return render_template("views/post-something.html")

@app.route("/privacy-policy")
def prviacy_policy():
	return render_template("views/privacy-policy.html")

@app.route("/terms-of-service")
def tos():
	return render_template("views/tos.html")

# End Routing

# Data Categorizing Routing 

@app.route("/post/category/projects", methods=["POST", "GET"])
def category_projects():
	posts = Posts.query.filter_by(category="Projects")
	

	return render_template("views/post.html", posts=posts)

@app.route("/post/category/space", methods=["POST", "GET"])
def category_space():

	posts = Posts.query.filter_by(category="Space")


	return render_template("views/post.html", posts=posts)

@app.route("/post/category/gamebuilds", methods=["POST", "GET"])
def category_gamebuilds():

	posts = Posts.query.filter_by(category="Game Builds")
	

	return render_template("views/post.html", posts=posts)

@app.route("/post/category/other", methods=["POST", "GET"])
def category_other():

	posts = Posts.query.filter_by(category="Other")

	return render_template("views/post.html", posts=posts)

#Data Handling Area
@app.route("/post/admin", methods=["POST"])
def post_admin():
	header = request.form["header"]
	subtitles = request.form["subtitles"]
	category = request.form["category"]
	content = request.form["content"]
	time_created = datetime.now()

	post_now = Posts(header=header,subtitles=subtitles,category=category,content=content,time_created=time_created.strftime("%d - %m - %Y %H: %M: %S"))
	db.session.add(post_now)
	db.session.commit()

	return redirect(url_for("post"))


# Data Deleting Area
@app.route("/post/admin/delete/<int:posts_id>")
def delete(posts_id):
	posts = Posts.query.get(posts_id)
	if not post:
		return redirect("/home")

	db.session.delete(posts)
	db.session.commit()
	return redirect("/post")

@app.route("/post/admin/update/<int:posts_id>", methods=["POST"])
def update(posts_id):
	posts = Posts.query.get(posts_id)
	if not post:
		return redirect("/post")

	posts.header = request.form["header"]
	posts.subtitles = request.form["subtitles"]
	posts.category = request.form["category"]
	posts.content = request.form["content"]
	posts.updated = True

	db.session.commit()

	return redirect(url_for("post"))

'''@app.route("/post/admin/category/data_state_change", methods=["POST", "GET"])
def state_change():
	posts = Posts.query.filter_by(Posts.category).all()

	if posts.category == "Projects":
		return redirect(url_for("category_projects"))

	elif posts.category == "Space":
		return redirect(url_for("category_space"))

	elif posts.category == "Gamebuilds":
		return redirect(url_for("category_gamebuilds"))'''




# Error Handling 
@app.errorhandler(404)
def error404(error):
	return render_template("views/error.html"), 404


@app.errorhandler(405)
def error404(error):
	return "stp", 405

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')