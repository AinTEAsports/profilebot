import os
import json

from typing import Any


class JsonHandler:
    
    def __init__(self, jsonFilename : str, createNew : bool = False) -> None :
        if not os.path.exists(jsonFilename):
            if createNew:
                with open(jsonFilename, 'w') as f:
                    f.write("{}")
            else:
                raise FileNotFoundError("given json file does not exists")

        self.__filename = jsonFilename


    def getJSON(self) -> dict[str] :
        with open(self.__filename, 'r') as f:
            jsonObject = json.load(f)
        
        return jsonObject


    def update(self, newJson : dict[str]) -> None :
        with open(self.__filename, 'w') as f:
            json.dump(newJson, f)
            
    
    def expand(self, toAdd : dict[str]) -> None :
        expandedDict = self.getJSON()
        expandedDict.update(toAdd)
        
        self.update(newJson=expandedDict)
        
    
    def createEntree(self, key : str, value : Any, replace : bool = False) -> None :
        if self.keyExists(key) and not replace:
            raise KeyError("the pair key/value you're trying to add already exists, to replace it, make sure the parameter 'replace' is set to 'True'")

        newDict = self.getJSON()
        newDict[key] = value
        
        self.update(newJson=newDict)


    def reinitialize(self, forceReinitialize : bool = True) -> None :
        if forceReinitialize:
            os.remove(self.__filename)
        
        with open(self.__filename, 'w') as f:
            f.write("{}")


    def keyExists(self, key : Any) -> bool :
        jsonObject = self.getJSON()
        
        return key in jsonObject.keys()

