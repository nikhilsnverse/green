from flask import Flask, render_template
import os

app = Flask(__name__)

EXCLUDE_HERO = {'ab.jpeg', 'at.png', 'g4.png', 'g5.png'}

@app.route('/')
def index():
    images_dir = os.path.join(app.static_folder, 'images')
    all_files = sorted([f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))])
    hero_images = [f for f in all_files if f not in EXCLUDE_HERO]
    return render_template('index.html', images=all_files, hero_images=hero_images)

@app.route('/submit_enquiry', methods=['POST'])
def submit_enquiry():
    from flask import request, jsonify
    data = request.form
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    message = data.get('message')
    print(f"Enquiry received - Name: {name}, Phone: {phone}, Email: {email}, Message: {message}")
    return jsonify({'status': 'success', 'message': 'Thank you! We will get back to you shortly.'})

if __name__ == '__main__':
    app.run(debug=True)
