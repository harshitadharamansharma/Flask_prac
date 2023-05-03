from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField  # not only a flask thing; framework agnostic form system
from wtforms.validators import DataRequired
from flask import flash


# Create a flask instance
app = Flask(__name__)
app.config['SECRET_KEY']="MY SECRET KEY THAT NO ONE IS SUPPOSED TO KNOW"

#Create a form class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# BooleanField
# DataFields
# DateTimeField
# RadioField
# TextAreaField


## Validators
# DataRequired
# IPAdress
# flask-WTF docs



# Create  a route decorator
@app.route('/')

# def index():
#     return "<h1>Hello World!!</h1>"

# def index():
#     return render_template("index.html")

def index():
    nname = "haha"
    stuff = "This is <strong>Bold</strong> text."
    flash("Welcome to our Website!")
    return render_template("index.html", user_name = nname, Stuff_html = stuff)

# FILTERS
# safe:- telling the app.py that it is safe to send the html content to the targetted template page( the page int he template folder .html file)
# capitalize
# lower
# upper
# title
# trim:- remove trailing sdpaces in the end
# striptags:- stripe out the html tags from the content

# localhost:5000/user/haha
@app.route('/user/<name>')

# def user(name):
    # return "<h1> Hello {} </h1>".format(name)

# def user(name):
#     return render_template("user.html",user_name=name)


def user(name):
    First_name = name  #"MYMYName"
    stuff = "This is <strong>Bold</strong> Text"
    LList = ["haaha", "dfdfg", "sdsdf", "fklklkd"]
    pizza_list = ["mashroom", "Sweet corn", "cheeze", 67]
    return render_template("user.html", First_name=First_name, stuff = stuff, name_list=LList, Pizza_Menu = pizza_list)



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
#     index()


@app.route('/name', methods=['GET', 'POST'])
# you usually post a form and get a web page as a response
def name():
    name = None
    form = NamerForm()    # NameerForm class's obhject created by us
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = '' 
        flash("Form Submitted Successfully!")

    return render_template("name.html", name = name, form = form)

