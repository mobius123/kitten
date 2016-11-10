from flask import Flask, render_template, redirect, request, make_response, json, session
import os
from twitter import *
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import session


mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'Kitten on rails'

app.config['MYSQL_DATABASE_USER'] = 'mobius123'
app.config['MYSQL_DATABASE_PASSWORD'] = 'las'
app.config['MYSQL_DATABASE_DB'] = 'Kitten3'
app.config['MYSQL_DATABASE_HOST'] = '0.0.0.0'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return redirect('/userHome')
    else:
        return render_template('signin.html')


@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
 
 
 
        # connect to mysql
 
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
 
 
 
 
        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                consumerkey = data [0][4]
                consumersecret = data [0][5]
                accesstoken = data [0][6]
                tokensecret = data [0][7]
                t = Twitter(auth= OAuth(accesstoken, tokensecret, consumerkey, consumersecret))
                pythonTweets = t.search.tweets(q = "#python")
                return render_template('userHome.html', pythonTweets = pythonTweets)
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
 
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()
    
@app.route('/signUp',methods=['POST'])
def signUp():
    try:
     _name = request.form['inputName']
     _email = request.form['inputEmail']
     _password = request.form['inputPassword']
     _consumerkey = request.form['inputConsumerkey']
     _consumersecret = request.form['inputConsumersecret']
     _accesstoken = request.form['inputAccesstoken']
     _tokensecret = request.form['inputTokensecret']
    
     if _name and _email and _password and _consumerkey and _consumersecret and _accesstoken and _tokensecret:
      
      conn = mysql.connect()
      cursor = conn.cursor()
      _hashed_password = generate_password_hash(_password)
      cursor.callproc('sp_createUser',(_name,_email,_hashed_password,_consumerkey,_consumersecret,_accesstoken,_tokensecret))
      data = cursor.fetchall()
      
      if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
      else:
        return json.dumps({'error':str(data[0])})
     else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()


        


# Run the app.
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
