from common.model import Recipe
from psycopg2.extensions import connection

class RecipeDao:
    def __init__(self, con:connection ):
        self.con = con
    
    # recipeデータをデータベースに追加
    def insert_recipe(self, recipe:Recipe):        
            with self.con.cursor() as cursor:
                # recipeテーブルにレシピ名を追加
                sql = "INSERT INTO recipe (menu, img_url, url) VALUES (%s, %s, %s) RETURNING id"
                cursor.execute(sql, (recipe.menu, recipe. img_url, recipe.url))
                # 登録したレシピのidを取得
                recipe_id = cursor.fetchone()[0]
                
                # ingredientテーブルにレシピidと材料名、材料量を追加
                sql = "INSERT INTO ingredient (recipe_id , name, amount) VALUES (%s, %s, %s)"
                for ingredient in recipe.ingredient_list:
                    cursor.execute(sql, (recipe_id, ingredient.name, ingredient.amount))

                # processテーブルにレシピidと手順Noと手順内容を追加
                sql = "INSERT INTO process (recipe_id , step_num, step) VALUES (%s, %s, %s)"
                for process in recipe.process_list:
                    cursor.execute(sql, (recipe_id, process.num, process.step))