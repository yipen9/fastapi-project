import base_import as base_import
import src.config as config

print(config.DATABASE_URL)


print(config.get_conf("DATABASE_URL1","1234"))