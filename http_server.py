#!/user/bin/env python3
"""
HTML and REST server for the retro-frame.
"""

# Imports
from flask import Flask, render_template, request, jsonify
from abstract_source import SourceType
from app import RetroFrame

# Global variables
app =  Flask(__name__)
app_handle = None

# Class declarations
class RetroFrameHttpServer():
    def __init__(self,handle, port):
        global app_handle 
        app_handle = handle

    def serve_forever(self):
        app.run(host="0.0.0.0", threaded=True)

# Function declarations

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/v1/display/brightness', methods = ['GET', 'PUT', 'PATCH'])
def brightness():
    print(request)
    if request.method == 'GET':
        return jsonify(level=app_handle.display.brightness)
    elif request.method == 'PUT' or request.method == 'PATCH':
        if request.is_json:
            content = request.get_json()
            app_handle.display.brightness = content['level']
            return jsonify(level=app_handle.display.brightness)
        else:
            return 'Unsupported content-type', 403

@app.route('/api/v1/settings/length', methods = ['GET', 'PUT', 'PATCH'])
def length():
    if request.method == 'GET':
        return jsonify(length=app_handle.view_length)
    elif request.method == 'PUT' or request.method == 'PATCH':
        if request.is_json:
            content = request.get_json()
            app_handle.view_length = content['length']
            return jsonify(length=app_handle.view_length)
        else:
            return 'Unsupported content-type', 403

@app.route('/api/v1/settings/mode', methods = ['GET', 'PUT', 'PATCH'])
def mode():
    if request.method == 'GET':
        return jsonify(length=app_handle.view_length)
    elif request.method == 'PUT' or request.method == 'PATCH':
        if request.is_json:
            content = request.get_json()
            app_handle.view_length = content['length']
            return jsonify(length=app_handle.view_length)
        else:
            return 'Unsupported content-type', 403

@app.route('/api/v1/sources/<type>/status', methods = ['GET', 'PUT', 'PATCH'])
def source_status(type):
    if request.method == 'GET':
        return jsonify(status=app_handle.get_content_allowance(type))
    elif request.method == 'PUT' or request.method == 'PATCH':
        if request.is_json:
            content = request.get_json()
            app_handle.set_content_allowence(type,content['status'])
            return jsonify(status=app_handle.get_content_allowance(type))
        else:
            return 'Unsupported content-type', 403

@app.route('/api/v1/sources/youtube/', methods = ['PUT', 'PATCH'])
def source_youtube():
    if request.method == 'PUT' or request.method == 'PATCH':
        if request.is_json:
            content = request.get_json()
            if app_handle.rest_add_youtube_video(content['url']):
                return 'Content started to load', 200
            else:
                return 'Failed to load content', 403
        else:
            return 'Unsupported content-type', 403