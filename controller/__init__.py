from flask import Flask

app = Flask(__name__)

app = Flask('Storage Query')

from controller.queries import queriesController

app.register_blueprint(queriesController)

