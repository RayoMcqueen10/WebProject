class Config: 
    SECRET_KEY ='IHohd39493(//&&%(/)ljhdsjhd128973848UHUHhhsgwgnkpipai'
    DEBUG      = True

class ConfigDevelopment(Config):
    MYSQL_HOST      = 'localhost'
    MYSQL_USER      = 'root'
    MYSQL_PASSWORD  = 'mysql'
    MYSQL_DB        = 'gamezone'

config ={
    'developmnet': ConfigDevelopment
} 