import responder
import pymysql.cursors

api = responder.API()


@api.route("/")
def request(req, resp):

    pass


if __name__ == '__main__':
    api.run()
