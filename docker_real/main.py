from flask import Flask, Response, request, jsonify
from PIL import Image
import pytesseract
from nltk.tokenize import WordPunctTokenizer
import enchant
import imutils
import numpy as np
import re
import cv2
import os

app = Flask(__name__)

def image_pytesseract(img):
    #img = cv2.imread(image)
    if img.shape[1] < 500:
        Fimg = cv2.cvtColor(imutils.resize(img, width=400), cv2.COLOR_BGR2GRAY)
    else:
        Fimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if not text_filtering(Fimg):

        blur = cv2.GaussianBlur(Fimg, (5, 5), 0)
        threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        return text_filtering(threshold)
    else: return True

def text_filtering(img):
    result = ''
    result = WordPunctTokenizer().tokenize(pytesseract.image_to_string(img, lang='eng', config=r'-c preserve_interword_spaces=1 --oem 3 --psm 3'))
    result = [re.sub('[^A-Za-z0-9+-/*÷=×±∓∘∙∩∪≅∀√%∄∃θπσ≠<>≤≥≡∼≈≢∝≪≫∈∋∉⊂⊃⊆⊇⋈∑∫∏∞x()]', '', i).lower() for i in result if
                   re.sub('[^A-Za-z0-9+-/*÷=×±∓∘∙∩∪≅∀√%∄∃θπσ≠<>≤≥≡∼≈≢∝≪≫∈∋∉⊂⊃⊆⊇⋈∑∫∏∞x()]', '', i) != '']

    if len(result) <= 3:
        return False
    else:
        Ncount,Ccount,Tcount,Fcount = 0,0,0,0
        for i in result:
            if i.isdigit():
                Ncount += 1
            else:
                if i in '+-/*÷=×±∓∘∙∩∪≅∀√%∄∃θπσ≠<>≤≥≡∼≈≢∝≪≫∈∋∉⊂⊃⊆⊇⋈∑∫∏∞x,.()':
                    Ccount += 1
                else:
                    temp1, temp2 = [idx for idx in range(len(i)) if i[idx].isdigit()], [idx for idx in range(len(i)) if i[idx] in '+-/*÷=×±∓∘∙∩∪≅∀√%∄∃θπσ≠<>≤≥≡∼≈≢∝≪≫∈∋∉⊂⊃⊆⊇⋈∑∫∏∞x,.()']
                    if temp1 or temp2:
                        Ncount += len(temp1)
                        Ccount += len(temp2)
                    else:
                        if enchant.Dict("en_US").check(i):
                            Tcount += 1
                        else:
                            Fcount += 1

        if ((Ccount + Ncount < Tcount + Fcount) and (Tcount <= Fcount)) or ((Tcount + Fcount >= 10) and (abs(Tcount - Fcount) < 3)):  # false일 경우 | (Ccount + Ncount + Tcount < 6) or
            return False
        else:
            return True

@app.route("/", methods=["POST"])
def test():
    image = request.files['image']
    if image_pytesseract(np.array(Image.open(image))):
        result = True
    else: result = False
    return jsonify({'result': result})

if __name__ == '__main__':
    import argparse
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080), debug=True))
