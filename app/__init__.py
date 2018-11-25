

from flask import Flask

import os

from config import app_config


#webapp = Flask(__name__)

webapp = Flask(__name__, instance_relative_config=True)
#webapp.config.from_object(app_config[config_name])
webapp.config.from_pyfile('config.py')

from app import main
from app import login
from app import user




