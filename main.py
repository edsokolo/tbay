if __name__ == '__main__':
    from tbay import *

    beyonce = User()
    beyonce.username = "bknowles"
    beyonce.password = "uhuohohohohonana"
    steve = User(username="steve", password="bingbong")
    session.add(beyonce)
    session.add(steve)
    session.commit()