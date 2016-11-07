from flask import Flask, render_template, redirect, request, make_response
import os
from twitter import *
app = Flask(__name__)

@app.route('/')
def hello_world():
    author = "Me"
    name = "You"
    return render_template('index.html', author=author, name=name)
    
@app.route('/login', methods = ['POST'])
def signup():
    consumerkey = request.form['consumerkey']
    consumersecret = request.form['consumersecret']
    accesstoken = request.form['accesstoken']
    tokensecret = request.form['tokensecret']
    t = Twitter(auth= OAuth(accesstoken, tokensecret,
                       consumerkey, consumersecret))
    pythonTweets = t.search.tweets(q = "#python")
     
    
    return render_template('login.html', pythonTweets = pythonTweets)
  

# Run the app.
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
