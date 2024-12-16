from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Membre

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Replace 'username', 'password', 'localhost', 'dbname' with your MySQL credentials and database details
app.config['SECRET_KEY'] = 'AnassLpro165'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:anasslpro@localhost/fge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




db.init_app(app)

# Route to home page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test')
def test():
    return render_template('test.html')

# Route to list all members
@app.route('/members')
def list_members():
    search_query = request.args.get('search', '')

    # Query the database based on the search query
    if search_query:
        # Search by name (first name or last name) or email
        members = Membre.query.filter(
            (Membre.Nom.like(f'%{search_query}%')) |
            (Membre.Prenom.like(f'%{search_query}%')) |
            (Membre.Email.like(f'%{search_query}%'))
        ).all()
    else:
        # If no search query, return all members
        members = Membre.query.all()
    
    return render_template('members.html', members=members)

# Route to add a new member
@app.route('/members/add_member', methods=['GET', 'POST'])
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
            return redirect('/members/add_member')  # Redirect back to the form to correct the input
        
        if len(nom) > 50:
            flash("The name cannot be longer than 50 characters.", 'error')
            return redirect('/members/add_member')
        
        if len(prenom) > 50:
            flash("The prénom cannot be longer than 50 characters.", 'error')
            return redirect('/members/add_member')
        
        if len(email) > 50:
            flash("The email cannot be longer than 50 characters.", 'error')
            return redirect('/members/add_member')
        try:
            # Add new member to the database
            new_member = Membre(Membre_id=id, Nom=nom, Prenom=prenom, Email=email, Role=role, Club_id=club_id)
            db.session.add(new_member)
            db.session.commit()
            
            flash("Member added succesfully", 'success')
              # Redirect to the members list
        
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'An error occurred: {str(e)}', 'error')  # Display error message
            return redirect('/members/add_member')
        
        return redirect('/members')
    
    return render_template('add_member.html')


# Route to delete a member
@app.route('/members/edit_member/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    member = Membre.query.get(id)
    
    if request.method == 'POST':
        Nom = request.form['Nom']
        Prenom = request.form['Prenom']
        Email = request.form['Email']
        Role = request.form['Role']
        Club_id = request.form['Club_id']
        
        member.Nom = Nom
        member.Prenom = Prenom
        member.Email = Email
        member.Role = Role
        member.Club_id = Club_id

        if len(Nom) > 50:
            flash("The name cannot be longer than 50 characters.", 'error')
            return redirect('/members/edit_member/' + str(id))
        
        if len(Prenom) > 50:
            flash("The prénom cannot be longer than 50 characters.", 'error')
            return redirect('/members/edit_member/' + str(id))
        
        if len(Email) > 100:
            flash("The email cannot be longer than 50 characters.", 'error')
            return redirect('/members/edit_member/' + str(id))
        
        try : 
            db.session.commit()
            flash('Member updated successfully', 'success')
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'An error occurred: {str(e)}', 'error')  # Display error message
            return redirect('/members/edit_member/' + str(id))
        
        
        return redirect('/members')  # Redirect to the members list
    
    return render_template('edit_member.html', member=member)

@app.route('/members/delete_member/<int:id>', methods=['GET', 'POST'])
def delete_member(id):
    member = Membre.query.get(id)
    db.session.delete(member)
    db.session.commit()
    flash('Member deleted successfully', 'success')
    return redirect('/members')


if __name__ == "__main__":
    app.run(debug=True)
