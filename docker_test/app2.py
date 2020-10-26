from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
import sys
from PIL import Image
import pytesseract
import argparse
import cv2

@app.route('/')
def tesseract_ocr():
    text = pytesseract.image_to_string(Image.open(t7.png))
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
