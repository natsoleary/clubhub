#!/usr/bin/env python

# -----------------------------------------------------------------------
# database.py
# Author: ClubHub
# Methods for getting information from the database for clubs
# -----------------------------------------------------------------------

import psycopg2
from sys import argv
from club import Club

credentials = "dbname=deh7cgr3q4ep2k host=ec2-107-21-126-201.compute-1.amazonaws.com port=5432 user=jsiuzyeldmymak password=5225866350e591dde0d90e57f4954c2f7c34d2991a2ba2903ea7c1b1d85fa766 sslmode=require"

# -----------------------------------------------------------------------
def prepare(value):
    index = value.find('_')
    index2 = value.find('%')
    prepared = value
    if (index >= 0):
        prepared = prepared[:index] + '\'' + prepared[index:]
    if (index2 >= 0):
        prepared = prepared[:index2] + '\'' + prepared[index:]

    prepared = '%' + prepared + '%'
    return prepared

# -----------------------------------------------------------------------
# Returns club data when provided a dictionairy containing arguments (search query, days, categories)
def getClubs(argument):

    # base queries to be added upon
    q = "SELECT * FROM clubs"
    query = "SELECT * FROM clubs"
    conditions = False
    querywords = False
    tickboxes = False
    addbracket = False
    parameters = []

    # alter query if search term is available
    if argument['searchquery'] is not None:
        querywords = True
        conditions = True
        query += " WHERE (POSITION(%s in LOWER(name)) > 0 OR POSITION(%s in LOWER(description)) > 0 OR POSITION(%s in LOWER(days)) > 0 OR POSITION(%s in LOWER(president)) > 0 OR POSITION(%s in LOWER(president_netid)) > 0 OR POSITION(%s in LOWER(website)) > 0 OR POSITION(%s in LOWER(categories)) > 0 OR POSITION(%s in LOWER(email)) > 0 OR POSITION(%s in LOWER(copresident)) > 0 OR POSITION(%s in LOWER(copresident_netid)) > 0 OR POSITION(%s in LOWER(treasurer)) > 0 OR POSITION(%s in LOWER(treasurer_netid)) > 0)"
        for x in range(12):
            parameters.append(argument['searchquery'].lower())

    days = False
    categories = False
    d = []
    c = []
    # add all days and categories to respective arrays so that they can be appended to the query
    for x in argument['days']:
        if x is not None:
            days = True
            d.append(x)
    for x in argument['categories']:
        if x is not None:
            categories = True
            c.append(x)

    # alters query depending on what filters have been chosen
    if days == True and categories == True and querywords == True:
        query += " AND (( "
        for count, x in enumerate(d):
            if count != 0:
                query += " OR "
            query += "LOWER(days) LIKE %s"
            parameters.append("%" + x.lower() + "%")
        query += ") AND ("
        for count, x in enumerate(c):
            if count != 0:
                query += " OR "
            query += "LOWER(categories) LIKE %s"
            parameters.append("%" + x.lower() + "%")
        query += "))"

    if days == True and categories == False and querywords == True:
        query += " AND ( "
        for count, x in enumerate(d):
            if count != 0:
                query += " OR "
            query += "LOWER(days) LIKE %s"
            parameters.append("%" + x.lower() + "%")
        query += ")"

    if days == False and categories == True and querywords == True:
        query += " AND ( "
        for count, x in enumerate(c):
            if count != 0:
                query += " OR "
            query += "LOWER(categories) LIKE %s"
            parameters.append("%" + x.lower() + "%")
        query += ")"
        
    if days == True and categories == True and querywords == False:
        query += " WHERE ( "
        for count, x in enumerate(d):
            if count != 0:
                query += " OR "
            query += "LOWER(days) LIKE %s"
            parameters.append("%" + x.lower() + "%")
        query += ") AND ("
        for count, x in enumerate(c):
            if count != 0:
                query += " OR "
            query += "LOWER(categories) LIKE %s"
            parameters.append("%" + x.lower() + "%")
        query += ")"

    if days == True and categories == False and querywords == False:
        query += " WHERE ( "
        for count, x in enumerate(d):
            if count != 0:
                query += " OR "
            query += "LOWER(days) LIKE %s"
            parameters.append("%" + x.lower() + "%")
        query += ")"

    if days == False and categories == True and querywords == False:
        query += " WHERE ( "
        for count, x in enumerate(c):
            if count != 0:
                query += " OR "
            query += "LOWER(categories) LIKE %s"
            parameters.append("%" + x.lower() + "%")
        query += ")"

    # return data in alphabetical order
    query += " ORDER BY name"
    connection = psycopg2.connect(credentials)
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    clubs = cursor.fetchall()
    cursor.close()
    connection.close()
    # return meta data and full data for table and modal respectively
    clubDetails = []
    clubMeta = []
    for c in clubs:
        clubDetails.append(c)
        clubMeta.append([c[0], c[1], c[2]])

    return clubMeta, clubDetails

# -----------------------------------------------------------------------
# returns the columns in the database
def getHeaders():
    connection = psycopg2.connect(credentials)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT column_name from information_schema.columns WHERE table_name = 'clubs'")
    headers = cursor.fetchall()
    cursor.close()
    connection.close()
    headersMeta = []
    headersFull = []
    for h in range(len(headers)):
        if h < 3:
            headersMeta.append(headers[h][0].replace('_', ' ').title())
        headersFull.append(headers[h][0].replace('_', ' ').title())
    # return meta data and detailed data for table and modal respectively
    return headersMeta, headersFull

# -----------------------------------------------------------------------
# returns all the categories we can filter by
def getCategories():
    categories = [['Days', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ['Category', 'A Cappella', 'Academic', 'Career Opportunity', 'Cultural', 'Dance', 'Educational', 'Environmental', 'Games', 'Media', 'Music', 'Performing Arts', 'Political', 'Publication', 'Religious', 'Service', 'Social', 'Special Interest', 'Theater']]
    return categories

# -----------------------------------------------------------------------
def getEditables(netid):
    connection = psycopg2.connect(credentials)
    parameters = []
    clubs = []
    cursor = connection.cursor()
    query = "SELECT * FROM clubs WHERE president_netid = %s OR copresident_netid = %s OR treasurer_netid = %s"
    parameters.append(netid)
    parameters.append(netid)
    parameters.append(netid)
    cursor.execute(query, parameters)
    row = cursor.fetchone()
    #count = 1;
    while row is not None:
        club = Club(str(row[12]), str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]),
                    str(row[7]), str(row[8]), str(row[9]), str(row[10]), str(row[11]))
        clubs.append(club)
        row = cursor.fetchone()
        #count = count + 1
    cursor.close()
    connection.close()
    return clubs

# -----------------------------------------------------------------------
def editClub(clubid, newVals):
    #vals = [newName, newDesc, newWeb, newDays, newEmail]

    connection = psycopg2.connect(credentials)
    cursor = connection.cursor()

    try:
        qStr = "UPDATE clubs SET name = %s, description = %s, website = %s, days = %s, email = %s WHERE clubid = %s"
        cursor.execute(qStr, newVals + [clubid])
    except Exception as e:
        return e

    connection.commit()

    cursor.close()
    connection.close()

    return "Club edited successfully."
