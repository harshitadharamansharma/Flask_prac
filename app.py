from flask import Flask, render_template


# Create a flask instance
app = Flask(__name__)


# Create  a route decorator
@app.route('/')

# def index():
#     return "<h1>Hello World!!</h1>"

# def index():
#     return render_template("index.html")

def index():
    nname = "haha"
    stuff = "This is <strong>Bold</strong> text."
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
    return render_template("user.html", First_name=First_name, stuff = stuff, name_list=LList)


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