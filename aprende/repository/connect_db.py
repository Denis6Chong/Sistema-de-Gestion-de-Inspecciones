from sqlmodel import create_engine

def connect():
    engine = create_engine("mysql+pymysql://root:Mypass_0622@172.20.10.4:3306/hello_mysql", echo=False)
    return engine