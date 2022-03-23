from flask import Flask,render_template,request
from logging import FileHandler,WARNING
import urllib.request
import os
from PIL import Image
import cv2
import easyocr
from easyocr import Reader
#import numpy as np
import pickle
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

#--------------------------------------------Category----------------------------------------------
All_dictionary = [
    {'Apparel':[{'Topwear':['Tshirt','Shirt','Dress','Jacket','Tops','Undershirt','Pullover']},
            {'Bottomwear':  ['Jeans','Pant','Shorts','Skirt','Trouser']},
            {'Outerwear': ['Coat','Sweater','Hoodie','Cardigan','Blazer','Knit']}]},
            
    {'Footwear':[{'Casual':['Sandal','Flipflop','Boots','Heels','Flats']},
            {'Formal': ['Shoes']},
            {'Sports':['Sneaker']}]},
            
    {'Accessories': [{'Bags' : ['Bagpack','Handbag','Dufflebag','Slingbag']},
                {'Wristwear' : ['Watch','Cufflink','Gloves','Wristband']},
                {'Eyewear' : ['Sunglass']},
                {'Jewellery' : ['Necklace','Ring','Bracelet','Pendent','Earring']},
                {'hats' : ['Cap','Hat','Beanie cap']},
                {'Others' : ['Scarf','Socks','Wallet','Belt','Ties']}]},

    {'Furniture': [{'Storage' : ['Wardrobe','Trolley','Drawer','Cabinet']},
                {'Display' : ['Table','Hanger']},
                {'Others' : ['Chair','Stool','Sofa']}]}
                ]

#------------------------------------All product label--------------------------------------------

All_categories = ['Tshirt','Shirt','Dress','Jacket','Tops','Undershirt','Pullover','Jeans','Pant','Shorts','Skirt','Trouser',
                    'Coat','Sweater','Hoodie','Cardigan','Blazer','Knit','Sandal','Flipflop','Boots','Heels','Flats','Shoes',
                    'Sneaker','Bagpack','Handbag','Dufflebag','Slingbag','Watch','Cufflink','Gloves','Wristband','Sunglass',
                    'Necklace','Ring','Bracelet','Pendent','Earring','Cap','Hat','Beanie cap','Scarf','Socks','Wallet','Belt',
                    'Ties','Wardrobe','Trolley','Drawer','Cabinet','Table','Hanger','Chair','Stool','Sofa']

app = Flask(__name__,template_folder="template")
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

def extract_label(img):
    lst = []
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img, detail=0)
    #result = result.title()
    #lst = lst.append(i for i in result)
    lst = ''.join(''.join(i) for i in str(result).title())
    print(lst)
    for i in All_categories:
        if i in lst:
            return (i)

def get_category_detail(label):
    if label == 'Innerwear':
        sub_cat = 'Innerwear'
        cat = 'Apparel'
    else:
        for i in All_dictionary:
            for j in i.values():
                for k in j:
                    for l in k.values():
                        if label in l:
                            sub_cat = np.array(list(k.keys()))
                            cat = np.array(list(i.keys()))
                            sub_cat = ''.join(map(str,sub_cat))
                            cat = ''.join(map(str,cat))
                            return (sub_cat,cat)


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/predict", methods = ['GET','POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file_path = os.path.join('static//', filename)
        file.save(file_path)
        extracted_label = extract_label(file_path)
        print(extracted_label)
        if extracted_label !=  None:
            sub_cat,cat = get_category_detail(extracted_label)
            return render_template('predict.html', product = extracted_label,sub_cat = sub_cat,cat = cat,user_image = file_path)
        else:
            product = "No label found"
            sub_cat = "No sub-category found"
            cat = "No category found"
            return render_template('predict.html', product=product,sub_cat = sub_cat,cat = cat,user_image=file_path)



if __name__ == "__main__":
    app.run()
