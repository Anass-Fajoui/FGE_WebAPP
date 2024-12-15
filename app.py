from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Membre

app = Flask(__name__)

# Replace 'username', 'password', 'localhost', 'dbname' with your MySQL credentials and database details
app.config['SECRET_KEY'] = 'AnassLpro165'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:anasslpro@localhost/fge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Route to home page
@app.route('/')
def home():
    return render_template('home.html')

# Route to list all members
@app.route('/members')
def list_members():
    members = Membre.query.all()  # Get all members from the database
    return render_template('members.html', members=members)

# Route to add a new member
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        # Get data from the form
        id = request.form['Membre_id']
        nom = request.form['Nom']
        prenom = request.form['Prenom']
        email = request.form['Email']
        role = request.form['Role']
        club_id = request.form['Club_id']
        
        # Check if the member ID already exists in the database
        existing_member = Membre.query.filter_by(Membre_id=id).first()
        if existing_member:
            flash('A member with this ID already exists.', 'error')
            return redirect('/add_member')  # Redirect back to the form to correct the input

        try:
            # Add new member to the database
            new_member = Membre(Membre_id=id, Nom=nom, Prenom=prenom, Email=email, Role=role, Club_id=club_id)
            db.session.add(new_member)
            db.session.commit()
            
            
            return redirect('/members')  # Redirect to the members list
        
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'An error occurred: {str(e)}', 'error')  # Display error message
            return redirect('/add_member')
    
    return render_template('add_member.html')


# Route to delete a member
@app.route('/edit_member/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    member = Membre.query.get(id)
    
    if request.method == 'POST':
        member.Nom = request.form['Nom']
        member.Prenom = request.form['Prenom']
        member.Email = request.form['Email']
        member.Role = request.form['Role']
        member.Club_id = request.form['Club_id']
        
        db.session.commit()
        return redirect('/members')  # Redirect to the members list
    
    return render_template('edit_member.html', member=member)

@app.route('/delete_member/<int:id>', methods=['GET', 'POST'])
def delete_member(id):
    member = Membre.query.get(id)
    db.session.delete(member)
    db.session.commit()
    return redirect('/members')


if __name__ == "__main__":
    app.run(debug=True)
