
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctor.db'  # SQLite database
db = SQLAlchemy(app)


class Doctor(db.Model):
    serial_number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(100)) 
    day_available = db.Column(db.String(100))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        doctor_name = request.form['doctor_name']
        search_area = request.form['search_area']
        
        try:
            # Perform a database query to retrieve the doctors based on the search criteria
            doctors = Doctor.query.filter(Doctor.name.like(f'%{doctor_name}%')).filter(Doctor.area.like(f'%{search_area}%')).all()
        except Exception as e:
            # Log the error for debugging
            print(e)
            doctors = []
            
        return render_template('search.html', doctors=doctors)

    return render_template('search.html', doctors=[])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False,host='0.0.0.0')
