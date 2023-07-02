import db as db
import mail as mail
import os
from flask import Flask,render_template,request,url_for,jsonify
import json
# opencv doesn't seem to support gif so i'm trying imageio


app = Flask(__name__)

@app.route('/contact')
def contact():
    images_folder = os.path.join(app.static_folder, 'img', 'swords')

    # Get the list of image file names in the folder
    image_files = os.listdir(images_folder)

    # Retrieve the image file URLs
    image_files_urls = [
        url_for('static', filename=f'img/swords/{image_file}')
        for image_file in image_files
    ]

    # Convert the image file URLs to a regular list of strings
    image_files_list = [str(url) for url in image_files_urls]

    # Convert the image files list to JSON
    image_files_json = jsonify(image_files_list)
    return render_template('contact.html',image_files_json=image_files_json)

@app.route('/')
def index():
    images_folder = os.path.join(app.static_folder, 'img', 'swords')

    # Get the list of image file names in the folder
    image_files = os.listdir(images_folder)

    # Retrieve the image file URLs
    image_files_urls = [
        url_for('static', filename=f'img/swords/{image_file}')
        for image_file in image_files
    ]

    # Convert the image file URLs to a regular list of strings
    image_files_list = [str(url) for url in image_files_urls]

    # Convert the image files list to JSON
    image_files_json = jsonify(image_files_list)
    return render_template('index.html', image_files_json=image_files_json)



# @app.route('/get_images', methods=['GET'])
# def get_images():
#     image_folder = os.path.join(app.static_folder, 'img','swords')  # Folder path where images are stored
    
#     # Get the list of image file names in the folder
#     image_files = os.listdir(image_folder)
    
#     frames = []
#     for filename in image_files:
#         image_path = os.path.join(image_folder, filename)
#         frame = cv2.imread(image_path)
#         frames.append(frame)
        
#     return jsonify({'images': frames})


""" @app.route("/generate_gif", methods=["POST"])
def generate_gif():
    image_folder = os.path.join(app.static_folder, 'img','swords')

    # Get the list of image file names in the folder
    image_files = os.listdir(image_folder)

    frames = []
    for filename in image_files:
        image_path = os.path.join(image_folder, filename)
        frames.append(imageio.imread(image_path))

    gif_path = "animation.gif"
    imageio.mimsave(gif_path, frames, duration=0.2)

    return jsonify({"gif_url": gif_path})
 """

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