import db as db
import mail as mail
import os
from flask import Flask,render_template,request, jsonify


app = Flask(__name__)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_images', methods=['GET'])
def get_images():
    image_folder = os.path.join(app.static_folder, 'img','swords')  # Folder path where images are stored
    images = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder)]
    return jsonify({'images': images})

@app.route('/insert', methods = ['POST'])
def insert():
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        mail.send_email(name,email,message)
        db.insert_details(name,email,message)
        details = db.get_details()
        print(details)
        for detail in details:
            var = detail
        return render_template('contact.html', var=var)
    
if __name__ == "__main__":
    
    app.run(host = 'localhost', port = '5000', debug=True)