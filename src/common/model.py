from typing import List

class Ingredient:
    def __init__(self, name: str, amount: str):
        self.name = name
        self.amount = amount
                
class Process:
    def __init__(self, num: int, step: str):
        self.num = num        
        self.step = step
    
class Recipe:
    def __init__(self, menu: str, img_url: str, url: str):
        self.menu = menu
        self.img_url = img_url
        self.url = url

    # ingredient_listフィールドを設定するメソッド
    def set_ingredients(self, ingredient_list: List[Ingredient]):
        self.ingredient_list = ingredient_list

    # process_listフィールドを設定するメソッド
    def set_processes(self, process_list: List[Process]):
        self.process_list = process_list        
        
        
