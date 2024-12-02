from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from typing import List
from common.model import Ingredient, Process, Recipe
from bs4 import BeautifulSoup
import requests

class RecipeCrawler:
    def get_saved_list(self, page: Page) -> List[Recipe]:
        """Cookpadの保存済みのレシピのURL一覧を返す

        Args:
            page (Page): _description_

        Returns:
            List[str]: _description_
        """
        # レシピのurlを取得
        url_list = []
    
        recipe_list: List[Recipe] = []

        while True:   
            # 特定のセクションを指定
            section_locator = page.locator("#main_contents a")  # 特定セクション内のリンクを取得

            # リンク数を取得
            count = section_locator.count()
            
            # セクション内のすべてのURLを取得
            for i in range(count):
                href = section_locator.nth(i).get_attribute("href")
                if href and (href.startswith('/jp/recipes/')):  # href が存在する場合のみ追加
                    menu = section_locator.nth(i).text_content().strip()  # 前後の空白を削除
                    img_url = page.get_by_role("img", name= menu).get_attribute("src")
                    recipe_list.append(Recipe( menu,img_url, f"https://cookpad.com{href}"))
                    
            next_link = page.get_by_role("link", name="次へ")        

            # 次へボタンが存在する場合は
            if next_link.is_visible():         
                # 次へのURL取得
                next_url = next_link.get_attribute("href")
                # 次へボタンをClick
                next_link.click()
                page.wait_for_url(f"**{next_url}") # 画面が遷移するまで待つ処理を入れる
            else:
                break    
        return recipe_list
    
    
    def set_recipe_detail(self, recipe: Recipe) -> Recipe:
        """レシピ詳細(材料・手順)を設定

        Args:
            recipe (Recipe): _description_

        Returns:
            Recipe: _description_
        """
        res = requests.get(recipe.url)        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 材料の抽出
        ingredient_list: List[Ingredient] = []
        ingredient_li = soup.select('#ingredients > div.ingredient-list > ol > li')
        for li_tag in ingredient_li:
            # 材料名を取得
            name = li_tag.find('span').getText()
            # 材料の量を取得
            amount = li_tag.find('bdi').getText()
            ingredient_list.append(Ingredient(name, amount))

        # 手順を抽出
        process_list: List[Process] = []
        process_li = soup.select('#steps > ol > li ')
        num = 1
        for li_tag in process_li:
            # 手順を取得
            step = li_tag.find('p').getText()
            process_list.append(Process(num, step))
            num += 1
        
        # レシピに取得したレシピ情報を設定
        recipe.set_ingredients(ingredient_list)
        recipe.set_processes(process_list)
        
        return recipe
        
        

