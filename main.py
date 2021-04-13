# importing csv module
import csv
import pyrebase
import numpy as np
from scipy.stats import ttest_1samp
# import pandas as pd
# from sklearn.cluster import Birch
# import matplotlib.pyplot as plt
import geopy.distance


def grab():
    # csv file name
    filename1 = "hack_illinois_part1.csv"
    filename2 = "hack_illinois_part2.csv"

    # initializing the titles and rows list
    fields = []
    rows = []

    # reading csv file

    with open(filename1, 'r') as csvfile1:
        # creating a csv reader object
        csv_reader1 = csv.reader(csvfile1)

        fields = next(csv_reader1)

        # extracting each data row one by one
        for row in csv_reader1:
            rows.append(row)

    with open(filename2, 'r') as csvfile2:
        # creating a csv reader object
        csv_reader2 = csv.reader(csvfile2)

        # extracting field names through first row
        fields = next(csv_reader2)

        # extracting each data row one by one
        for row in csv_reader2:
            rows.append(row)

    print('Field names are: ' + ', '.join(field for field in fields))
    i = 0
    # first index corresponds to different asset IDs, second index is array of all data corresponding to that
    # asset ID. The data in second index is in array[8] format specified by var fields
    vehicle_by_ID = [[]]
    # first index corresponds to different vehicle types, second index is each vehicle ID.
    # third index of is array of all data corresponding to that asset ID.
    # The data in third index is in array[8] format specified by var fields
    vehicle_by_name = [[[]]]
    # keeps track of all seen vehicle types
    types = []
    count = 0
    while i < len(rows):
        # parsing each column of a row
        assetID = rows[i][0]
        if i != 0:
            vehicle_by_ID.append([])
        # group rows into 2D-ish array based on asset ID
        j = 0
        while assetID == rows[i + j][0]:
            vehicle_by_ID[count].append(rows[i + j])
            j += 1
            if (i + j) >= len(rows):
                break
        vehicle_type = vehicle_by_ID[count][0][2]
        if vehicle_type not in types:
            types.append(vehicle_type)
            vehicle_by_name.append([])
        vehicle_by_name[types.index(vehicle_type)].append(vehicle_by_ID[count])
        i += j
        count += 1
    vehicle_by_name[0].pop(0)
    return vehicle_by_ID, vehicle_by_name, types


def process(arr):
    # fuel ratio per vehicle per day
    # frpv_day[(vehicle index)][(day)] = vehicleID, day, fuel / hours
    frpv_day = []
    # fuel ratio per vehicle per month
    # frpv_month[(vehicle index)][(month)] = vehicleID, month index, fuel / hours, (if month contains days 1-30/31)
    frpv_month = []
    # fuel ratio per vehicle per 300 hours
    # frpv_300[(vehicle index)][(totalhours/300)] = vehicleID, fuel / hours, (if hours = exactly 300)
    frpv_300 = []
    # fuel ratio  per vehicle per 150 hours
    # frpv_150[(vehicle index)][(totalhours/150)] = vehicleID, fuel / hours, (if hours = exactly 150)
    frpv_150 = []
    # distance  per vehicle per day
    # dpv_day[(vehicle index)][(day)] = vehicleID, day, distance
    dpv_day = []
    # distance per vehicle per month
    # dpv_month[(vehicle index)][(month)] = vehicleID, day, distance, (if month contains days 1-30/31)
    dpv_month = []
    # area of operation per vehicle per month
    # aop_month[(vehicle index)][(month)] = vehicleID, month index, maxN, maxS, maxE, maxW, (if month contains days 1-30/31)
    aop_month = []
    # area of operation (total) per vehicle
    # aop_total[(vehicle index)] = day[0], maxN, maxS, maxE, maxW
    aop_total = []
    frpv_total = []
    dpv_total = []
    # parse data, find new variables
    i = 0
    for vehicle in arr:
        cur_day = (-1, -1)
        prev_day = (-1, -1)
        cur_month = 0
        total_distance = 0.0
        total_hours = 0.0
        hours_300 = 0.0
        hours_150 = 0.0
        fuel_300 = 0.0
        fuel_150 = 0.0
        total_fuel = 0.0
        count_300 = 0
        count_150 = 0

        maxN = -10000
        maxS = 10000
        maxE = -10000
        maxW = 10000
        # count_month = 0
        hours_month = 0
        fuel_month = 0

        complete_month = False
        date = []
        for day in vehicle:
            t = str(day[1])
            date = t.split("-")
            fuel_300 += float(day[4])
            fuel_150 += float(day[4])
            hours_300 += float(day[3])
            hours_150 += float(day[3])
            total_fuel += float(day[4])
            total_hours += float(day[3])
            if cur_month != int(date[1]):
                if cur_month == 0:
                    cur_month = int(date[1])
                    distance_month = 0
                    fuel_month = 0
                    hours_month = 0
                    complete_month = date[2] == 1
                else:
                    # aop_month.append(list((day[0], date[0], cur_month, maxN, maxS, maxE, maxW, complete_month)))
                    # dpv_month.append(list((day[0], date[0], cur_month, distance_month, complete_month)))
                    frpv_month.append(
                        list((day[0], date[0], cur_month, fuel_month / hours_month, fuel_month, hours_month,
                              lat, long, complete_month)))
                    cur_month = int(date[1])
                    distance_month = 0
                    fuel_month = 0
                    hours_month = 0
                    complete_month = True
                # count_month += 1
            hours_month += float(day[3])
            fuel_month += float(day[4])
            # if hours_300 >= 300:
            # frpv_300.append(list((day[0], date[0], date[1], date[2], fuel_300 / hours_300, fuel_300, hours_300, True)))
            # fuel_300 = 0.0
            # count_300 += 1
            # hours_300 = 0
            # if hours_150 >= 150:
            # frpv_150.append(list((day[0], date[0], date[1], date[2], fuel_150 / hours_150, fuel_150, hours_150, True)))
            # fuel_150 = 0.0
            # count_150 += 1
            # hours_150 = 0

            # if maxN < float(day[6]):
            #    maxN = float(day[6])
            # if maxS > float(day[6]):
            #    maxS = float(day[6])
            # if maxE < float(day[7]):
            #    maxE = float(day[7])
            # if maxW > float(day[7]):
            #    maxW = float(day[7])

            prev_day = cur_day
            cur_day = (float(day[6]), float(day[7]))
            distance = geopy.distance.distance(cur_day, prev_day).km * (prev_day != (-1, -1))
            total_distance += distance
            # dpv_day.append(list((day[0], date[0], date[1], date[2], distance, total_distance)))
            # frpv_day.append(
            # list((day[0], date[0], date[1], date[2], float(day[4]) / float(day[3]), float(day[4]), float(day[3]),
            # total_fuel, total_hours)))
            distance_month += distance
            lat = day[6]
            long = day[7]
        # aop_month.append(list((day[0], date[0], date[1], maxN, maxS, maxE, maxW, date[2] == 31 or date[2] == 30)))
        # dpv_month.append(list((day[0], date[0], date[1], distance_month, date[2] == 31 or date[2] == 30)))
        frpv_month.append(
            list((day[0], date[0], date[1], fuel_month / hours_month, fuel_month, hours_month,
                  lat, long, date[2] == 31 or date[2] == 30)))
        # aop_total.append(list((day[0], maxN, maxS, maxE, maxW)))
        # dpv_total.append(list((day[0], total_distance, lat, long)))
        frpv_total.append(list((day[0], total_hours, total_fuel, total_fuel / total_hours)))
        # if hours_150 > 0:
        # frpv_150.append(list((day[0], date[0], date[1], date[2], fuel_150 / hours_150, fuel_150, hours_150, False)))
        # if hours_300 > 0:
        # frpv_300.append(list((day[0], date[0], date[1], date[2], fuel_300 / hours_300, fuel_300, hours_300, False)))
        i += 1

    # a = np.array(aop_total, dtype=object)
    # np.savetxt('aop_total.csv', a, fmt="%s", delimiter=',', header="vehicleID, maxLat, minLat, maxLong, minLong")

    # a = np.array(dpv_total, dtype=object)
    # np.savetxt('dpv_total.csv', a, fmt="%s", delimiter=',', header="vehicleID, total_distance, lat, long")

    a = np.array(frpv_total, dtype=object)
    np.savetxt('frpv_total.csv', a, fmt="%s", delimiter=',', header="vehicleID, total_hours, total_fuel, fuel / hours")

    #a = np.array(aop_month, dtype=object)
    #np.savetxt('aop_month.csv', a, fmt="%s", delimiter=',',
               #header="vehicleID, year, month, maxLat, minLat, maxLong, minLong, completeMonth")

    #a = np.array(dpv_month, dtype=object)
    #np.savetxt('dpv_month.csv', a, fmt="%s", delimiter=',', header="vehicleID, year, month, distance, completeMonth")

    # a = np.array(dpv_day, dtype=object)
    # np.savetxt('dpv_day.csv', a, fmt="%s", delimiter=',', header="vehicleID, year, month, day, distance, totalDistance")

    # a = np.array(frpv_150, dtype=object)
    # np.savetxt('frpv_150.csv', a, fmt="%s", delimiter=',',
    # header="vehicleID, year, month, day, fuel / hours, fuel, hours, hours>=150")

    # a = np.array(frpv_300, dtype=object)
    # np.savetxt('frpv_300.csv', a, fmt="%s", delimiter=',',
    # header="vehicleID, year, month, day, fuel / hours, fuel, hours, hours>=300")

    a = np.array(frpv_month, dtype=object)
    np.savetxt('frpv_month.csv', a, fmt="%s", delimiter=',',
               header="vehicleID, year, month, fuel / hours,  fuel, hours, lat, long, completeMonth")

    # a = np.array(frpv_day, dtype=object)
    # np.savetxt('frpv_day.csv', a, fmt="%s", delimiter=',',
    # header="vehicleID, year, month, day, fuel / hours, fuel, hours, totalFuel, totalHours")


firebaseConfig = {
    "apiKey": "AIzaSyBXiLgoJB-ihGXR5RCRSIcRWEbbV36LUHU",
    "authDomain": "hackku-2021-trackify.firebaseapp.com",
    "databaseURL": "https://hackku-2021-trackify-default-rtdb.firebaseio.com/",
    'projectId': "hackku-2021-trackify",
    "storageBucket": "hackku-2021-trackify.appspot.com",
    "messagingSenderId": "374386429309",
    "appId": "1:374386429309:web:0862b875498b46c173d014",
    "measurementId": "G-Y24W2VEKW8"
}
arr1, arr2, veh_types = grab()
print(veh_types)
process(arr1)
print("OPA")
filename1 = "aop_month.csv"
filename2 = "aop_total.csv"
filename3 = "dpv_day.csv"
filename4 = "dpv_month.csv"
filename5 = "dpv_total.csv"
filename6 = "frpv_150.csv"
filename7 = "frpv_300.csv"
filename8 = "frpv_day.csv"
filename9 = "frpv_month.csv"
filename10 = "frpv_total.csv"

# aop_month_arr = np.genfromtxt(filename1, delimiter=',', dtype=None)
# aop_total_arr = np.genfromtxt(filename2, delimiter=',', dtype=None)
# dpv_day_arr = np.genfromtxt(filename3, delimiter=',', dtype=None)
# dpv_month_arr = np.genfromtxt(filename4, delimiter=',', dtype=None)
# dpv_total_arr = np.genfromtxt(filename5, delimiter=',', dtype=None)
# frpv_150_arr = np.genfromtxt(filename6, delimiter=',', dtype=None)
# frpv_300_arr = np.genfromtxt(filename7, delimiter=',', dtype=None)
print("hello")
# frpv_day_arr = np.genfromtxt(filename8, delimiter=',', dtype=None)
frpv_month_arr = np.genfromtxt(filename9, delimiter=',', dtype=None)
frpv_total_arr = np.genfromtxt(filename10, delimiter=',', dtype=None)


def find_type(arr, check):
    l = 0
    while l < len(arr):
        for v in arr[l]:
            if check == int(v[0][0]):
                return l
        l += 1


def favg(arr, arrt):
    te = []
    for type1 in arr:
        tfr = 0
        print(type1)
        if len(type1) == 0:
            continue
        for v in type1:
            vid = int(v[0][0])
            for x in arrt:
                if vid == int(x[0]):
                    tfr += float(x[3])
                    break
        te.append(tfr / len(type1))
    print(te)
    return te


firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

print("k")
A = []
# from favg, plaintext to not have to constantly recompute
avgs = [49.803257402237556, 49.827196974814505, 49.79350392937023,
        49.822661770372804, 49.827491765690155, 49.821742796296476]

# avgs = favg(arr2, frpv_total_arr)
print("yo")


def month_fhr():
    i = 0
    while i < 240000:
        tempID = int(frpv_month_arr[i][0])
        x = find_type(arr2, tempID)
        temp_arr = []
        while frpv_month_arr[i][0] == tempID:
            temp_arr.append(float(frpv_month_arr[i][3]))
            i += 1
            if i == 240000:
                break
        tset, pval = ttest_1samp(temp_arr, avgs[x])
        if pval < 0.05:  # alpha value is 0.05 or 5%
            A.append(list((frpv_month_arr[i - 1][0], frpv_month_arr[i - 1][1], frpv_month_arr[i - 1][2],
                           frpv_month_arr[i - 1][3], "0", "0")))
            print(temp_arr)
            # data = {"vehicle_id": str(frpv_month_arr[i - 1][0]),
            # "year": str(frpv_month_arr[i - 1][1]),
            # "month": str(frpv_month_arr[i - 1][2]),
            # "lat": "0",
            # "long": "0"}
            # db.child("maint").child(str(frpv_month_arr[i - 1][0])).set(data)

    B = np.array(A, dtype=object)
    np.savetxt('over_under_use.csv', B, fmt="%s", delimiter=',',
               header="vehicleID, year, month, fuel / hours, lat, long")


month_fhr()
# geopy.distance.distance(coords_1, coords_2).km
# n = 22
# plt.xlabel("Year")
# plt.ylabel("Arctic Sea Ice Extent (1,000,000 sq km)")
# plt.plot(year[:n], extent[:n], 'o')

# initialising pyrebase

# initialisatiing Database

# How to save a data
