import responder
import pymysql.cursors

api = responder.API()


@api.route("/ref")
def request(req, resp):
    """
    urlにsfenの局面をパラメタとして埋め込むことも考えたが
    特殊記号とかでエラーを招きそうなのでPOSTのボディに埋め込む
    :param req:
    :param resp:
    :return:

    """
    pass


if __name__ == '__main__':
    api.run()
