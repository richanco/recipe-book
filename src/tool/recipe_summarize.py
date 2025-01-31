from playwright.sync_api import sync_playwright
import os
from pathlib import Path
from common.dao import RecipeDao
from recipe_crawler import RecipeCrawler
import psycopg2
from common import config 

# 実行中のスクリプトのディレクトリを取得
script_dir = Path(__file__).resolve().parent

# Chromeプロファイルの保存先ディレクトリ
CHROME_PROFILE_DIR = os.path.join(script_dir, "chrome_profile")

def main():
    # Playwrightを利用したブラウザ操作
    with sync_playwright() as p:
        # Chromeのプロファイルを永続化する
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=CHROME_PROFILE_DIR,  # プロファイルディレクトリ
            channel="chrome",                 # Chromeブラウザを使用
            headless=False,                   # GUIを表示
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        # ブラウザページを取得
        page = browser_context.new_page()

        # 認証が必要なウェブサイトにアクセス
        page.goto("https://cookpad.com/jp/accounts/new?return_to=https%3A%2F%2Fcookpad.com%2Fjp")

        # 初回ログインが必要ならここで操作（手動またはスクリプト）
        print("ブラウザが起動しました。必要に応じてログインを行ってください。")

        # 認証状態を確認（例: ログイン後のページに移動）
        page.goto("https://cookpad.com/jp")
        print("認証済み状態を確認しました。")
        
        print("データ収集開始します。")
        # 保存済みボタンをClick
        page.get_by_role("link", name="保存済み", exact=True).click(force=True)
        page.wait_for_url("https://cookpad.com/jp/me/library_items?sources=saved") # 画面が遷移するまで待つ処理を入れる
        
        # Cookpadの保存済みレシピのURL取得
        cookpad_crawler = RecipeCrawler()
        recipe_list = cookpad_crawler.get_saved_list(page)
        print("データ収集完了しました。")
        
        print("データペースに登録します。")
        # DBに接続
        db_param = config.LOCAL_DBPARAM if config.ENV == 'local' else config.DBPARAM
        con = psycopg2.connect(db_param) 
    
        with con:        
            for recipe in recipe_list:
                recipe_detail = cookpad_crawler.set_recipe_detail(recipe)
                # データベースにデータを登録
                recipe_dao = RecipeDao(con)
                recipe_dao.insert_recipe(recipe_detail)
        con.close()
        
        print("データペース登録完了しました。")
        # ブラウザを閉じる
        browser_context.close()

if __name__ == "__main__":
    # プロファイルディレクトリが存在しない場合は作成
    if not os.path.exists(CHROME_PROFILE_DIR):
        os.makedirs(CHROME_PROFILE_DIR)

    main()
