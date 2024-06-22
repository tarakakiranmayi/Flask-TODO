from flask import Flask, render_template, url_for,jsonify, request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId
app=Flask(__name__)
#mongo url conection
app.config["MONGO_URI"] = "mongodb://localhost:27017/flaskdatabase"
#our app is connecting to mongodb

mongo = PyMongo(app)

@app.route('/',methods=['POST','GET'])

def index():
    # mongo.db.inventory.insert_one({"a":1})
    # a=mongo.db.inventory.find({})
    # for item in a:
    #     print(item['a'])
    if request.method=='POST':
        task_content=request.form['content']
        date=datetime.now()
        mongo.db.inventory.insert_one({"task":task_content,"date":date})
        return redirect('/')
    else:
        tasks=mongo.db.inventory.find({})
        
        # for item in tasks:
        #     print(item['task'])
        return render_template('index.html',tasks=tasks)


@app.route('/delete/<id>')
def delete(id):
    object_id=ObjectId(id)
    st=mongo.db.inventory.delete_one({"_id":object_id})
    
    
    if st.deleted_count==1:
        return redirect('/')
    else:
        return "there is a error while deleteing"


@app.route('/update/<id>',methods=['GET','POST'])

def update(id):
    object_id=ObjectId(id)
    task=mongo.db.inventory.find_one({"_id":object_id})
    print(task)
    if request.method=='POST':
        content1=request.form['content']
        content={}
        content['date']=datetime.now()
        content['task']=content1
        update_doc={'$set':content}
        try:
            result=mongo.db.inventory.update_one({"_id":object_id},update_doc)
            print(result)
        except Exception as e:
            return jsonify({"message": str(e)}), 500
        if result.matched_count == 1:
            return redirect('/')
        else:
            return jsonify({"message": "No data found with the given id"}), 404
    else:
        return render_template('update.html',task=task)

if __name__=='__main__':
    app.run(debug=True) 
