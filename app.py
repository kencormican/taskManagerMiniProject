# Import libraries
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = app = Flask(__name__)

# Create environmental variables
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


# Create intance of PyMongo
mongo = PyMongo(app)


# Create get_task() function & route decorator to display tasks
@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())


# Create add_task() function with a route decorator
@app.route("/add_task")
def add_task():
    return render_template("addtask.html",
                           categories=mongo.db.categories.find())


# Create insert_task() function with a route decorator
@app.route("/insert_task", methods=["POST"])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for("get_tasks"))


# Create edit_task() function with a route decorator
@app.route("/edit_task/<task_id>")
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template("edittask.html",
                           task=the_task, categories=all_categories)


# Create update_task() function to submit changes when edited
@app.route("/update_task/<task_id>", methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)},
                 {
            'task_name': request.form.get('task_name'),
            'category_name': request.form.get('category_name'),
            'task_description': request.form.get('task_description'),
            'due_date': request.form.get('due_date'),
            'is_urgent': request.form.get('is_urgent')
                 })

    return redirect(url_for('get_tasks'))


# Create delete_task() function with a route decorator
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


# Create get_categories() function to display the categories
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
                           categories=mongo.db.categories.find())


# Create edit_category() function to provide a view to edit a category
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
                           category=mongo.db.categories.find_one(
                               {'_id': ObjectId(category_id)}))


# Create update_category() function to write changes to the database
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))


# Create delete_category() function with a route decorator
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


# Create add_category() function with a route decorator
@app.route("/add_category")
def add_category():
    return render_template("addcategory.html")


# Create insert_category() function with a route decorator
@app.route("/insert_category", methods=["POST"])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form.get('category_name')}
    categories.insert_one(category_doc)
    return redirect(url_for("get_categories"))

# Alternate approach to insert_category
# @app.route('/insert_category', methods=['POST'])
# def insert_category():
#     category_doc = {'category_name': request.form.get('category_name')}
#     mongo.db.categories.insert_one(category_doc)
#     return redirect(url_for('get_categories'))


# Create IP & Port location to run app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
