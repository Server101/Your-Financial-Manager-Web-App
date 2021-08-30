import requests
from flask import Flask, render_template, request, url_for
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from pymongo import MongoClient
import main_functions
import os

from wtforms import StringField, DateField, SelectField, DecimalField
#pip install Flask-PyMongo Flask-WTF wtforms nspython

#
# Developer Name: Ricardo Brown
# Class: COP 4813 Professor Gregory Reis
# Project 4
#

#Connection database to PyMongo
credentials = main_functions.read_from_file("JSON_Documents/credentials.json")
#Credentials is now a dictionary
username = credentials["username"]
password = credentials["password"]

# Secret Key



app = Flask(__name__)
#app.config['SECRET KEY'] = '25kjih652'
app.config["MONGO_URI"] = "mongodb+srv://{0}:{1}@learningmongodb."\
"40ohx.mongodb.net/sample_airbnb?retryWrites=true&w=majority".format(username, password)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


mongo = PyMongo(app)

#Testing connection
#client = MongoClient(app.config)
#print(client.test)

# Functions
class Expenses(FlaskForm):
    description = StringField("description")
    category = SelectField("category", choices=[('Daily_Expense', 'Daily Expense'), ('Asset', 'Asset'), ('Urgent', 'Urgent'),
                                  ('Important', 'Important'),
                                  ('Urgent & Important', 'Urgent & Important'),('Expenditures', 'Expenditures')])
    cost = StringField("cost")
    currency = SelectField("currency", choices=[('USD', 'USD'),('EUR', 'EUR'), ('CAD', 'CAD'), ('PLN', 'PLN')])
    date = DateField("date")

    pass



def get_total_expenses(category):
    #Query to retrieve a category

   # for i in category:
       # print("Total Categories {0}.".format(i["category"]))
     #   print("Course {0} has {1} students enrolled.".format(i["category"], i["category"]))
    return

@app.route('/')
def index():

    my_expenses = mongo.db.expense.find()
    total_cost = 0
    for i in my_expenses:
     total_cost+=float(i["cost"])
    expensesByCategory = [
       ("category", get_total_expenses("category")),
    ]
    return render_template("index.html", expenses=total_cost, expensesByCategory=expensesByCategory)



#Add the currency converter here
def currency_converter(cost,currency):
    api_key_dict = main_functions.read_from_file("JSON_Documents/api_key.json")
    api_key = api_key_dict["my_key"]

    url="http://api.currencylayer.com/live?access_key=" + api_key
    response = requests.get(url).json()

    # SelectAuthor_dict = SelectAuthor
    main_functions.save_to_file(response, "JSON_Documents/currency.json")
    my_currency = main_functions.read_from_file("JSON_Documents/api_key.json")
    print(my_currency)


# Function to add values into the database
def populateDatabase(description, category, cost, currency, date):
    #try:
        #conn = MongoClient("db.expense")
        #print("Connected successfully!!!")
    #except:
        #print("Could not connect to MongoDB")

    #mycol = conn["expense"]

    dataValues = {"description": "description", "category": "category", "cost": "cost", "currency": "currency",  "date": "date" }

    my_expenses = mongo.db.expense
    db = my_expenses['db_expenses.expense']
    #print(db)
    #expenses = db.expense
    #print(expense)
    result = db.insert_one(dataValues)

    print(description, category, cost, date)
    currency_converter(cost, currency);
    return

   


@app.route("/addExpenses", methods=['GET', 'POST'])
def addExpenses():
    my_form = Expenses(request.form)
    #Creating counditions for user choice data
    if request.method == "POST":
        description = request.form['description']
        category = request.form["category"]
        cost = request.form['cost']
        currency = request.form['currency']
        date = request.form['date']
        response1 = [description, category, cost, currency, date]
        response2 = [cost, currency, date]
        populateDatabase(description, category, cost, currency, date)


        return render_template("expenseAdded.html", response1=response1, response2=response2, form=my_form)
    #else:
    #  print("Select a book to review")
    return render_template("addExpenses.html", form=my_form)

   #return render_template("addExpenses", form=Expenses)

@app.route("/expensesAdded")
def expenseAdded():


    return render_template("index.html")


app.run(debug=True)
