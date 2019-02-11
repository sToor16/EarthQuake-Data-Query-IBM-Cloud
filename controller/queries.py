# -- coding: utf-8 --
from flask import Blueprint, render_template, request
import ibm_db_dbi as db
from config import DB_CONNECTION_STRING
from collections import OrderedDict
from datetime import datetime
import timezonefinder, pytz
from geopy.distance import geodesic

from util_functions import decdeg2dms_latitude, decdeg2dms_longitude, dms_to_dd

queriesController = Blueprint('queriesController', __name__, template_folder='templates')


@queriesController.route('/', methods=['GET'])
def hello():
    lat = decdeg2dms_latitude(32.735687)
    long = decdeg2dms_longitude(97.1080656)
    print dms_to_dd(lat)
    print dms_to_dd(long)
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
        sql = '''SELECT "mag", "time" FROM QUAKES WHERE "mag" BETWEEN ? AND ?'''
        cursor.execute(sql, (lmag, hmag))
        result = cursor.fetchall()
        conn.close()
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
        sql = '''SELECT "place", "mag" FROM QUAKES 
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

    count = [0, 0]

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
    lmag = float(request.args['lmag'])
    hmag = float(request.args['hmag'])
    interval = request.args['interval']

    interval = float(interval)
    interval = round(interval, 2)

    error = ""
    result = []

    result_dict = OrderedDict()
    map_dict = {}
    i = lmag

    while i < hmag:
        map_dict[round(i+interval,3)] = str(i) + '--' + str(i + interval)
        i += interval
        i = round(i,3)
        # result_dict[i] = []
        result_dict[i] = 0

    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT "mag", "time" FROM QUAKES WHERE "mag" BETWEEN ? AND ?'''
        cursor.execute(sql, (lmag, hmag))
        result = cursor.fetchall()
        conn.close()
    except:
        error = "error try again"

    for r in result:
        i = lmag + interval
        while i <= hmag:
            if r[0] <= i:
                # result_dict[i].append(r)
                result_dict[i] += 1
                break
            i += interval
            i  = round(i,3)

    return render_template('clusturing.html', result_dict = result_dict, map_dict = map_dict)


@queriesController.route('/timed', methods=['GET'])
def timed():
    return render_template('timed.html', )


@queriesController.route('/timedExecute', methods=['GET'])
def timedExecute():
    sdate = request.args['sdate']
    edate = request.args['edate']
    stime = request.args['stime']
    etime = request.args['etime']

    stime = datetime.strptime(sdate + stime, "%Y-%m-%d%H:%M:%S")
    etime = datetime.strptime(edate + etime, "%Y-%m-%d%H:%M:%S")

    result = []

    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT "n_time", "place" FROM QUAKES
        WHERE "n_time" BETWEEN ? AND ?'''
        cursor.execute(sql, (stime, etime))
        result = cursor.fetchall()
        conn.close()
    except:
        error = "error try again"

    locations = []
    for r in result:
        if stime.time() < r[0].time() < etime.time():
            locations.append([r[0], r[1]])

    return render_template('timed.html', locations=locations)


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
        cursor.execute(sql, )
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
            places.append([r[2], distance])

    print count

    return render_template('radius.html', count=count, places=places)


@queriesController.route('/north', methods=['GET'])
def north():
    return render_template('north.html', )


@queriesController.route('/northExecute', methods=['GET'])
def northExecute():
    lat = request.args['lat']
    lat = lat.encode('utf-8')
    long = request.args['long']
    long = long.encode('utf-8')
    # lat = "32.735687°N"
    # long = "97.1080656°W"

    lat_tokens = lat.split('°')
    if lat_tokens[1] == 'S':
        lat_tokens[0] = (-1) * float(lat_tokens[0])

    long_tokens = long.split('°')
    if long_tokens[1] == 'W':
        long_tokens[0] = (-1) * float(long_tokens[0])

    print lat_tokens[0]
    print long_tokens[0]

    result = []

    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT "latitude", "longitude", "place" FROM QUAKES
            WHERE "latitude" = ? AND "longitude" = ?'''
        cursor.execute(sql,(lat_tokens[0],long_tokens[0]))
        result = cursor.fetchall()
        conn.close()
    except:
        error = "error try again"

    print result
    return render_template('north.html', result = result)


@queriesController.route('/polarity', methods=['GET'])
def polarity():
    return render_template('polarity.html', )


@queriesController.route('/polarityExecute', methods=['GET'])
def polarityExecute():
    mag = request.args['mag']
    polarity = request.args['polarity']

    result = []

    try:
        conn = db.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        sql = '''SELECT "place", "mag" FROM QUAKES
            WHERE "mag" > ? AND "polarity" = ? '''
        cursor.execute(sql, (mag, polarity,))
        result = cursor.fetchall()
        conn.close()
    except:
        error = "error try again"

    return render_template('polarity.html', result = result)
