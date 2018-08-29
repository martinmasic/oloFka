from flask import Flask

from .models import User
from .security import JWT
from .util import CustomJSONEncoder

app = Flask(__name__)
app.config.from_object('app.config')
app.json_encoder = CustomJSONEncoder

jwt = JWT(app, lambda p: User.get(User.id == p['user_id']))

from app.views import *
