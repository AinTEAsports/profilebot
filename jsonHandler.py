import os
import json

from typing import Any


class JsonHandler:
    
    def __init__(self, json_filename : str, create_new : bool = False) -> None() :
        if not os.path.exists(json_filename):
            if create_new:
                with open(json_filename, 'w') as f:
                    f.write("{}")
            else:
                raise FileNotFoundError("given json file does not exists")

        self.__filename = json_filename


    def get_json(self) -> dict[str:str] :
        with open(self.__filename, 'r') as f:
            json_object = json.load(f)
        
        return json_object


    def update(self, new_json : dict[str]) -> None() :
        with open(self.__filename, 'w') as f:
            json.dump(new_json, f)
            
    
    def expand(self, to_add : dict[str]) -> None() :
        expanded_dict = self.get_json()
        expanded_dict.update(to_add)
        
        self.update(new_json=expanded_dict)
        
    
    def create_entree(self, key : str, value : Any, replace : bool = False) -> None() :
        if self.key_exists(key) and not replace:
            raise KeyError("the pair key/value you're trying to add already exists, to replace it, make sure the parameter 'replace' is set to 'True'")

        newDict = self.get_json()
        newDict[key] = value
        
        self.update(new_json=newDict)


    def reinitialize(self, force_reinitialize : bool = True) -> None() :
        if force_reinitialize:
            os.remove(self.__filename)
        
        with open(self.__filename, 'w') as f:
            f.write("{}")


    def key_exists(self, key : Any) -> bool() :
        json_object = self.get_json()
        
        return key in json_object.keys()


