-- データベースに接続
\c my_recipe_db

-- recipe tablezの定義変更
ALTER TABLE recipe
ADD COLUMN img_url TEXT,
ADD COLUMN url TEXT;