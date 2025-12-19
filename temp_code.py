import json
import base64
from flask import request, flash, redirect, url_for, render_template

def upload():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash("Upload failed...")
            return redirect(request.url)

        file = request.files['file']

        if not file or file.filename == '':
            flash("No file selected")
            return redirect(request.url)

        try:
            # Read and decode file
            file_data = file.read()
            decoded_data = base64.urlsafe_b64decode(file_data)

            # SAFE deserialization
            data = json.loads(decoded_data.decode("utf-8"))

            # Validate expected keys
            title = data.get("title")
            points = data.get("points")

            if not title or not isinstance(points, list):
                raise ValueError("Invalid file structure")

            db.add_route(get_user().id, title, points)

            return redirect(url_for('dashboard'))

        except (ValueError, json.JSONDecodeError):
            flash("Invalid or corrupted file")
            return redirect(request.url)

    return render_template('upload.html')
