from Database import PromoDatabase
import time
from datetime import datetime, timedelta

#morning_time = 4
#evening_time = 18
#
#while True:
#    try:
#        if datetime.now().hour == morning_time or datetime.now().hour == evening_time:
#            PromoDatabase.CacheAllDeals()
#    except Exception as ex:
#        print(ex)
#    time.sleep(3600)
while True:
    try:
        PromoDatabase.CacheAllDeals()
    except Exception as ex:
        print(ex)
    time.sleep(3600)