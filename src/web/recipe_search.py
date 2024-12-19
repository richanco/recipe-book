import psycopg2
import os
from typing import List
from itertools import groupby

def recipe_search(*ingredient_name_args:str) -> List[dict]:
    """材料名からレシピデータを抽出する

    Args:
        *ingredient_name_args(str): _description_


    Returns:
        List[dict]: _description_
    """    
    # データベースに接続
    con = psycopg2.connect(os.getenv("DB_PARAM"))
        
    with con:
        with con.cursor() as cursor:
            # 入力された材料名であいまい検索できるように設定
            search_ingredient = [f'%{name}%' for name in ingredient_name_args]
            join_list = ['ingredient.name LIKE %s' for _ in search_ingredient]
                  
            # 入力された材料名からレシピidとレシピ名を取得する
            sql = """   SELECT 
                        recipe.id,
                        recipe.menu,
                        recipe.img_url,
                        ingredient.name
                        FROM recipe
                        INNER JOIN ingredient
                        ON recipe.id = ingredient.recipe_id
                        WHERE """ + ' OR '.join(join_list) 
                                       
            # 実行処理
            cursor.execute(sql, search_ingredient)
            
            # 取得したレシピをリストに一時退避
            temp_list = cursor.fetchall()
            
            # 同じidのレシピをグループ化
            grouped = groupby(temp_list, key=lambda x: x[0])
            
            recipe_list = []
            
            # 指定材料を全て含むレシピのみを抽出
            for key, group in grouped:
                print(f'{key}:')
                group_list = list(group)
                if group_extraction(group_list, ingredient_name_args):
                    recipe_list.append(group_list[0])
                
            # 検索する材料数以上を含む                      
            recipe_data_list = []
            
            for recipe in recipe_list:
                
                # レシピID取得
                recipe_id   = recipe[0]
                # レシピ名取得
                recipe_menu = recipe[1]
                # レシピURL取得
                img_url = recipe[2]
                                
                # 材料の抽出
                ingredient_list = []
                sql = """SELECT name, amount 
                    FROM ingredient
                    WHERE recipe_id = %s"""
                # 実行処理
                cursor.execute(sql, (recipe_id,))
                for ingredient in cursor:
                    dict_ingredient = {'name': ingredient[0], 'amount': ingredient[1]}
                    ingredient_list.append(dict_ingredient) 

                # 手順を抽出
                proc_list = []
                sql = """SELECT step_num, step 
                    FROM process
                    WHERE recipe_id = %s"""
                # 実行処理
                cursor.execute(sql, (recipe_id,))
                for process in cursor:
                    dict_process = {'step_num': process[0], 'step': process[1]}
                    proc_list.append(dict_process) 

                # 辞書データに変換                
                recipe_data = {
                    'menu': recipe_menu,
                    'img_url': img_url,
                    'ingredients': ingredient_list,
                    'processes' : proc_list
                }
                recipe_data_list.append(recipe_data)
                
            return recipe_data_list

def group_extraction(group:List[tuple], ingredients:tuple[str])->bool:
    """指定の材料が全て存在するか判定

    Args:
        group (List[tuple]): _description_
        ingredients (tuple[str]): _description_

    Returns:
        bool: _description_
    """
    judge_list = []
    for ingredient in ingredients:
        bool_list = []
        for item in group:
            bool_list.append(ingredient in item[3])
        judge_list.append(any(bool_list))                              
    return  all(judge_list)
  