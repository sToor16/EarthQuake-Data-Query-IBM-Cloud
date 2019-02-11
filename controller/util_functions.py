# -*- coding: utf-8 -*-
from config import DB_CONNECTION_STRING
import timezonefinder, pytz
from datetime import datetime
import ibm_db_dbi as db


def decdeg2dms_latitude(dd):
    negative = dd < 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    direction = 'N'
    if negative:
        direction = 'S'

    answer = str(degrees) + "°" + str(minutes) + "'" + str(seconds) + '"' + direction
    return answer

def decdeg2dms_longitude(dd):
    negative = dd < 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    direction = 'E'
    if negative:
        direction = 'W'

    answer = str(degrees) + "°" + str(minutes) + "'" + str(seconds) + '"' + direction
    return answer

def dms_to_dd(dms_value):
    dms_value = dms_value.replace("'", '°').replace('"', "°")
    dms_value = dms_value.split('°')
    d = float(dms_value[0])
    m = float(dms_value[1])
    s = float(dms_value[2])
    direction = dms_value[3]
    dd = d + float(m) / 60 + float(s) / 3600

    if direction == 'S' or direction == 'W':
        dd = (-1) * dd
    return dd

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