## note: this is a tutorial on how to use flask but will be used as a guide for the project
# resource:http://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972
import httplib2,base64,tempfile
import os
from controller import create_account,validate_user

from flask import Flask, render_template, json, jsonify, request, redirect, session, url_for, send_from_directory
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash, secure_filename
from apiclient import discovery
from apiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors
from apiclient.http import MediaFileUpload


SCOPES = 'https://www.googleapis.com/auth/drive' #the permissions that  I have over the drive
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'La Porra'

app = Flask(__name__)

mysql = MySQL()

app.config['UPLOAD_FOLDER'] = '../LaPorra/'
# These are the extension that are accepted
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg','PNG','JPG','JPEG'])

app.secret_key = 'why would I tell you my secret key?'


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'DianaDB'
app.config['MYSQL_DATABASE_PASSWORD'] = 'a01320622'
app.config['MYSQL_DATABASE_DB'] = 'LaPorra'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

'''
START OF GOOGLE API CODE

this lets the system get a connection with the google drive api ad make sure that the
account is correct.

'''
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('drive', 'v3', http=http)
flow = client.flow_from_clientsecrets(
    CLIENT_SECRET_FILE,
    SCOPES)

'''
END OF GOOGLE DRIVE API CODE
'''
@app.route("/")
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signUp.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    _surname = request.form['inputSurname']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _surname and _email and _password:
        fullname = _name.encode('utf-8')+' '+_surname.encode('utf-8')
        result = create_account(fullname,_email,_password)
        if result:
            return json.dumps({'message': 'User created successfully !'})
        else:
            return json.dumps({'error': str(data[0])})
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})

@app.route('/userHome')
def userHome():
    if session.get('user'):
        url = "https://drive.google.com/embeddedfolderview?id=0B2ELUBdmkmgVdTVzU1M0WXpWcGc" + "#grid"
        return render_template('userHome.html',urlDrive = url )
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    _username = request.form['inputEmail']
    _password = request.form['inputPassword']

    data = validate_user(_username) #check that the user is registered calls controller
    if data != 1 and data != -1:
        if check_password_hash(str(data[0][3]),_password):
            session['user'] = data[0][0]
            return redirect('/userHome')
        else:
            return render_template('error.html',error = 'Correo o contrasea incorrecta.')
    elif data == 1:
        return render_template('error.html',error = 'Correo o contrasea incorrecta.')

    elif data == -1:
        return render_template('error.html',error = "404: Por favor vuelva a ingresar." )

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def getType(filename):
    return filename.rsplit('.', 1)[1]

@app.route('/_upload',methods=['GET', 'POST'])
def upload():

    uploaded_files = request.files.getlist("file[]")
    filenames = []
    types = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            #Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            typeImg = getType(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            #Redirect the user to the uploaded_file route, which
            #will basicaly show on the browser the uploaded file
            folder_id = '0B2ELUBdmkmgVdTVzU1M0WXpWcGc'
            file_metadata = {
              'name' : ''+str(session['user'])+'-'+filename,
              'parents': [ folder_id ]
            }
            media = MediaFileUpload(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                    mimetype='image/'+typeImg,
                                    resumable=True)
            fileEnd = service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()

            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return render_template('errorPictures.html',error = 'El tipo de la imagen no es permitida')

    return redirect(url_for('userHome'))



if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run(debug=True)
