import flask.ext.restful.reqparse as reqparse
from werkzeug.exceptions import ClientDisconnected
from flask_restful import Api

from config import Config
TAG = '0.01'

class APIException(Exception):

    def __init__(self, message, code=400):
        Exception.__init__(self, message)
        self.message = message
        self.code = code
        self.status = 'error'
        self.version = TAG

class RequestParser(reqparse.RequestParser):
    """Wrap reqparse to raise APIException."""

    def parse_args(self, *args, **kwargs):
        try:
            return super(RequestParser, self).parse_args(*args, **kwargs)
        except ClientDisconnected as exc:
            raise APIException(exc.data['message'], 400)

class AbacoApi(Api):
    """General flask_restful Api subclass for all the APIs in the Abaco system."""

    show_traceback = Config.get('web', 'show_traceback')

    def handle_error(self, exc):
        if AbacoApi.show_traceback == 'true':
            raise exc
        if isinstance(exc, APIException):
            return self.make_response(data=error(msg=exc.message), code=exc.code)
        else:
            return self.make_response(data=error(), code=500)


def ok(result, msg="The request was successful"):
    d = {'result': result,
         'status': 'success',
         'version': TAG,
         'msg': msg}
    return d

def error(result=None, msg="Error processing the request."):
    d = {'result': result,
         'status': 'error',
         'version': TAG,
         'msg': msg}
    return d