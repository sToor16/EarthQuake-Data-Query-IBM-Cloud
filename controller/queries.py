from flask import Blueprint, render_template, request
import ibm_db_dbi as db
from config import DB_CONNECTION_STRING
from collections import OrderedDict

queriesController = Blueprint('queriesController', __name__, template_folder='templates')

@queriesController.route('/', methods=['GET'])
def hello():
    return render_template('common.html')


@queriesController.route('/question6', methods=['GET'])
def question6():
    return render_template('question6.html', )


@queriesController.route('/question6Execute', methods=['GET'])
def question6Execute():
    lmag = request.args['lmag']
    hmag = request.args['hmag']
    result = []

    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT "mag", "time" FROM EARTHQUAKE WHERE "mag" BETWEEN ? AND ?'''
        cursor.execute(sql, (lmag, hmag))
        result = cursor.fetchall()
    except:
        result.append("error try again")

    return render_template('question6.html', result=result)


@queriesController.route('/question7', methods=['GET'])
def question7():
    return render_template('question7.html', )


@queriesController.route('/question7Execute', methods=['GET'])
def question7Execute():
    llat = request.args['llat']
    hlat = request.args['hlat']
    llong = request.args['llong']
    hlong = request.args['hlong']
    result = []

    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT "place", "mag" FROM EARTHQUAKE 
        WHERE "latitude" BETWEEN ? AND ?
        AND "longitude"     BETWEEN ? AND ?
        ORDER BY "mag" DESC
        LIMIT 5
        '''
        cursor.execute(sql, (llat, hlat, llong, hlong))
        result = cursor.fetchall()
    except:
        result.append("error try again")

    return render_template('question7.html', result=result)


@queriesController.route('/question8', methods=['GET'])
def question8():
    return render_template('question8.html', )


@queriesController.route('/question8Execute', methods=['GET'])
def question8Execute():
    lmag = request.args['lmag']
    hmag = request.args['hmag']
    ranges = []

    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT "mag" FROM EARTHQUAKE WHERE "mag" BETWEEN ? AND ?'''
        cursor.execute(sql, (lmag, hmag))
        result = cursor.fetchall()
    except:
        result.append("error try again")
    return render_template('question6.html', ranges=ranges)

    return render_template('question8.html', result=result)

@queriesController.route('/clusturing', methods=['GET'])
def clusturing():
    return render_template('clusturing.html', )


@queriesController.route('/clusturingExecute', methods=['GET'])
def clusturingExecute():
    lmag = request.args['lmag']
    hmag = request.args['hmag']
    interval = request.args['interval']

    interval = float(interval)
    interval = round(interval, 2)

    error = ""

    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT "mag", "time" FROM EARTHQUAKE WHERE "mag" BETWEEN ? AND ?'''
        cursor.execute(sql, (lmag, hmag))
        result = cursor.fetchall()
        conn.close()
    except:
        error = "error try again"

    result_dict = {}

    for r in result:
        i = 0
        while i <= hmag:
            i = i + interval
            i = round(i, 3)
            print "i is: ", i
            if r[0] < i:
                print "r is: ",r[0]
                if i in result_dict:
                    # result_dict[i].append(r)
                    result_dict[i] = result_dict[i] + 1
                    break
                # result_dict[i] = [r]
                result_dict[i] = 1
                break

    return render_template('clusturing.html', result_dict = result_dict, error = error)

@queriesController.route('/timed', methods=['GET'])
def timed():
    return render_template('clusturing.html', )


@queriesController.route('/timedExecute', methods=['GET'])
def timedExecute():
    lmag = request.args['lmag']
    hmag = request.args['hmag']
    # time = request.args['time']

    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT "mag", "time" FROM EARTHQUAKE WHERE "mag" BETWEEN ? AND ?'''
        cursor.execute(sql, (lmag, hmag))
        result = cursor.fetchall()
        conn.close()
    except:
        error = "error try again"

    return render_template('clusturing.html', error = error)
