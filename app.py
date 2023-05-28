from flask import Flask, render_template
from flask import url_for, redirect #vid20
from flask import request #Vid10
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField # not only a flask thing; framework agnostic form system
from wtforms import PasswordField, BooleanField, ValidationError  #Vid14
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo, Length #Vid14
from datetime import datetime        # vid8
from flask import flash              # for mesages
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate    # Vid11
from werkzeug.security import generate_password_hash, check_password_hash  #Vid13
from datetime import date # vid16
from wtforms.widgets import TextArea #vid17

# Create a flask instance
app = Flask(__name__)
# Secret Key!
app.config['SECRET_KEY']="MY SECRET KEY THAT NO ONE IS SUPPOSED TO KNOW"  # environmental variable vdo#5

# Add Database
#Old AQLite DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # we can change to mysql and postgtresql #change this uri to point to where,whatever the other db we want to use #vid8
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'  # we can change to mysql and postgtresql #change this uri to point to where,whatever the other db we want to use #vid9
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost/our_users'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/our_users'


#Initialize The Database
db=SQLAlchemy(app)
# db=MySQLdb(app) 
migrate = Migrate(app, db)

#vid17
# Create a Blog post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))

#Create a Posts Form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget = TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

#vid21
#delete specific post with id
@app.route("/posts/delete/<int:id>")
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()

        #Return a message
        flash("Blog Post is Deleted!!!")

        #Grab all the postsfrom the database
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts = posts)

    except:
        flash("Whoops! Something went wrong while deleting this post!")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts = posts)




# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form=PostForm()

    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        #Add post data to database
        db.session.add(post)
        db.session.commit()

        #Return a message
        flash("Blog post added successfully!!")

    # Redirect to the webpage
    return render_template("add_post.html", form=form)

# Vid18
#blog posts list page
@app.route('/posts')
def posts():
    #Grab all the posts from the db
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts = posts)

#vid19
#Individual blog post page
@app.route("/posts/<int:id>")
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post = post)

#vid20
# Edit blog post
@app.route('/posts/edit/<int:id>', methods = ['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        #Update to database
        db.session.add(post)
        db.session.commit()
        flash("Pst has been updated!")
        return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form=form)

#vid16
# Json Thing
@app.route('/date')
def get_current_date():
    favorite_pizza = {
        "John": "pepperoni",
        "Mary": "Cheese",
        "Tim": "Mushroom"
    }
    return favorite_pizza
    # return {"Date": date.today()}

# Create Model 
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Do some password stuff ! #Vid13
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create A String
    def __repr__(self): 
        return '<Name %r>' % self.name 

#Vid12 
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User {} deleted successfully!!".format(id))
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)#,id=id)
    except:
        flash("Oops, something went wrong while deleting this user. Please try again")
        return render_template("add_user.html", form=form, name=name, our_users=our_users)#,id=id)



# Create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match!') ])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash the password!!!
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash = ''

        flash("User {} Added Successfully!".format(name))
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

# Update Database Record #Vid10
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']  #slightly different method form.validate_on_submit that we used in add-user function 
        name_to_update.email = request.form['email']  
        name_to_update.favorite_color = request.form['favorite_color']  

        try:
            db.session.commit()
            flash("User {} Updated Successfully!".format(id))
            return render_template("update.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there was a problem updating... try again!")
            return render_template("update.html", form=form, name_to_update=name_to_update)

    else: # just throw up the page ; when no post method is requested; just a visit to the page
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id)

#Vid15
# Create a password form class 
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email?", validators=[DataRequired()])
    password_hash = PasswordField("What's Your Password?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a form class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# BooleanField # DateFields # DateTimeField # RadioField # TextAreaField #DecimalField #FileField # HiddenField #HiddenField #MultipleField # FieldList #FloatField #IntegerField #PasswordField #RadioField #SelectField #SelectMultipleField #SubmitField #TextAreaField #DecimalField #FileField #HiddenField #HiddenField #Multiple
## Validators # DataRequired #Email #EqualTo #InputRequired # IPAdress #Length #MacAddress #NumberRange #Optional #Regexp #URL #UUID #AnyOf #NoneOf
#  # flask-WTF documentation # flask  # original wtf documentation

# Create  a route decorator
@app.route('/')
def index():
    nname = "haha"
    stuff = "This is <strong>Bold</strong> text."
    flash("Welcome to our Website!")
    return render_template("index.html", user_name = nname, Stuff_html = stuff)
# def index():
#     return "<h1>Hello World!!</h1>"
# def index():
#     return render_template("index.html")


# FILTERS
# safe:- telling the app.py that it is safe to send the html content to the targetted template page( the page int he template folder .html file)
# capitalize
# lower
# upper
# title
# trim:- remove trailing sdpaces in the end
# striptags:- stripe out the html tags from the content

#  localhost:5000/user/haha
@app.route('/user/<name>')
def user(name):
    First_name = name  #"MYMYName"
    stuff = "This is <strong>Bold</strong> Text"
    LList = ["haaha", "dfdfg", "sdsdf", "fklklkd"]
    pizza_list = ["mashroom", "Sweet corn", "cheeze", 67]
    return render_template("user.html", First_name=First_name, stuff = stuff, name_list=LList, Pizza_Menu = pizza_list)

# def user(name):
    # return "<h1> Hello {} </h1>".format(name)
# def user(name):
#     return render_template("user.html",user_name=name)


#Create custom error Pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def internal_server(e):
    return render_template("500.html"), 500 

# if __name__ == '__main__':
#     index()  #suggested by hhhahaha XD  #no need 

# Vid15
# Create password test page
@app.route('/test_pw', methods=['GET', 'POST'])
# you usually post a form and get a web page as a response
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()    # NamerForm class's object created by us
    
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = '' 
        form.password_hash.data = '' 
        
        #Lookup User By Email Address
        pw_to_check = Users.query.filter_by(email=email).first()
        # flash("Form Submitted Successfully!")

        # check Hashed Password
        passed = check_password_hash(pw_to_check.password_hash, password) # a boolean value

    return render_template("test_pw.html", 
                           email = email, 
                           password = password,
                           pw_to_check = pw_to_check,
                           passed = passed,
                           form = form)


#Create name page
@app.route('/name', methods=['GET', 'POST'])
# you usually post a form and get a web page as a response
def name():
    name = None
    form = NamerForm()    # NamerForm class's object created by us
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = '' 
        flash("Form Submitted Successfully!")

    return render_template("name.html", 
                           name = name, 
                           form = form)

