class User:
    username = ""
    diseases = []
    allergy = []
    smoke = False
    alcohol = False
    goodfoods = []
    notfoods = []
    def __init__(self,username, diseases, allergy, smoke, alcohol):
        self.username = username
        self.diseases = diseases
        self.allergy = allergy
        self.smoke = smoke
        self.alcohol = alcohol

    def getName(self):
        return self.name

    def getGender(self):
        return self.gender

    def getDisease(self):
        return self.diseases

    def getAllergy(self):
        return self.allergy

    def getSmoke(self):
        return self.smoke

    def getUser(self):
        return self

    def getAlcohl(self):
        return  self.alcohol

    def getGoodsFoods(self):
        return self.goodfoods

    def getNotFoods(self):
        return self.notfoods
