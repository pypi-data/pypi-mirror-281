from flask import jsonify,request


class CustomError(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        print("__init__")
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        print("to_dict")

        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def handle_custom_error(error,logger):
    logger.error(f"CustomError: {error.message}")
    logger.error(f"Request: {request.method} {request.url}")
    logger.error(f"Headers: {request.headers}")
    if request.is_json:
        logger.error(f"Body: {request.get_json()}")
    else:
        logger.error(f"Body: {request.data}")

    if error.status_code == 500:
        response = jsonify({'message': '格式不对'})
        response.status_code = 500
    else:
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
    return response
# 自定义 TypeError 的错误处理器
def handle_type_error(error,logger):
    logger.error(f"TypeError: {error}")
    logger.error(f"Request: {request.method} {request.url}")
    logger.error(f"Headers: {request.headers}")
    if request.is_json:
        logger.error(f"Body: {request.get_json()}")
    else:
        logger.error(f"Body: {request.data}")

    response = jsonify({'message': '发生了意外错误: ' + str(error)})
    response.status_code = 500
    return response
# 422  <!doctype html>
# <html lang=en>
# <title>422 Unprocessable Entity</title>
# <h1>Unprocessable Entity</h1>
# <p>The request was well-formed but was unable to be followed due to semantic errors.</p>
def register_error_handlers(app, logger):
    app.register_error_handler(CustomError, lambda error: handle_custom_error(error, logger))
    app.register_error_handler(TypeError, lambda error: handle_type_error(error, logger))
    app.register_error_handler(AttributeError, lambda error: handle_type_error(error, logger))

