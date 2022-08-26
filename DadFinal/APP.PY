#import regex, import zip files for extraction and unzipping, import time to grab current time
import re
import zipfile
from time import*
from datetime import datetime, date
#import files for operation on logfile, 
from results import loglinkdata
from tablebaber import tablebabmaker
from filesetup import*
from shortlogana import bb2
from htmlfilecreatetabe import MakeHtml

#import required flask modules to create webserver
from flask import *  
from flask_mail import *  
from pymongo import*

#Access the mongodb
cluster = MongoClient("mongodb+srv://root:toor@cluster0.cx5wq.mongodb.net/?retryWrites=true&w=majority")
#Createa a cluster and a collections for the logfiles
db=cluster["logs"]
collection2 = db["logs for data"]

#Create the app
app = Flask(__name__)
#Create a upload folder for the server where files will be saved too.
UPLOAD_FOLDER = r'Users\kizsa\Desktop\DADFINAL\UPLOAD_FOLDER'

filename=''
#Reload if changes occur to code
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#set key so doesnt error out
app.secret_key = "super secret key"
#Setup mail account with correct port to send logs of the processed data
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '5f91f0b600be8b'
app.config['MAIL_PASSWORD'] = '90bee1986d8bc4'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
#create SMPT mail to send logfiles
mail=Mail(app)
now=datetime.now()
current_time = now.strftime("%H:%M:%S")
today=date.today()
logtablewords=[]
body=open('htmlfile.html','r')
readbody=body.read()
        
#sfrom results import loglinkdata
msg = Message(subject = "Time: " +current_time + " "+ "Date:"+ " "+ str(today), body ="Table logfile is attached" ,sender = "admin@gmail.com", recipients = ["kizsaud@gmail.com"])  

#Main page routed, get and post methods, grabs the file name from user input, unzips to Upload folder directory and calls the myfile function to perform operations once upload is clicked
@app.route('/', methods=['GET', 'POST'])
def upload_file():
       
        file=request.form.get("fname")

        if request.method == 'POST':
            if file.endswith('zip'):
                with zipfile.ZipFile(file,'r') as zipref:
                    zipref.extractall(r'C:\Users\kizsa\Desktop\DADFINAL\UPLOAD_FOLDER')

                    return myfile(file)
            else:
                return myfile(file)              

        return render_template('mainpage.html')
#create a url with file name as endpoint
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)
       
    
@app.route('/uploads/<name>')

def myfile(name):
    
    
    jobname=name.strip('.txt')
    if name.endswith('zip'):
        name=r'C:\Users\kizsa\Desktop\DADFINAL\UPLOAD_FOLDER\TaskLog.Task-1'
    with open(name,'r') as log:
        f=log.read()
    versionget=open('versiongit.txt','w')
    regularlog=open('regularlog.txt','w')
    regularlog.write(f)
  #grab version infromation from logfile
    with open(name) as logfile:
        for line in logfile:
            if 'Switch Ports Model' in line:
                    
                    
                versionget.write(line)
                nextline=next(logfile)
                if '------ ' in nextline:
                    nextline=next(logfile)
                    
                versionget.write(nextline)
                nextline=next(logfile)
                versionget.write(nextline)
                break
        if 'Switch Ports Model' not in logfile:
            versionget.write('None')
            versionget.write('\n')
            versionget.write('NONE')   
                
        versionget.close()
    #shorten logfile to read easily    
    ShortenTextAeTestInfo='.%AETEST-6-INFO.+|.%AETEST-3-ERROR.+|%GENIE-6-INFO:.+pyATS.+|.%ASYNC_-3-ERROR.+|.%AETEST-4-WARNING.+|.%SCRIPT-3-ERROR.+|.%SCRIPT-6-INFO.+|.%aetest-5-NOTICE.+|.%autoeasy-5-NOTICE.+'
    ShortenTextAetError='.%AETEST-6-INFO.+|.%AETEST-3-ERROR..+|.%ASYNC_-3-ERROR.+'
    ShortenListOfText=re.findall(ShortenTextAeTestInfo,f)
    shortenlogpart2=']:.+'

    #write the shortened version to a file, Make t  to a method, so it auto does this
    shortlog =open ('shortenedlog.txt','w+')
    for x in range (len(ShortenListOfText)):
        shortlog.write(ShortenListOfText[x])
        shortlog.write("\n")
    shortlog.close()
    with open('shortenedlog.txt','r') as log2:
        z=log2.read()
    shortenlistoftextpart2=re.findall(shortenlogpart2,z)


    results=open('new.txt','w')

    #this file is written simply because it makes the text easier to read, we took out anything that had cisco/time/etc
    for x in range(len(shortenlistoftextpart2)):
        results.write(shortenlistoftextpart2[x])
        results.write("\n")
    results.close()
    #Call printer function to capture all failed testcases and setthem to respective variables
    printer.tableoperatons()
    #Call the tablemaker function to create the table and write it to html file so it can be viewed after the main page, pass in name of the actual job file and the version informoation grabbed from logfile
    var=tablebabmaker.tablemaker(jobname,versionget)
    #dict1=loglinkdata.loglinkdatamethod()
    outputfile=r'C:\users\kizsa\DADFINAL\templates\htmlfile.html'
    tempopen=open(r'C:\Users\kizsa\Desktop\DADFINAL\templates\htmlfile.html','w+')
    fj=open('htmlfile.html','r')
    for lines in fj:
        #print(lines)
        tempopen.write(lines)
    tempopen.close()
    fj.close()
    #button operations to create a Detailed reason button which gives a more indepth view of a error in a testcase, as well as full log display seperated by testcase
    #Also database is connected using these methods and anytime operations are run it is sent to mongodb as a log for the program as well as email with the table
    list1=loglinkdata.loglinkdatamethod()
    name=var 
    allresults=MakeHtml.bab5()
    var=json.dumps('results.txt')
  
    content=app.open_resource('htmlfile.html','r')
    with app.open_resource("htmlfile.html") as fp:  
        msg.attach("htmlfile.html", "text/html", fp.read())
        mail.send(msg)    
   
    return render_template('htmlfile.html',name=name,allresults=allresults)
#route for delte database button    
@app.route('/my-link/')
def my_link():
    collection2.delete_many({})
    flash('Database Deleted')
    sleep(5)

    return render_template('mainpage.html')




#run
if __name__ =='__main__':
    SECRET_KEY = "Your_secret_string"

    app.run(host="0.0.0.0", port=8080, threaded=True,debug=True)
