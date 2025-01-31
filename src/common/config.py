from dotenv import load_dotenv
import os
from os.path import join, dirname

ENV = os.getenv('ENV')
LOCAL_DBPARAM = os.getenv('LOCAL_DBPARAM')
DBPARAM = os.getenv('DB_PARAM')