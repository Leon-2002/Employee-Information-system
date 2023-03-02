from flask import Flask, render_template, url_for,redirect, request,session, flash
import re
import psycopg2


app = Flask(__name__)
app.secret_key = '1234jsldfja;kldj;fla2'
conn = psycopg2.connect("postgresql://postgres:admin321@localhost:5432/employee_db")

@app.route("/")
@app.route("/login", methods = ['POST','GET'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        username = request.form['username']
        password = request.form['password']

        cursor =conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            flash('Logged in successfully !')
            return redirect(url_for("index"))
        else:
            msg = 'Incorrect username / password !'
            flash('Incorrect username / password !')
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username, ))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM accounts WHERE email= %s',  (email, ))
        acc_email= cursor.fetchone()
        if account:
            msg = 'Account already exists !'
            flash("Accounts exists Already")
        elif acc_email:
            msg = 'email already exists !'
            flash("email exists Already")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
                flash('Invalid email address !')
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
            flash('Username must contain only characters and numbers !')
        elif not re.match(r'[A-Za-z0-9]{8,}+', password):
            msg = 'password must contains 8 minimum characters or numbers'
            flash('password must contains 8 minimum characters or numbers')
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:

            insertQuery = "INSERT INTO accounts(username, password, email) VALUES (%s, %s, %s)"
            values = (username,password, email)
            cursor.execute(insertQuery,values)
            conn.commit()
            msg = 'You have successfully registered !'
            flash('You have successfully registered !')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/index')
def index():
   
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee_tbl ORDER by lname")
    data = cur.fetchall()

    return render_template('index.html', employee_tbl = data)


@app.route('/insert', methods = ['POST','GET'])
def insert():
   if request.method == "POST":
      lname = request.form['lname']
      fname = request.form['fname']
      email = request.form['email']
      address = request.form['address']
      number = request.form['number']
      position = request.form['position']

      cur = conn.cursor()
      insertQuery = "INSERT INTO employee_tbl(lname,fname,email,address,number,position) VALUES (%s, %s, %s, %s, %s, %s)"
      values = (lname,fname,email,address,number,position)
      cur.execute(insertQuery, values)
      print("Data Inserted Successfully.")
      conn.commit()

   return redirect(url_for('index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    cur =conn.cursor()
    cur.execute("DELETE FROM employee_tbl WHERE id=%s", (id_data,))
    conn.commit()
    return redirect(url_for('index'))   


@app.route('/update', methods = ["POST", "GET"])
def update():
   if request.method == 'POST':
      id = request.form['id']
      lname = request.form['lname']
      fname = request.form['fname']
      email = request.form['email']
      address = request.form['address']
      number = request.form['number']
      position = request.form['position']

   cur = conn.cursor()
   
   query = "UPDATE  employee_tbl SET lname = %s, fname = %s, email = %s, address = %s, number = %s, position =%s WHERE id = %s"
   val = lname,fname,email,address,number,position, id
   cur.execute(query,val)
   conn.commit()
   return redirect(url_for('index'))


if __name__ == '__main__':
   app.run(host = "127.0.0.1", port = 80, debug=True)
   