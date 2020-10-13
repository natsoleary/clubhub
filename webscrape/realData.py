import re
from club import Club
import psycopg2

def filter():

    f = open("ClubData.txt", 'r', encoding='utf8')
    data = f.read()

    clubs = re.findall('<div class="jumbotron">.+</div>', data)

    clubsFiltered = []

    # need to adjust club.py to handle facebook/twitter/instagram
    # need to adjust database to handle facebook/twitter/isntagram

    i = 1
    for c in clubs:

        title = desc = category =  email =  presEmail =  pres = copresEmail = copres = tresEmail = tres = website = ""  

        c = c.replace('<div class="jumbotron">', '')
        startTitle = c.index('<b>') + len('<b>')
        endTitle = c.index('</b>')
        title = c[startTitle:endTitle]
        
        c = c[endTitle+9:]
        endDesc = c.index('<br/>')
        desc = c[:endDesc]
        c = c[endDesc + len('<br/>'):]

        if c.__contains__('Category: '):
            startCat = c.index('Category: ') + len('Category: ')
            endCat = c.index('<br/>')
            category = c[startCat:endCat]
            c = c[endCat + len('<br/>'):]

        if c.__contains__('E-mail'):
            startEmail = c.index('">') + len('">')
            endEmail = c.index("</a><br/>")
            email = c[startEmail:endEmail]
            c = c[endEmail + len("</a><br/>"):]

        if c.__contains__('President'):
            mailto = c.index('mailto:') + len('mailto:')
            endmailto = c.index('@')
            presEmail = c[mailto : endmailto]
            endmailto = c.index('">')
            c = c[endmailto+len('">'):]
            endPres = c.index("</a><br/>")
            pres = c[:endPres]
            c = c[endPres + len("</a><br/>"):]

        if c.__contains__('Co-President'):
            mailto = c.index('mailto:') + len('mailto:')
            endmailto = c.index('@')
            copresEmail = c[mailto : endmailto]
            endmailto = c.index('">')
            c = c[endmailto+len('">'):]
            endCoPres = c.index("</a><br/>")
            copres = c[:endCoPres]
            c = c[endCoPres + len("</a><br/>"):]

        if c.__contains__('Treasurer'):
            mailto = c.index('mailto:') + len('mailto:')
            endmailto = c.index('@')
            tresEmail = c[mailto : endmailto]
            endmailto = c.index('">')
            c = c[endmailto+len('">'):]
            endTres = c.index("</a><br/>")
            tres = c[:endTres]
            c = c[endTres + len("</a><br/>"):]

        if c.__contains__('Website'):
            startLink = c.index('href="') + len('href="')
            endLink = c.index('">')
            website = c[startLink:endLink]

        # print("Title:", title)
        # print("Desc:", desc)
        # print("Category:", category)
        # print("Email:", email)
        # print("President Email:", presEmail)
        # print("President:", pres)
        # print("CoPresident Email:", copresEmail)
        # print("CoPresident:", copres)
        # print("Treasurer Email:", tresEmail)
        # print("Treasurer:", tres)
        # print("Website:", website)

        # print("------------------------------------------------------------------------------------------------------------------------------------------------------------")

        f = Club(i, title, desc, "", pres, presEmail, website, category, email, copres, copresEmail, tres, tresEmail)
        clubsFiltered.append(f)
        i = i + 1

    
    return clubsFiltered


def updateDatabase():
    
    credentials = "dbname=deh7cgr3q4ep2k host=ec2-107-21-126-201.compute-1.amazonaws.com port=5432 user=jsiuzyeldmymak password=5225866350e591dde0d90e57f4954c2f7c34d2991a2ba2903ea7c1b1d85fa766 sslmode=require"
    conn = psycopg2.connect(credentials)
    cursor = conn.cursor()

    # change current values in database to have diff ids (so as not to conflict)
    s = "UPDATE clubs SET clubid = %s WHERE clubid = %s"

    # replace with numbers starting 1000, to differentiate
    for i in range(1, 15):
        cursor.execute(s, [str(1000+i), str(i)])
    
    # call filter, get the clubs
    clubs = filter()
    
    # insert the clubs into the database
    s = "INSERT INTO clubs VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for club in clubs:
        params = [club.getName(), club.getDescription(), club.getDays(), club.getPresident(), club.getPresident_Netid(), club.getWebsite(), club.getCategories(), club.getEmail(), club.getCopresident(), club.getTreasurer(), club.getCopresident_Netid(), club.getTreasurer_Netid(), club.getId()]
        cursor.execute(s, params)

    # check that it worked
    check = "SELECT * FROM clubs"
    cursor.execute(check)
    rows = cursor.fetchall()

    for r in rows:
        print(r)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------------")

    # commit
    conn.commit()

    # come back and ask the boys about the days thing, don't have that for any of the new ones
    # do we make them up? leave them blank because we already have examples?


if __name__ == "__main__":
    updateDatabase()

