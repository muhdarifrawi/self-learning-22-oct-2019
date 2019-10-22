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

@app.route("/")
def home():
    return render_template("index.template.html")
    
#"magic code" - - boilerplate
if __name__ == "__main__":
   app.run(host=os.environ.get("IP"),
      port=int(os.environ.get("PORT")),
      debug=True)

# 1. Retrieve the environment variables
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'sample_airbnb'

# 2. Create the connection
conn = pymongo.MongoClient(MONGO_URI)

# 3. Query
doc = conn[DATABASE_NAME]["listingsAndReviews"].find({
    'address.country':'Canada'
}).limit(10)

for d in doc:
    print("Name:", d['name'])
    print("Price: $", d['price'])
    print('-------')

