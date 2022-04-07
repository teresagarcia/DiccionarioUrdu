from flask import Flask, render_template,request,redirect,url_for
from bson import ObjectId
from pymongo import MongoClient
import os
from datetime import datetime

app = Flask(__name__)   

title = "Prueba Inicial Diccionario Urdu"
heading = "Intentando crear mi Diccionario de Urdu"

client = MongoClient("mongodb://127.0.0.1:27017") #host uri  
db = client.urdudic #Select the database  
words = db.words #Select the collection name 

def redirect_url():    
    return request.args.get('next') or \    
           request.referrer or \    
           url_for('index')    
  
@app.route("/list")    
def lists ():    
    #Display the all words    
    words_l = words.find()    
    a1="active"    
    return render_template('index.html',a1=a1,words=words_l,t=title,h=heading)    
  
@app.route("/")    
@app.route("/recent")    
def words ():    
    #Display the Recent words    
    words_l = words.find().sort({_id:1}).limit(10)   
    a2 = "active"    
    return render_template('index.html',a2=a2,words=words_l,t=title,h=heading)    
  
  
@app.route("/favourites")    
def favourites ():    
    #Display the recent words    
    words_l = words.find({"fav":"yes"})   
    a3 = "active"    
    return render_template('index.html',a3=a3,words=words_l,t=title,h=heading)    
  
@app.route("/fav")    
def fav ():    
    #fav-or-not ICON    
    id=request.values.get("_id")    
    word=words.find({"_id":ObjectId(id)})    
    if(word[0]["fav"]=="yes"):    
        words.update({"_id":ObjectId(id)}, {"$set": {"fav":"no"}})    
    else:    
        words.update({"_id":ObjectId(id)}, {"$set": {"fav":"yes"}})    
    redir=redirect_url()        
    
    return redirect(redir)    
  
@app.route("/action", methods=['POST'])    
def action ():    
    #Adding a word    
    urdu_word=request.values.get("urdu_word")    
    translit=request.values.get("translit")    
    meaning=request.values.get("meaning")    
    gender=request.values.get("gender")    
    words.insert({ "urdu_word":urdu_word, "translit":translit, "meaning":meaning, "gender":gender, "date": datetime.datetime.now(), "fav":"no"})    
    return redirect("/list")    
  
@app.route("/remove")    
def remove ():    
    #Deleting a word with various references    
    key=request.values.get("_id")    
    words.remove({"_id":ObjectId(key)})    
    return redirect("/")    
  
@app.route("/update")    
def update ():    
    id=request.values.get("_id")    
    word=words.find({"_id":ObjectId(id)})    
    return render_template('update.html',words=word,h=heading,t=title)    
  
@app.route("/action3", methods=['POST'])    
def action3 ():    
    #Updating a word with various references    
    urdu_word=request.values.get("urdu_word")    
    translit=request.values.get("translit")    
    meaning=request.values.get("meaning")    
    gender=request.values.get("gender")    
    id=request.values.get("_id")    
    words.update({"_id":ObjectId(id)}, {'$set':{ "urdu_word":urdu_word, "translit":translit, "meaning":meaning, "gender":gender }})    
    return redirect("/")    
  
@app.route("/search", methods=['GET'])    
def search():    
    #Searching a word with various references    
    key=request.values.get("key")    
    refer=request.values.get("refer")    
    if(key=="_id"):    
        words_l = words.find({refer:ObjectId(key)})    
    else:    
        words_l = words.find({refer:key})    
    return render_template('searchlist.html',words=words_l,t=title,h=heading)    
    
if __name__ == "__main__":    
    app.run()   