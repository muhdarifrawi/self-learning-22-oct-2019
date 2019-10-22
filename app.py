from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo

app = Flask(__name__)

@app.route("/")
def home():
    return "test data"
    
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

