-- ユーザー名「recipe_user」を作成する
-- 権限にデータベース作成権限、ユーザー作成権限を加える（スーパーユーザーではない）
CREATE USER recipe_user WITH PASSWORD 'pass' CREATEDB LOGIN;

-- recipe db
CREATE DATABASE my_recipe_db;

-- my_recipe_dbデータベースの所有者をrecipe_userに変更（推奨）
ALTER DATABASE my_recipe_db OWNER TO recipe_user

-- データベースに接続
\c my_recipe_db;

-- recipe_userにpublicスキーマの権限を付与
GRANT USAGE ON SCHEMA public TO recipe_user;
GRANT CREATE ON SCHEMA public TO recipe_user;

-- レシピユーザーにデフォルト権限を付与（新規オブジェクト向け）
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO recipe_user;

-- レシピユーザーにシーケンスの権限を付与
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO recipe_user;

-- recipe table
CREATE TABLE recipe (
    id SERIAL,
    menu varchar(100) NOT NULL,
    PRIMARY KEY (id)
) ;

-- ingredient table
CREATE TABLE ingredient (
    recipe_id Integer,
    name varchar(50) ,
    amount varchar(50) 
) ;

ALTER TABLE ingredient ALTER COLUMN amount TYPE varchar(50);

-- process table
CREATE TABLE process (
    recipe_id Integer,
    step_num Integer,
    step TEXT
) ;