#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arulmani Sennimalai"
__date__ = "$Feb 6, 2017 2:45:33 PM$"

import urllib
import urllib2
from dateutil.parser import parse
import ast
from datetime import datetime, timedelta
import traceback

def flyby( latitude, longitude ):
    
    # data provides the necessary parameters for the API call
    data = {}
    data['lat'] = latitude
    data['lon'] = longitude
    #API_KEY is mandatory to access the API
    # checkout the https://api.nasa.gov/api.html#authentication to find more details about the access limits
    data['api_key'] = 'cCmxPDETHKP8EBQ3rLBE9AEZkvHLNasBr6wUxQjC' 
    
    # Final URL is formed with the data parameters and url value
    url_values = urllib.urlencode(data)    
    url = 'https://api.nasa.gov/planetary/earth/assets'
    full_url = url + '?' + url_values
    
    # Handling of various exceptions possible while accessing the URL
    try: 
        data = urllib2.urlopen(full_url)
    except urllib2.HTTPError, e:
        print 'HTTPError = ' + str(e.code) + " " + str(e.reason)
        return
    except urllib2.URLError, e:
        print 'URLError = ' + str(e.code) + " " + str(e.reason)
        return
    except httplib.HTTPException, e:
        print 'HTTPException'
        return
    except Exception:
        print 'generic exception: ' + traceback.format_exc()
        return
    
    # If the URL is successfully accessed, then read the data from the API
    the_page = data.read()
    dict = ast.literal_eval(the_page)
    
    # The API return value has count = "no of records available" and result = "date and ID"
    try:
        noOfRecords = dict['count']
        queryData = dict['results']
    except KeyError, e:
        print 'No valid data found - API returned: ' + str(dict)
        return
    except:
        print 'generic exception'
        return
    
    # Processing of the date value from the returned query string
    data = ast.literal_eval(str(queryData[0]))
    imageDate = data['date']
    prevDate=datetime.strptime(imageDate,'%Y-%m-%dT%H:%M:%S')
    timeDiff = []
    
    # Calculation of the avergae time delta for the particular location
    # Store the time difference between the current and previous date and store in list
    for i in range(1,noOfRecords):
        #print prevDate
        data = ast.literal_eval(str(queryData[i]))
        imageDate = data['date']
        currDate=datetime.strptime(imageDate,'%Y-%m-%dT%H:%M:%S')
        diff = (currDate-prevDate).total_seconds() / 86400
        if(diff > 0):
            timeDiff.append(diff)
            prevDate = currDate
    
    currDate = prevDate
    # Calculate the average no.of days between 2 consecutive dates in which image was taken
    avg_time_delta_days = sum(timeDiff) / len(timeDiff)
    
    # Based on the average calculate the next date and time at which image will be taken
    nextDate = currDate + timedelta(days=avg_time_delta_days)
    if((nextDate - datetime.now()).total_seconds() >= 0):
        print "Next time: " + str(nextDate)
    else:
        print "The predicated next time: " + str(nextDate) +" is in the past. Next image data is required to predict the future time "
    
    # Calculation of next date tried with mins and secs precision also
    # Resulted in the same values as timedelta in days
    '''avg_time_delta_mins = avg_time_delta_days * 1440
    avg_time_delta_secs = avg_time_delta_days * 86400'''
    '''nextDate = currDate + timedelta(minutes=avg_time_delta_mins)
    print "Next time: " + str(nextDate)
    nextDate = currDate + timedelta(seconds=avg_time_delta_secs)
    print "Next time: " + str(nextDate)'''
    # Return from the program
    return


if __name__ == "__main__":
    # Providing test input as a list
    testinput = [ [36.098592,-112.097796], [43.078154,43.078154], [36.998979,-109.045183], [37.7937007,-122.4039064], [1.5,100.75], [] ]
    for data in testinput:
        try:
            flyby(data[0],data[1])
        except IndexError:
            pass