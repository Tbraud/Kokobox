import os
from flask import Flask,request,render_template,url_for,send_from_directory
from werkzeug import secure_filename
from time import gmtime, strftime
app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')


@app.route("/sharefiles/",methods=['GET', 'POST'])
def listoffiles():
  flag=0
  if request.method == 'POST':
    f = request.files['file_data']
    f.save('./files/'+secure_filename(f.filename))
    print f
    flag=1

  dirlist=os.listdir("./files") 
  filesize=[]
  fileaddress=[]
  for fi in dirlist:
    size2=""
    size=(os.path.getsize("./files/"+fi))

    if size>1000:
      if size/1000>1000:
        if size/(1000*1000)>1000:
          size2=str(size/(1000*1000*1000))+" GB"
        else:
          size2=str(size/(1000*1000))+" MB"
      else:
        size2=str(size/1000)+" KB"
    else:
      size2=str(size)+" B"
    filesize.append(size2)

  return render_template('sharefiles.html',flag=flag,files_list=zip(dirlist,filesize))

@app.route("/sharefiles/download/<name>/")
def download(name):
  return send_from_directory("./files/", name, as_attachment=True)

@app.route("/shoutbox/", methods=['GET','POST'])
def shoutbox():
  if request.method=='POST':
    msg=request.form['usermsg']
    user=request.form['username']
    print msg
    f=open('./static/log/chat','a')
    f.write(strftime("%H:%M:%S", gmtime())+" - "+user+" : "+msg+"\n")
    f.close()
  chat=[]
  return render_template('chat.html')

@app.route("/chat/")
def chat():
  f=open('./static/log/chat','r')
  chat=[]
  for line in f:
    chat.append(line)
  return render_template('chat2.html',chat_lines=chat[::-1])






if __name__ == "__main__":
    app.run(debug=True)
