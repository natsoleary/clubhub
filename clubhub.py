#!/usr/bin/env python
# -----------------------------------------------------------------------
# clubhub.py
# Author: ClubHub
# -----------------------------------------------------------------------

from sys import argv
from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, request, session, flash
import os
import ssl
import flask
from database import *
from club import Club
from CASClient import CASClient

# -----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

app.secret_key = b'_!\xe0\x1a\xcb\xfbO \xee\xf3\xaa\xec\xceC-p\xe7>\xfe\xc5i:\xc9\xad'
# -----------------------------------------------------------------------
# website homepage
@app.route('/')
def index():
    # authenticate user and get netid
    netid = CASClient().authenticate()
    #netid = 'jlytle123'
    netid = netid.strip()

    # check if edit button should be displayed
    clubs = getEditables(netid)
    showEdit = True
    if len(clubs) == 0:
        showEdit = False
    categories = getCategories()
    html = render_template('mainpage.html', categories=categories, netid=netid, showEdit=showEdit)
    response = make_response(html)
    return response

# -----------------------------------------------------------------------
# website search (generation of clubs in table on mainpage)
@app.route('/search')
def search():
    # authenticate user and get netid
    netid = CASClient().authenticate()
    #netid = 'jlytle123'
    netid = netid.strip()
    #get search queries for table
    categories = getCategories()
    days = []
    catgs = []
    for x in range(0, len(categories[0])-1):
        days.append(request.args.get('Days'+str(x+2)))
    for x in range(0, len(categories[1])-1):
        catgs.append(request.args.get('Category'+str(x+2)))

    # create argument for selection from database using dictionary
    argument = {}
    argument['categories'] = catgs
    argument['days'] = days
    argument['searchquery'] = request.args.get('searchquery')

    clubs, clubDetails = getClubs(argument)
    headers, headersFull = getHeaders()
    # generate html
    html = '<div class="table-wrapper-scroll-y custom-scrollbar">'
    html += '<div class="table-responsive">'
    html += '<table class="table table-hover">'
    html += '<thead><tr class="header_dark">'
    # table headers
    for header in headers:
        html += '<th><Strong>' + header + '</Strong></th>'
    html += '</tr></thead>'
    # generate modals
    for index, club in enumerate(clubs):
        html += '<tr style="height:100px; overflow:auto;" tabindex="0" onclick="window.location=' + \
            "'#openModal" + str(index+1) + "'" + ';">'
        html += "<div id='openModal" + str(index+1) + "'class='modalDialog'>"
        html += '<div>'
        html += '<a href="#close" title="Close" class="close">X</a>'
        html += '<center><h2>' + str(club[0]) + '</h2></center>'
        html += '<table2>'
        for index2, detail in enumerate(clubDetails[index]):
            if 'Netid' in str(headersFull[index2]) or detail is None or 'Clubid' in str(headersFull[index2]):
                continue
            html += '<tr2>'
            html += '<td2><p><strong>' + str(headersFull[index2]) + ':</strong> '
            if 'President' == headersFull[index2]:
                html += '<a href="mailto:' + str(clubDetails[index][index2+1]) + '@princeton.edu">'
                html += str(detail) + '</a>'
            elif 'Copresident' == str(headersFull[index2]) or 'Treasurer' == str(headersFull[index2]):
                html += '<a href="mailto:' + str(clubDetails[index][index2+2]) + '@princeton.edu">'
                html += str(detail) + '</a>'
            elif 'Website' == str(headersFull[index2]):
                html += '<a href="' + str(detail) + '">'
                html += str(detail) + '</a>'
            elif 'Email' == str(headersFull[index2]):
                html += '<a href="mailto:' + str(detail) + '">'
                html += str(detail) + '</a>'
            else:
                html += str(detail)
            html += '</p></td2>'
            html += '</tr2>'
        html += '<center><button class="btn btn-primary"><a href="#close" title="Close" style="color:white;">CLOSE</a></button></center>'
        html += '</table2>'
        html += '</div>'
        html += '</div>'
        html += '</div>'
        # fill in table data
        for index2, c in enumerate(club):
            html += '<td style="width:33%">' + str(c) + '</td>'
        html += '</tr>'  
    html += '</table>'
    html += '</div>'
    html += '</div>'
    response = make_response(html)
    return response
# -----------------------------------------------------------------------
@app.route('/edit')
def edit():

    netid = CASClient().authenticate()
    netid = netid.strip()
    clubs = getEditables(netid)
            
    html = render_template('editclubs.html', clubs=clubs, netid=netid)
    response = make_response(html)
    return response

# -----------------------------------------------------------------------                                              
@app.route('/about')
def about():
    #netid = 'testingLocal'
    # authenticate user and get netid
    netid = CASClient().authenticate()
    netid = netid.strip()
    # determine if edit button should be available
    clubs = getEditables(netid)
    showEdit = True
    if len(clubs) == 0:
        showEdit = False
    categories = getCategories()
    html = render_template('about.html', netid=netid, showEdit=showEdit)
    response = make_response(html)
    return response

# ----------------------------------------------------------------------- 
@app.route('/updateDatabase')
def updateDatabase():
    netid = CASClient().authenticate()
    netid = netid.strip()
    newName = request.args.get('clubName')
    newDesc = request.args.get('clubDesc')
    newWeb = request.args.get('clubWeb')
    newDays = request.args.get('clubDays')
    newEmail = request.args.get('clubEmail')

    clubid = request.args.get('clubId')

    vals = [newName, newDesc, newWeb, newDays, newEmail]
    errorsuccess = editClub(clubid, vals)

    html = render_template('errorsuccess.html', errorsuccess=errorsuccess, netid=netid, showEdit=True)
    response = make_response(html)
    return response

# -----------------------------------------------------------------------
if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)

    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
