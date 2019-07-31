#!/user/bin/env python3
"""
HTML and REST server for the retro-frame.
"""

# Imports
from flask import Flask, render_template, request, jsonify
from abstract_source import SourceType
from app import RetroFrame
import json
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
                return 'Unsupported', 400
            elif request.method == 'PUT' or request.method == 'PATCH':
                return 'Unsupported', 400

        @app.route('/api/v1/sources/<type>/status', methods = ['GET', 'PUT', 'PATCH'])
        def source_status(type):
            if request.method == 'GET':
                return jsonify(status=self.app_handle.get_content_allowance(type))
            elif request.method == 'PUT' or request.method == 'PATCH':
                if request.is_json:
                    content = request.get_json()
                    if self.app_handle.set_content_allowence(type,content['status']):
                        return jsonify(status=self.app_handle.get_content_allowance(type))
                    else:
                        return 'Failed to set status', 500
                else:
                    return 'Unsupported content-type', 400

        @app.route('/api/v1/slideshow/', methods = ['PUT', 'PATCH'])
        def source_slideshow():
            if request.method == 'PUT' or request.method == 'PATCH':
                if request.is_json:
                    content = request.get_json()
                    if self.app_handle.rest_set_slideshow_control(content['command']):
                        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
                    else:
                        return 'Unknown command received', 500
        
        @app.route('/api/v1/sources/status', methods = ['GET', 'PUT', 'PATCH'])
        def source_all_status():
            if request.method == 'GET':
                imagesStatus = self.app_handle.get_content_allowance("images")
                animationsStatus = self.app_handle.get_content_allowance("animations")
                videosStatus = self.app_handle.get_content_allowance("videos")
                giphyStatus = self.app_handle.get_content_allowance("giphy")
                youtubeStatus = self.app_handle.get_content_allowance("youtube")

                output = json.dumps(dict(images=("status",imagesStatus),animations=("status",animationsStatus),videos=("status",videosStatus),giphy=("status",giphyStatus),youtube=("status",youtubeStatus)))
                return output
                
            elif request.method == 'PUT' or request.method == 'PATCH':
                if request.is_json:
                    content = request.get_json()
                    self.app_handle.set_content_allowence("images",content['images']['status'])
                    self.app_handle.set_content_allowence("animations",content['animations']['status'])
                    self.app_handle.set_content_allowence("videos",content['videos']['status'])
                    self.app_handle.set_content_allowence("giphy",content['giphy']['status'])
                    self.app_handle.set_content_allowence("youtube",content['youtube']['status'])

                    return 'Filters updated', 200
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

        @app.route('/api/v1/sources/giphy/random', methods = ['PUT', 'PATCH'])
        def source_giphy():
            if request.method == 'PUT' or request.method == 'PATCH':
                if request.is_json:
                    content = request.get_json()
                    if self.app_handle.rest_add_giphy_video(content['tag'], content['count']):
                        return 'Content started to load', 200
                    else:
                        return 'Failed to load content', 500
                else:
                    return 'Unsupported content-type', 400

        app.run(host="0.0.0.0",threaded=True)