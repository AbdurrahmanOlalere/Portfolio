import db as db
import mail as mail
import os
from flask import Flask, render_template, request, url_for, jsonify 
from flask_caching import Cache
import json
import imageio
import db
# db.create_Details_table()  # moved to main guard below

app = Flask(__name__)

# Create a cache object for images
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Ensure the database and table are created before handling requests
# @app.before_request


# Set cache control headers for static files
@app.after_request
def add_cache_control(response):  
    if 'static' in request.url:
        response.headers['Cache-Control'] = 'public, max-age=3600'  # Setting the desired max-age value in seconds
    return response


@app.route('/contact')
def contact():
    images_folder = os.path.join(app.static_folder, 'img', 'portal')

    # Get the list of image file names in the folder
    image_files = os.listdir(images_folder)

    # Retrieve the image file URLs
    image_files_urls = [
        url_for('static', filename=f'img/portal/{image_file}') #changed to dragon, then a portal file
        for image_file in image_files
    ]
    # print(image_files_urls) use to check image urls

    # Convert the image file URLs to a regular list of strings
    image_files_list = [str(url) for url in image_files_urls]

    # Convert the image files list to JSON
    image_files_json = json.dumps(image_files_list)
    return render_template('contact.html', image_files_json=image_files_json)

@app.route('/')
def index():
    images_folder = os.path.join(app.static_folder, 'img', 'portal')

    # Get the list of image file names in the folder
    image_files = os.listdir(images_folder)

    # Retrieve the image file URLs
    image_files_urls = [
        url_for('static', filename=f'img/portal/{image_file}')
        for image_file in image_files
    ]

    # Convert the image file URLs to a regular list of strings
    image_files_list = [str(url) for url in image_files_urls]

    # Convert the image files list to JSON
    image_files_json = json.dumps(image_files_list)
    return render_template('index.html', image_files_json=image_files_json)

@app.route('/projects')
def projects():
    images_folder = os.path.join(app.static_folder, 'img', 'portal')

    # Get the list of image file names in the folder
    image_files = os.listdir(images_folder)

    # Retrieve the image file URLs
    image_files_urls = [
        url_for('static', filename=f'img/portal/{image_file}')
        for image_file in image_files
    ]

    # Convert the image file URLs to a regular list of strings
    image_files_list = [str(url) for url in image_files_urls]

    # Convert the image files list to JSON
    image_files_json = json.dumps(image_files_list)
    return render_template('project.html', image_files_json=image_files_json)


@app.route('/get_images')
@cache.cached(timeout=3600)  # Cache the result for 3600 seconds (1 hour)
def get_images():
    images_folder = os.path.join(app.static_folder, 'img', 'portal')

    # Get the list of image file names in the folder
    image_files = sorted(os.listdir(images_folder))

    # Retrieve the image file URLs
    image_files_urls = [
        url_for('static', filename=f'img/portal/{image_file}')
        for image_file in image_files
    ]

    return jsonify({'image_urls': image_files_urls})


# this route is giving me some trouble, the gif isn't being displayed i'm so dumb maybe nowthis works becuaase the script is called after the element exists.
@app.route("/generate_gif", methods=["POST"])
def generate_gif():
    image_folder = os.path.join(app.static_folder, 'img','portal')

    # Get the list of image file names in the folder
    image_files = os.listdir(image_folder)

    frames = []
    for filename in image_files:
        image_path = os.path.join(image_folder, filename)
        frames.append(imageio.imread(image_path))

    gif_path = "animation.gif"
    imageio.mimsave(gif_path, frames, duration=0.2)

    return jsonify({"gif_url": gif_path})
 

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
    db.create_database('portfoliodb')
    db.create_Details_table()
    app.run(host = 'localhost', port = '5000', debug=True)