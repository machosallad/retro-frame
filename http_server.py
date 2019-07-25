#!/user/bin/env python3
"""
HTML and REST server for the retro-frame.
"""

# Imports
from flask import Flask, render_template, request, jsonify
from abstract_source import SourceType
from app import RetroFrame
import threading

# Class declarations
class RetroFrameHttpServer(threading.Thread):
    def __init__(self,handle, port):
        super(RetroFrameHttpServer,self).__init__()
        self.app_handle = handle
        # Can setup other things before thread starts

    def run(self):
        print("HTTP server is starting")
        app = Flask(__name__)

        @app.route('/')
        def index():
            return render_template("index.html")

        @app.route('/api/v1/display/brightness', methods = ['GET', 'PUT', 'PATCH'])
        def brightness():
            print(request)
            if request.method == 'GET':
                return jsonify(level=self.app_handle.display.brightness)
            elif request.method == 'PUT' or request.method == 'PATCH':
                if request.is_json:
                    content = request.get_json()
                    self.app_handle.display.brightness = content['level']
                    return jsonify(level=self.app_handle.display.brightness)
                else:
                    return 'Unsupported content-type', 400

        @app.route('/api/v1/settings/length', methods = ['GET', 'PUT', 'PATCH'])
        def length():
            if request.method == 'GET':
                return jsonify(length=self.app_handle.view_length)
            elif request.method == 'PUT' or request.method == 'PATCH':
                if request.is_json:
                    content = request.get_json()
                    self.app_handle.view_length = content['length']
                    return jsonify(length=self.app_handle.view_length)
                else:
                    return 'Unsupported content-type', 400

        @app.route('/api/v1/settings/mode', methods = ['GET', 'PUT', 'PATCH'])
        def mode():
            if request.method == 'GET':
                return jsonify(length=self.app_handle.view_length)
            elif request.method == 'PUT' or request.method == 'PATCH':
                if request.is_json:
                    content = request.get_json()
                    self.app_handle.view_length = content['length']
                    return jsonify(length=self.app_handle.view_length)
                else:
                    return 'Unsupported content-type', 400

        @app.route('/api/v1/sources/<type>/status', methods = ['GET', 'PUT', 'PATCH'])
        def source_status(type):
            if request.method == 'GET':
                return jsonify(status=self.app_handle.get_content_allowance(type))
            elif request.method == 'PUT' or request.method == 'PATCH':
                if request.is_json:
                    content = request.get_json()
                    self.app_handle.set_content_allowence(type,content['status'])
                    return jsonify(status=self.app_handle.get_content_allowance(type))
                else:
                    return 'Unsupported content-type', 400

        @app.route('/api/v1/sources/youtube/', methods = ['PUT', 'PATCH'])
        def source_youtube():
            if request.method == 'PUT' or request.method == 'PATCH':
                if request.is_json:
                    content = request.get_json()
                    if self.app_handle.rest_add_youtube_video(content['url']):
                        return 'Content started to load', 200
                    else:
                        return 'Failed to load content', 500
                else:
                    return 'Unsupported content-type', 400

        app.run()