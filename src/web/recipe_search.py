import psycopg2
import os
from typing import List

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
            # 入力された材料名からレシピidとレシピ名を取得する
            sql = """SELECT 
                        recipe.id, 
                        menu,
                        img_url
                    FROM recipe
                    INNER JOIN (
                        SELECT 
                            id, 
                            COUNT(*) as cnt
                        FROM recipe
                        INNER JOIN ingredient ON recipe.id = ingredient.recipe_id
                        WHERE name ~ %s
                        GROUP BY id
                    ) ingredient_count 
                    ON recipe.id = ingredient_count.id
                    WHERE ingredient_count.cnt >= %s
                    LIMIT 10"""
            
            # 材料名を正規表現で検索
            search_ingredient = '|'.join('(.*'+ ingredient_name + '.*)' for ingredient_name in ingredient_name_args)
            # 実行処理
            cursor.execute(sql, (search_ingredient, len(ingredient_name_args)))
            
            # 取得したレシピをリストに一時退避
            recipe_list = []
            for recipe in cursor:
                recipe_list.append(recipe)

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
