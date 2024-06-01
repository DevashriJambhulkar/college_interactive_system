from flask import Flask,render_template,request,session,redirect,g,url_for, sessions
import mysql.connector
from flask_mysqldb import MySQL
import os
from sqlalchemy import true
from flask_socketio import join_room, leave_room, send, SocketIO, emit
import random
from string import ascii_uppercase

import random
import string
import hashlib
app = Flask(__name__)

from werkzeug.utils import secure_filename

app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "mydatabase" 

app.config['UPLOAD_FOLDER'] = 'Forum/static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mkv', 'WEBM', 'mp3', 'MOV', 'AVCHD'}

posts = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']




socketio = SocketIO(app)

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

mysql1= MySQL(app)
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
  
@app.route('/login_register', methods=['POST', 'GET'])
def login():
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mydatabase"
    )
    mycursor=mydb.cursor()

    if request.method=='POST':
        login=request.form
        username=login['username']
        password=login['password']
        mycursor.execute("select *from user where username='"+username+"' and password='"+password+"'")
        r=mycursor.fetchall()
        count=mycursor.rowcount
        if username=="Admin" and password=="Admin123":
            return redirect('/users')
        elif count==1:
            session['logged_In']= True
            return render_template("dash.html",username=username)
        elif count>1:
            return "More tham one user"
        else:
            return render_template("login_register.html", text ="Incorrect username or password")
        
    mydb.commit()
    mycursor.close()    
    return render_template('login_register.html')

@app.route('/login_register1', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        college = request.form['college']
        choose = request.form['choose']
        password = request.form['password']

        cur = mysql1.connection.cursor()

        cur.execute("INSERT INTO user (username,email,college,choose,password) VALUES (%s ,%s, %s, %s,%s)", (username, email, college, choose, password))

        mysql1.connection.commit()

        cur.close()
        return render_template('login_register.html')
    return render_template('login_register.html')

@app.route('/changepass')
def changepass():  
    return render_template('changepass.html')

@app.route('/dash', methods=['POST', 'GET'])
def dash():
    return render_template('dash.html', posts=posts)


@app.route('/index')
def index():
    return render_template('index.html')

@socketio.on('text')
def handle_message(message):
    emit('text', message, broadcast=True)

@socketio.on('file')
def handle_file(data):
    filename = data['filename']
    file_data = data['file_data']
    emit('file', {'filename': filename, 'file_data': file_data}, broadcast=True)

@app.route('/userchat', methods=['GET','POST'])
def support():
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mydatabase"
    )
    mycursor=mydb.cursor()
    if request.method=='POST':
        login=request.form
        username=login['username']
        mycursor.execute("select *from user where username='"+username+"'")
        r=mycursor.fetchall()
        count=mycursor.rowcount
        if count==1:
            return render_template("index.html")
        elif count>1:
            return render_template("userchat.html", text ="Enter username OR Username is not found")
        else:
            return render_template("userchat.html", text ="Enter username OR Username is not found")
    mydb.commit()
    mycursor.close()  
    return render_template('userchat.html')
@app.route('/users')
def users():
    cur = mysql1.connection.cursor()
    q = "SELECT * FROM user"
    cur.execute(q)
    res = cur.fetchall()
    r = "SELECT * FROM replies"
    cur.execute(r)
    rep = cur.fetchall()
    m = "SELECT * FROM messages"
    cur.execute(m)
    msg = cur.fetchall()
    mysql1.connection.commit()
    return render_template('users.html', data=res, msg=msg, rep=rep)


@app.route('/delete')
def delete():
    user_id = request.args['id']
    q = "DELETE FROM user WHERE id="+user_id
    cur = mysql1.connection.cursor()
    cur.execute(q)
    r = "DELETE FROM replies WHERE id="+user_id
    cur = mysql1.connection.cursor()
    cur.execute(r)
    m = "DELETE FROM messages WHERE id="+user_id
    cur = mysql1.connection.cursor()
    cur.execute(m)
    mysql1.connection.commit()
    cur.close()
    return redirect('/users')

@app.route('/edit')
def edit():
    user_id = request.args['id']
    q = "SELECT * FROM user WHERE id="+user_id
    cur = mysql1.connection.cursor()
    cur.execute(q)
    res = cur.fetchone()
    mysql1.connection.commit()
    return render_template('edit.html', data =res)

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        user_id = request.form['id']
        username = request.form['username']
        email = request.form['email']
        college = request.form['college']
        choose = request.form['choose']
        password = request.form['password']

        cur = mysql1.connection.cursor()
        q = "UPDATE user SET username=%s, email=%s, college=%s, choose=%s, password=%s WHERE id="+user_id
        cur.execute(q, (username, email, college, choose, password))
        mysql1.connection.commit()
        cur.close()
        return redirect('/users')

@app.route('/chat', methods=['GET','POST'])
def chat():
    cur = mysql1.connection.cursor()
    cur.execute("SELECT * FROM replies r JOIN messages m ON r.message_id = m.id;")
    replies = cur.fetchall()
    cur.execute("SELECT * FROM messages")
    messages = cur.fetchall()
    cur.close()
    return render_template('chat.html', messages=messages, replies=replies)


@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        message = request.form['message']
        sender = request.form['sender']
        cur = mysql1.connection.cursor()
        cur.execute("INSERT INTO messages (sender, message) VALUES (%s, %s)", (sender, message))
        mysql1.connection.commit()
        cur.close()
        return redirect(url_for('chat'))
    
@app.route('/reply_message/<int:message_id>', methods=['POST'])
def reply_message(message_id):
    if request.method == 'POST':
        reply = request.form['reply']
        sender = request.form['sender']
        cur = mysql1.connection.cursor()
        cur.execute("INSERT INTO replies (message_id, sender, reply) VALUES (%s, %s, %s)", (message_id, sender, reply))
        mysql1.connection.commit()
        cur.close()
        return redirect(url_for('chat'))
        
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            caption = request.form.get('caption', '')
            location = request.form.get('location', '')
            post = {'filename': filename, 'likes': 0, 'comments': [], 'caption': caption, 'location': location}
            posts.append(post)
            return redirect(url_for('dash'))
    return render_template('upload.html')

@app.route('/like/<filename>', methods=['POST'])
def like(filename):
    for post in posts:
        if post['filename'] == filename:
            post['likes'] += 1
            break
    return redirect(url_for('dash'))

@app.route('/comment/<filename>', methods=['POST'])
def comment(filename):
    comment = request.form['comment']
    for post in posts:
        if post['filename'] == filename:
            post['comments'].append(comment)
            break
    return redirect(url_for('dash'))
    
@app.route("/chitchat", methods=["POST", "GET"])
def chitchat():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("chitchat.html", error="Please Enter A Name.", code=code, name=name)

        if join != False and not code:
            return render_template("chitchat.html", error="Please Enter A Room Code.", code=code, name=name)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("chitchat.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("chitchat.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("chitchat"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)
    
