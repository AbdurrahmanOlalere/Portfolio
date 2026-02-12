import db as db
import migration as migration
import mail as mail
import os
from flask import Flask, render_template, request, url_for, jsonify, redirect
from flask_caching import Cache
import json
import imageio
# db.create_Details_table()  # moved to main guard below

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

def list_images(subfolder='portal'):
    images_folder = os.path.join(app.static_folder, 'img', subfolder)
    try:
        files = sorted(
            f for f in os.listdir(images_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
        )
    except FileNotFoundError:
        return []
    return [url_for('static', filename=f'img/{subfolder}/{f}') for f in files]

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
    image_files = list_images()  # now defined above
    return render_template('index.html', image_files=image_files)

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
 

@app.route('/insert', methods=['POST'])
def insert():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    try:
        db.insert_details(name, email, message)
        # optional: send email, logging, etc.
        return redirect(url_for('contact'))
    except Exception as e:
        print("Insert failed:", e)
        # still redirect back to contact (optionally show an error message)
        return redirect(url_for('contact'))
    
if __name__ == "__main__":
    # Run migrations only once (not on every Flask reload in debug mode)
    import sys
    if 'werkzeug.serving' not in sys.modules:  # only on first startup, not on reload
        print("Running migrations...")
        migration.create_details_table()
        print("Migrations complete.")
    
    app.run(host='localhost', port='5000', debug=True)