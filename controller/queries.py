from flask import Blueprint
import ibm_db_dbi as db
from config import DB_CONNECTION_STRING

queriesController = Blueprint('queriesController', __name__, template_folder='templates')

@queriesController.route('/', methods=['GET'])
def hello():
    conn = db.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()

    sql = '''SELECT * FROM'''

    cursor.execute(sql,)
    result = cursor.fetchall()
    print result
    return "success"