import os
import json

from typing import Any


class JsonHandler:
    
    def __init__(self, json_filename : str, create_new : bool = False) -> None :
        """Init method for JsonHandler class

        Args:
            json_filename (str): your json filename
            create_new (bool, optional): option to create new file if which you given was not found. Defaults to False.

        Raises:
            FileNotFoundError: if the "json_filename" was not found and "create_new" was not set up to True
        """
        
        if not os.path.exists(json_filename):
            if create_new:
                with open(json_filename, 'w') as f:
                    f.write("{}")
            else:
                raise FileNotFoundError("given json file does not exists")

        self.__filename = json_filename


    def get_json(self) -> dict[str:str] :
        """Method to get json file content

        Returns:
            dict[str:str]: the content of the json file
        """
        
        with open(self.__filename, 'r') as f:
            json_object = json.load(f)
        
        return json_object


    def update(self, new_json : dict[str]) -> None :
        """Method to replace json content with a new dict

        Args:
            new_json (dict[str]): the new dict you want to write into the json file
        """
        
        with open(self.__filename, 'w') as f:
            json.dump(new_json, f)
            
    
    def expand(self, to_add : dict[str]) -> None :
        """Method to concatenate json file content with a new dict

        Args:
            to_add (dict[str]): the dict you want to add to actual json content
        """
        
        expanded_dict = self.get_json()
        expanded_dict.update(to_add)
        
        self.update(new_json=expanded_dict)
        
    
    def create_entree(self, key : str, value : Any, replace : bool = False) -> None :
        """Method to create a new pair key:value

        Args:
            key (str): the key you want to add
            value (Any): thevalue you want to add
            replace (bool, optional): option to activate if the key already exists and you want to replace it. Defaults to False.

        Raises:
            KeyError: if the key already exists and the parameter "replace" was not set to "True"
        """
        
        if self.key_exists(key) and not replace:
            raise KeyError("the pair key/value you're trying to add already exists, to replace it, make sure the parameter 'replace' is set to 'True'")

        newDict = self.get_json()
        newDict[key] = value
        
        self.update(new_json=newDict)


    def reinitialize(self, force_reinitialize : bool = True) -> None :
        """Method that reinitialize the json file

        Args:
            force_reinitialize (bool, optional): force reinitialize by deleting the file before writing in it. 
                                                 It avoids errors like corrupted file or something else. Defaults to True.
        """
        
        if force_reinitialize:
            os.remove(self.__filename)
        
        with open(self.__filename, 'w') as f:
            f.write("{}")


    def key_exists(self, key : Any) -> bool :
        """Method that returns if a key exists in json file

        Args:
            key (Any): the key you want to verify it exists

        Returns:
            bool: existence of given key
        """
        
        json_object = self.get_json()
        
        return key in json_object.keys()

