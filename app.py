from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from flask_uploads import UploadSet, IMAGES, configure_uploads

app = Flask(__name__)

TOP_LEVEL_DIR = os.path.abspath(os.curdir) #1
upload_dir = '/static/uploads/img/' #2
app.config["UPLOADS_DEFAULT_DEST"] = TOP_LEVEL_DIR + upload_dir #3
app.config["UPLOADED_IMAGES_DEST"] = TOP_LEVEL_DIR + upload_dir #4
app.config["UPLOADED_IMAGES_URL"] = upload_dir #5

images_upload_set = UploadSet('images', IMAGES) #6
configure_uploads(app, images_upload_set) #7

#configure mongo
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'uploads_demo'
conn = pymongo.MongoClient(MONGO_URI)
db = conn[DATABASE_NAME]
#endconfigure

@app.route("/")
def home():
    return render_template("index.template.html")
    
@app.route('/', methods=['POST'])
def upload():
    image = request.files.get('image') #1 -- get the uploaded image
    filename = images_upload_set.save(image) #2 -- save it
   # create the mongo record below
    db["images"].insert_one({
        'image_url' : images_upload_set.url(filename) #3 -- save the url
    })
    return redirect(url_for('gallery'))

@app.route('/gallery')
def gallery():
    all_images = db['images'].find({}); #1
    return render_template('gallery.template.html', all_images=all_images) #2
    
#"magic code" - - boilerplate
if __name__ == "__main__":
   app.run(host=os.environ.get("IP"),
      port=int(os.environ.get("PORT")),
      debug=True)
