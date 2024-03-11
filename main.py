from flask import Flask, render_template, request
from flask_mail import Mail, Message
import uuid
import sqlite3

app = Flask(__name__)
mail_username = "eligombis.yt3@gmail.com"
mail_password = "qaok iyix nfdc anfy"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password
app.config["MAIL_DEFAULT_SENDER"] = (mail_username, mail_password)
mail = Mail(app)

@app.route('/home')
@app.route('/')
def home():
  return render_template("index.html")

@app.route('/contact')
def contact():
  return render_template("contact.html")

@app.route('/about')
def about():
  return render_template("about.html")

@app.route('/email-list', methods=["GET", "POST"])
def emailList():
  if request.method == "POST":
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS verification(id TEXT, email TEXT)")
    
    verifyID = str(uuid.uuid4())
    email = request.form["emailBox"]

    cursor.execute("INSERT INTO verification(id, email) VALUES (?, ?)", (verifyID, email))
    db.commit()
    cursor.close()
    db.close()
    
    msg = Message("Hello", sender=mail_username, recipients= [str(email)])
    msg.body = "Hope the test works"
    msg.html = f'''
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Verify</title>
</head>
<body style = "font-family: Arial, Helvetica, sans-serif; background-color: rgb(52, 123, 152);">
  <header>
      <h1 style = "display: inline; margin-left: 0; font-size: 60px; margin-top: 0; color: #091535;">LTHS Programming Club</h1>
  </header>
  <center><a href = "http://127.0.0.1:5000/verify?{verifyID}"<button style = "font-size: 36px; border-color: white; background-color:#67B132;">Click Here To Verify</button></center>
</body>
</html>
'''
    mail.send(msg)
    return "Sent"
  return render_template("emailList.html")

@app.route("/verify?<id>")
def verify(id):
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()
  cursor.execute("CREATE TABLE IF NOT EXISTS emailList(email TEXT)")

  cursor.execute(f"SELECT email FROM verification WHERE id = {id}")
  email = cursor.fetchone()[0]

  cursor.execute("INSERT INTO emailList(email) VALUES (?)", (email))
  return render_template("verify.html")

if __name__ == "__main__":
    app.run()