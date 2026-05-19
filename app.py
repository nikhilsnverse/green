from flask import Flask, render_template, Response
import os
from datetime import datetime

app = Flask(__name__)
SITE_URL = 'https://www.greenmounttower.in'

EXCLUDE_HERO = {'ab.jpeg', 'at.png', 'g4.png', 'g5.png'}

@app.route('/')
def index():
    images_dir = os.path.join(app.static_folder, 'images')
    all_files = sorted([f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))])
    hero_images = [f for f in all_files if f not in EXCLUDE_HERO]
    return render_template('index.html', images=all_files, hero_images=hero_images, site_url=SITE_URL)

@app.route('/robots.txt')
def robots():
    content = f"""User-agent: *
Allow: /
Sitemap: {SITE_URL}/sitemap.xml
"""
    return Response(content, mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    today = datetime.now().strftime('%Y-%m-%d')
    sections = [
        '', '#project', '#ongoing', '#completed',
        '#highlights', '#gallery', '#specifications',
        '#location', '#contact'
    ]
    urls = ''
    for s in sections:
        urls += f"""  <url>
    <loc>{SITE_URL}/{s}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{'1.0' if s == '' else '0.8'}</priority>
  </url>
"""
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>
"""
    return Response(content, mimetype='application/xml')

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
