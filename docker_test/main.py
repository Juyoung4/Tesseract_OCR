from flask import Flask, request, jsonify, Response
import pytesseract
from PIL import Image
import os

@app.route('/')
def index():
    return Response("hello!! world!!")

@app.route('/apitest', methods=['POST'])
def app():
   image = request.files['image']
   text = pytesseract.image_to_string(Image.open(image), lang ='eng')
   return jsonify({'result': text})

if __name__ == '__main__':
	import argparse
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080), debug = True))