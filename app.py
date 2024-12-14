from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace 'username', 'password', 'localhost', 'dbname' with your MySQL credentials and database details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:anasslpro@localhost/fge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your model (assuming a table called Membre)
class Membre(db.Model):
    __tablename__ = 'Membre'
    Membre_id = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(100))
    Prenom = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Role = db.Column(db.String(50))
    Club_id = db.Column(db.Integer)

# Route to list all members
@app.route('/members')
def list_members():
    members = Membre.query.all()  # Get all members from the database
    return render_template('members.html', members=members)


@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        # Get data from form
        id = request.form['Membre_id']
        nom = request.form['Nom']
        prenom = request.form['Prenom']
        email = request.form['Email']
        role = request.form['Role']
        club_id = request.form['Club_id']
        
        # Add new member to the database
        new_member = Membre(Membre_id=id, Nom=nom, Prenom=prenom, Email=email, Role=role, Club_id=club_id)
        db.session.add(new_member)
        db.session.commit()
        
        return redirect('/members')  # Redirect to the members list
    
    return render_template('add_member.html')

if __name__ == "__main__":
    app.run(debug=True)
