from flask import Blueprint, render_template, request
import ibm_db_dbi as db
from config import DB_CONNECTION_STRING
from collections import OrderedDict
from datetime import datetime
import timezonefinder, pytz
from geopy.distance import geodesic

queriesController = Blueprint('queriesController', __name__, template_folder='templates')


@queriesController.route('/', methods=['GET'])
def hello():

    result = []
    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT COUNT(*) FROM QUAKES'''
        cursor.execute(sql,)
        result = cursor.fetchall()
    except:
        result.append("error try again")

    print result
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


@queriesController.route('/theory', methods=['GET'])
def theory():
    return render_template('theory.html', )


@queriesController.route('/theoryExecute', methods=['GET'])
def theoryExecute():
    stime = request.args['stime']
    etime = request.args['etime']
    stime = datetime.strptime(stime, "%H:%M:%S").time()
    etime = datetime.strptime(etime, "%H:%M:%S").time()

    result = []

    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT "n_time", "latitude", "longitude" FROM QUAKES'''
        cursor.execute(sql, )
        result = cursor.fetchall()
        conn.close()
    except:
        result.append("error try again")

    count = [0,0]

    i = 0
    for r in result[:]:
        print i
        i += 1
        tf = timezonefinder.TimezoneFinder()
        if r[1] <= -90 or r[1] >= 90:
            continue
        if r[2] <= -180 or r[2] >= 180:
            continue
        timezone_str = tf.certain_timezone_at(lat=r[1], lng=r[2])

        if timezone_str is None:
            print "Could not determine the time zone"
        else:
            timezone = pytz.timezone(timezone_str)
            local_time = ((r[0] + timezone.utcoffset(r[0])).time())
            if stime < local_time < etime:
                count[0] += 1
                continue
            count[1] += 1

    print count

    return render_template('theory.html', count=count)


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
                print "r is: ", r[0]
                if i in result_dict:
                    # result_dict[i].append(r)
                    result_dict[i] = result_dict[i] + 1
                    break
                # result_dict[i] = [r]
                result_dict[i] = 1
                break

    return render_template('clusturing.html', result_dict=result_dict, error=error)


@queriesController.route('/timed', methods=['GET'])
def timed():
    return render_template('clusturing.html', )


@queriesController.route('/timedExecute', methods=['GET'])
def timedExecute():
    # lmag = request.args['lmag']
    # hmag = request.args['hmag']
    # time = request.args['time']

    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT "mag", "time" FROM EARTHQUAKE WHERE "mag" BETWEEN ? AND ?'''
        cursor.execute(sql, )
        result = cursor.fetchall()
        conn.close()
    except:
        error = "error try again"

    return render_template('clusturing.html', error=error)

@queriesController.route('/radius', methods=['GET'])
def radius():
    return render_template('radius.html', )


@queriesController.route('/radiusExecute', methods=['GET'])
def radiusExecute():
    lat = request.args['lat']
    long = request.args['long']
    radius = int(request.args['radius'])

    first = (lat, long)
    result = []

    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT "latitude", "longitude", "place" FROM QUAKES'''
        cursor.execute(sql,)
        result = cursor.fetchall()
        conn.close()
    except:
        error = "error try again"

    count = [0]
    places = []

    for r in result:
        if r[0] > 90 or r[0] < -90:
            continue
        second = (r[0], r[1])
        distance = int(geodesic(first, second).miles)
        if distance <= radius:
            count[0] += 1
            places.append([r[2],distance])

    print count

    return render_template('radius.html', count = count, places = places)


def time_zone_basic():
    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.certain_timezone_at(lat=49.2827, lng=-123.1207)

    if timezone_str is None:
        print "Could not determine the time zone"
    else:
        timezone = pytz.timezone(timezone_str)
        date_str = "2014-05-28 22:28:15"
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        print dt
        print "The time in %s is %s" % (timezone_str, dt + timezone.utcoffset(dt))

def create_column_in_table():
    conn = db.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()
    sql = '''ALTER TABLE EARTHQUAKE
          ADD COLUMN "local_time"
          TIME'''
    cursor.execute(sql, )
    conn.commit()

def set_polarity():
    conn = db.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()
    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'ak' '''
    cursor.execute(sql, )
    result1 = cursor.fetchall()
    print result1

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'at' '''
    cursor.execute(sql, )
    result3 = cursor.fetchall()
    print result3

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'ci' '''
    cursor.execute(sql, )
    result4 = cursor.fetchall()
    print result4

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'hv' '''
    cursor.execute(sql, )
    result5 = cursor.fetchall()
    print result5

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'id' '''
    cursor.execute(sql, )
    result6 = cursor.fetchall()
    print result6

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'mb' '''
    cursor.execute(sql, )
    result7 = cursor.fetchall()
    print result7

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'nc' '''
    cursor.execute(sql, )
    result8 = cursor.fetchall()
    print result8

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'nm' '''
    cursor.execute(sql, )
    result9 = cursor.fetchall()
    print result9

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'nn' '''
    cursor.execute(sql, )
    result9 = cursor.fetchall()
    print result9

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'pr' '''
    cursor.execute(sql, )
    result9 = cursor.fetchall()
    print result9

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'pt' '''
    cursor.execute(sql, )
    result9 = cursor.fetchall()
    print result9

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'se' '''
    cursor.execute(sql, )
    result9 = cursor.fetchall()
    print result9

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'us' '''
    cursor.execute(sql, )
    result9 = cursor.fetchall()
    print result9

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'uu' '''
    cursor.execute(sql, )
    result9 = cursor.fetchall()
    print result9

    sql = '''SELECT "polarity","locationSource" FROM QUAKES WHERE "locationSource" = 'uw' '''
    cursor.execute(sql, )
    result9 = cursor.fetchall()
    print result9
