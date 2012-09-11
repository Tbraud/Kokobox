#!/usr/bin/python
import os
import mimetypes
from tools import readable_size
from flask import Flask,request,render_template,url_for,send_from_directory,session,escape
from werkzeug import secure_filename
from time import gmtime, strftime
app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTi'

@app.route("/")
def index():
  return render_template('index.html')


@app.route("/about/")
def about():
  return render_template('about.html')

@app.route("/sharefiles/",methods=['GET', 'POST'])
def listoffiles():
  flag=0
  if request.method == 'POST':
    f = request.files['file_data']
    f.save('./files/'+secure_filename(f.filename))
    print f
    flag=1
  dirlist=os.listdir("./files") 
  filelist=[]
  filesize=[]
  fileaddress=[]
  for fi in dirlist:
    filelist.append(fi+" - "+str(mimetypes.guess_type("./files/"+fi)[0]))
    filesize.append(readable_size(os.path.getsize("./files/"+fi)))
  return render_template('sharefiles.html',flag=flag,files_list=zip(filelist,filesize))

@app.route("/sharefiles/download/<name>/")
def download(name):
  return send_from_directory("./files/", name, as_attachment=True)

@app.route("/shoutbox/", methods=['GET','POST'])
def shoutbox():
  if 'usershoutbox' in session:
    user=escape(session['usershoutbox'])
  else:
    user='Anonyme'
  if request.method=='POST':
    msg=request.form['usermsg']
    user=request.form['username']
    session['usershoutbox']=user
    print msg
    ok=False
    while not ok:
      try:
        f=open('./static/log/chat','a')
        towrite=strftime("%H:%M:%S", gmtime())+" - "+user+" : "+msg+"\n"
        f.write(towrite.encode('utf-8'))
        f.close()
        ok=True
      except IOError:
        print "Error"
  return render_template('chat.html',name=user)

@app.route("/chat/")
def chat():
  ok=False
  while not ok:
    try:
      f=open('./static/log/chat','r')
      ok=True
    except IOError:
      print "Error"
  chat=[]
  for line in f:
    chat.append(line.decode('utf-8'))
  return render_template('chat2.html',chat_lines=chat[::-1])



@app.route("/food/",methods=['GET','POST'])
def food():
  initpoll()
  fi=None
  fii=None
  ok=False
  while not ok:
    try:
      fii=open('./static/log/'+strftime("%y%m%d", gmtime())+"-config",'r')
      ok=True
    except IOError:
      print 'error'


  state=0
  for line in fii:
    if 'state' in line:
      state=int(line.split()[1])
  fii.close()

  if state==0:
    fi=open('./static/log/'+strftime("%y%m%d", gmtime())+"-choices",'r')
    choices=[]
    for line in fi:
      choices.append(line.split())
    fi.close()

    flag_vote=0
    if 'userfood' in session:
      flag_vote=1
      print "lol" 


    if request.method=='POST':
      choice=request.form['food']
      user=request.form['username']
      session['userfood']=user
      flag_vote=1
      fi=open('./static/log/'+strftime("%y%m%d", gmtime())+'-choices','a')
      fi.write(user+" "+choice+"\n")
      fi.close()
      choices.append((user,choice))
 
    return render_template('food.html',vote=flag_vote,choices_list=choices,poll_state=state)

  elif state==1:
    fi=open('./static/log/'+strftime("%y%m%d", gmtime())+"-order",'r')
    orders=[]
    for line in fi:
      print line
      orders.append((line.split()[0],line.split(" ",1)[1]))
    fi.close()

    if request.method=='POST':
      user=request.form['username']
      order=request.form['order']
      print order
      order.replace('\n', ' ')
      fi=open('./static/log/'+strftime("%y%m%d", gmtime())+'-order','a')
      towrite=user+" "+order+"\n"
      fi.write(towrite.encode('utf-8'))
      fi.close()
      orders.append((user,order))


    return render_template('food.html',orders_list=orders,poll_state=state)

def initpoll():
  if not os.path.isfile("./static/log/"+strftime("%y%m%d", gmtime())+"-choices"):
    ok=False
    while not ok:
      try:
        fi=open('./static/log/'+strftime("%y%m%d", gmtime())+"-choices",'w')
        fi.close()
        ok=True
      except IOError:
        print 'error'

  if not os.path.isfile("./static/log/"+strftime("%y%m%d", gmtime())+"-config"):
    ok=False
    while not ok:
      try:
        fi=open('./static/log/'+strftime("%y%m%d", gmtime())+"-config",'w')
        fi.write('state 0\n')
        fi.close()
        ok=True
      except IOError:
        print 'error'
  if not os.path.isfile("./static/log/"+strftime("%y%m%d", gmtime())+"-order"):
    ok=False
    while not ok:
      try:
        fi=open('./static/log/'+strftime("%y%m%d", gmtime())+"-order",'w')
        fi.close()
        ok=True
      except IOError:
        print 'error' 




if __name__ == "__main__":
    app.run(debug=True)
