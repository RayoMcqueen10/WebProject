class Config: 
    SECRET_KEY ='IHohd39493(//&&%(/)ljhdsjhd128973848UHUHhhsgwgnkpipai'
    DEBUG      = True

class ConfigDevelopment(Config):
    '''MYSQL_HOST      = 'gamezone.mysql.pythonanywhere-services.com'
    MYSQL_USER      = 'gamezone'
    MYSQL_PASSWORD  = 'mysql'
    MYSQL_DB        = 'gamezone' '''
    #pythonanywhere
    MYSQL_HOST      = 'gamezone.mysql.pythonanywhere-services.com'
    MYSQL_USER      = 'gamezone'
    MYSQL_PASSWORD  = '77Antonio77'
    MYSQL_DB        = 'gamezone$gamezone'


config = {
    'development': ConfigDevelopment
} 