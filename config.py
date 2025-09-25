class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Yankee%40143@localhost/mechanic_shop'
    DEBUG = True
    
class ProductionConfig:
    pass

class TestingConfig:
    pass