class Club (object):
    def __init__(self, clubid, name, description, days, president,
                 president_netid, website, categories, email, copresident, copresident_netid, treasurer, treasurer_netid):
        self.__id = clubid
        self.__name = name
        self.__description = description
        self.__days = days
        self.__president = president
        self.__president_netid = president_netid
        self.__website = website
        self.__categories = categories
        self.__email = email
        self.__copresident = copresident
        self.__copresident_netid = copresident_netid
        self.__treasurer = treasurer
        self.__treasurer_netid = treasurer_netid

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getDescription(self):
        return self.__description

    def getDays(self):
        return self.__days

    def getPresident(self):
        return self.__president

    def getPresident_Netid(self):
        return self.__president_netid

    def getWebsite(self):
        return self.__website

    def getCategories(self):
        return self.__categories

    def getEmail(self):
        return self.__email

    def getCopresident(self):
        return self.__copresident

    def getCopresident_Netid(self):
        return self.__copresident_netid

    def getTreasurer(self):
        return self.__treasurer

    def getTreasurer_Netid(self):
        return self.__treasurer_netid
