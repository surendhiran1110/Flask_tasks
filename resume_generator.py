from flask import Flask, render_template, request, send_file,send_from_directory
from datetime import datetime
import os

app = Flask(__name__)

# Directory to save uploaded resumes
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create the folder if it is doesn't exist

uploaded_file_path = None  # Global variable to store the path of the uploaded file

@app.route('/', methods=['GET', 'POST'])
def index():
    global uploaded_file_path
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        objective = request.form['objective']
        education_10th_percentage = request.form['10th_percentage']
        education_12th_percentage = request.form['12th_percentage']
        education_cgpa = request.form['cgpa']
        work_experience = request.form['work_experience']
        skills = request.form['skills']
        
        # Create content to dispaly in a dowloaded file
        resume_content = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nAddress: {address}\n\n"
        resume_content += f"Objective:\n{objective}\n\n"
        resume_content += f"Education:\n10th Percentage: {education_10th_percentage}%\n12th Percentage: {education_12th_percentage}%\nCGPA: {education_cgpa}\n\n"
        resume_content += f"Work Experience:\n{work_experience}\n\n"
        resume_content += f"Skills:\n{skills}"
        
        # Save the file local server
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{name}_{timestamp}_resume.txt"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        print(file_path)
        with open(file_path, 'w') as file:
            file.write(resume_content)
        
        uploaded_file_path = file_path #uopdate the global variable
        
        return render_template('success.html', filename=filename)
    return render_template('resume_upload.html')

# dowload section
@app.route('/download', methods=['GET']) 
def download():
    global uploaded_file_path
    if uploaded_file_path and os.path.exists(uploaded_file_path):
        return send_file(uploaded_file_path, as_attachment=True, download_name=os.path.basename(uploaded_file_path))
    return "No file uploaded yet."

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
