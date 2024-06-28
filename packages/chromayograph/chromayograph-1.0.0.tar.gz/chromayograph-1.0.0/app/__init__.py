from flask import Flask
from flask_cors import CORS
from app.main.v1.api import *
from app.main.v2.api import *
from app.eluent_curve.api import *
from app.exceptions import register_error_handlers
from flask_apispec import FlaskApiSpec, doc
from app.mylogger import get_logger

import requests
import json
from datetime import datetime


logger = get_logger('mylogger', log_file='app.log')



def custom_schema_name_resolver(schema):
    return schema.__class__.__name__


def create_app():
    app = Flask(__name__)


    app.config.update({
        'APISPEC_SWAGGER_URL': '/swagger/',
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/',
        'APISPEC_SCHEMA_NAME_RESOLVER': custom_schema_name_resolver,
    })

    docs = FlaskApiSpec(app)
    docs.register_existing_resources()

    app.register_blueprint(main_bp_1, url_prefix='/api/v1')
    register_main_v1(docs)

    app.register_blueprint(eluent_curve_blue, url_prefix='/api/eluent')
    eluent_curve_api(docs)

    app.register_blueprint(main_bp_2, url_prefix='/api/v2')
    register_main_v2(docs)
    print(docs.spec.to_dict())
    @app.route('/swagger-json/', methods=['GET'])
    def swagger_json():
        try:
            swagger_dict = docs.spec.to_dict()
            print(json.dumps(swagger_dict, indent=2))  # 打印Swagger JSON数据
            return jsonify(swagger_dict)
        except Exception as e:
            logger.error(f"Error generating Swagger JSON: {e}")
            return jsonify({"error": "Failed to generate Swagger JSON"}), 500

    # CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register error handlers
    register_error_handlers(app,logger)

    # 启用 CORS

    @app.before_request
    def log_request_info():
        request_info = {
            "method": request.method,
            "url": request.url,
            "headers": dict(request.headers),
            "body": request.get_json() if request.is_json else request.data.decode('utf-8')
        }
        # 保存请求信息以便在after_request中使用
        request.environ['request_info'] = request_info

    @app.after_request
    def log_request_and_response_info(response):
        # 只记录状态码不等于200的响应
        if response.status_code != 200:
            separator = '-' * 80
            logger.info(separator)

            # 记录请求信息
            request_info = request.environ.get('request_info')
            if request_info:
                logger.info(f"Request: {request_info['method']} {request_info['url']}")
                logger.debug(f"Headers: {request_info['headers']}")
                logger.debug(f"Body: {request_info['body']}")

            # 记录响应信息
            logger.info(f"Response: {response.status}")
            logger.debug(f"Response Headers: {dict(response.headers)}")

            # 获取响应体并记录
            response_data = response.get_data(as_text=True)
            logger.debug(f"Response Body: {response_data}")

        return response


    return app
