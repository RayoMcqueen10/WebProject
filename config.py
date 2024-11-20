class Config: 
    SECRET_KEY ='IHohd39493(//&&%(/)ljhdsjhd128973848UHUHhhsgwgnkpipai'
    DEBUG      = True

class ConfigDevelopment(Config):
    MYSQL_HOST       = 'localhost'
    MYSQL_USER       = 'root'
    MYSQL_PASSWORD   = 'mysql'
    MYSQL_DB        = 'gamezone'
    #pythonanywhere
    '''MYSQL_HOST      = 'gamezone.mysql.pythonanywhere-services.com'
    MYSQL_USER      = 'gamezone'
    MYSQL_PASSWORD  = '777Pedro777'
    MYSQL_DB        = 'gamezone$gamezone' '''

class ConfigMail(Config):
    MAIL_SERVER     = 'smtp.gmail.com'
    MAIL_PORT       = 587
    MAIL_USE_TLS    = True
    MAIL_USE_SSL    = False
    MAIL_USERNAME   = 'pedro.cernas1877@alumnos.udg.mx'
    MAIL_PASSWORD   = 'uwgc efsj rtqq qxkr'
    MAIL_DEFAULT_SENDER = 'pedro.cernas1877@alumnos.udg.mx'
    MAIL_ASCII_ATACHMENTS = True
    
config = {
    'development': ConfigDevelopment,
    'mail'       : ConfigMail
} 