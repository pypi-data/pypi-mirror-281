import requests
import json
import random

def get(link: str):
    r = requests.get(link)
    return json.loads(r.text)

def getCharacterbyID(id: int):
    return get("https://stand-by-me.herokuapp.com/api/v1/characters/{}".format(str(id)))
    
def getAllCharacters():
    return get("https://stand-by-me.herokuapp.com/api/v1/characters/")

def getCharacterbyQuery(category: str, query: str):
    return get("https://stand-by-me.herokuapp.com/api/v1/characters/query/query?{0}={1}".format(category, query))

def getRandomCharacter():
    return get("https://stand-by-me.herokuapp.com/api/v1/characters/{}".format(random.randint(1, 155)))

def getStandbyID(id: int):
    return get("https://stand-by-me.herokuapp.com/api/v1/stands/{}".format(str(id)))

def getAllStands():
    return get("https://stand-by-me.herokuapp.com/api/v1/stands/")

def getStandbyQuery(category: str, query: str):
    return get("https://stand-by-me.herokuapp.com/api/v1/stands/query/query?{0}={1}".format(category, query))

def getRandomStand():
    return get("https://stand-by-me.herokuapp.com/api/v1/stands/{}".format(random.randint(1, 155)))