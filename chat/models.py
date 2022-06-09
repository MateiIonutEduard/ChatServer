from flask import *
from flask_sqlalchemy import SQLAlchemy
from chat.utils import *
import shutil

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mihai:NAIoEObXEbvQjLH!@localhost/chat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Account(db.Model):
    __tablename__ = 'account'

    Id = db.Column(db.INTEGER(), primary_key=True)
    Username = db.Column(db.Text, nullable=False)
    Password = db.Column(db.Text, nullable=False)
    Address = db.Column(db.Text, nullable=False)
    Status = db.Column(db.Text, nullable=True)
    Profile = db.Column(db.Text, nullable=True)
    apikey = db.Column(db.Text, nullable=True)

    def __init__(self, Username, Password, Address, Status, Profile, apiKey):
        self.Username = Username
        self.Password = Password

        self.Address = Address
        self.Status = Status

        self.Profile = Profile
        self.apikey = apiKey


class Message(db.Model):
    __tablename__ = 'message'

    Id = db.Column(db.INTEGER(), primary_key=True)
    SenderId = db.Column(db.INTEGER(), nullable=False)
    post = db.Column(db.Text)
    ReceiverId = db.Column(db.ForeignKey('account.Id'), nullable=False, index=True)

    account = db.relationship('Account')


class Audio(db.Model):
    __tablename__ = 'audio'

    Id = db.Column(db.INTEGER(), primary_key=True)
    Filename = db.Column(db.Text, nullable=False)
    ContentType = db.Column(db.Text, nullable=False)
    Buffer = db.Column(db.LargeBinary, nullable=False)
    MessageId = db.Column(db.ForeignKey('message.Id'), nullable=False, index=True)

    message = db.relationship('Message')


@app.route('/api/account/profile/', methods=['GET'])
def getProfile():
    key = request.args.get('apikey')

    if key is not None:
        account = Account.query.filter(Account.apikey == key).all()
        return send_file(account.Profile, mimetype='image/*')
    else:
        return Response('NotFound', status=404)


@app.route('/api/account/', methods=['GET', 'POST'])
def updateAccount():
    if request.method == 'GET':
        name = request.args.get('name')
        key = request.args.get('apikey')

        if name is not None:
            account = Account.query.filter(Account.Username == name).all()
            if account is not None and len(account) > 0:
                return jsonify(account[0])
            else:
                return Response(response="Not Found!", status=404)
        else:
            if key is not None:
                account = Account.query.filter(Account.apikey == key).all()
                if account is not None and len(account) > 0:
                    return jsonify(account)
                else:
                    return Response(response="NotFound", status=404)
            else:
                return Response(response="Unauthorized", status=401)
    elif request.method == 'POST':
        if not 'Username' in request.form:
            address = request.form['Address']
            password = request.form['Password']

            account = Account.query.filter(Account.Address == address).all()
            hashKey = getHash(password)

            if len(account) < 1:
                return Response(response="NotFound", status=404)

            if account[0].Password == hashKey:
                apiKey = getApiKey()
                account[0].apikey = apiKey

                db.session.commit()
                return jsonify(apikey=apiKey)
            else:
                return Response(response="Unauthorized", status=401)

        else:
            username = request.form['Username']
            address = request.form['Address']
            password = request.form['Password']

            status = request.form['Status']
            profile = request.files['Profile']
            imagePath = None

            if profile.filename != '':
                imagePath = "data/{}".format(profile.filename)
                profile.save(imagePath)

            passKey = getHash(password)
            apiKey = getApiKey()

            account = Account(username, passKey, address, status, imagePath, apiKey)
            db.session.add(account)

            db.session.commit()
            return jsonify(apikey=apiKey)
