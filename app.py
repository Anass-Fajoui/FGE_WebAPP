from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Membre, s_inscrire

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
    # Extract filters from the query parameters
    club_id = request.args.get('Club_id')
    cellule_ids = request.args.getlist('Cellule_id')  # Get all selected cellule_ids
    
    # Build the query
    query = Membre.query
    
    if club_id:  # Filter by club
        query = query.filter(Membre.Club_id == club_id)
    
    if cellule_ids:  # Filter by cellules
        query = query.join(s_inscrire, s_inscrire.Membre_id == Membre.Membre_id).filter(s_inscrire.Cellule_id.in_(cellule_ids))
    
    # Get filtered members
    members = query.all()
    
    return render_template('members.html', members=members)

# Route to add a new member
@app.route('/members/add_member', methods=['POST', 'GET'])
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
        
        # Validate input lengths
        if len(nom) > 50:
            flash("The name cannot be longer than 50 characters.", 'error')
            return redirect('/members/add_member')
        
        if len(prenom) > 50:
            flash("The prénom cannot be longer than 50 characters.", 'error')
            return redirect('/members/add_member')
        
        if len(email) > 50:
            flash("The email cannot be longer than 50 characters.", 'error')
            return redirect('/members/add_member')
        
        # Create a new member object
        new_member = Membre(Membre_id=id, Nom=nom, Prenom=prenom, Email=email, Role=role, Club_id=club_id)
        db.session.add(new_member)
        
        # Managing memberships
        # Get the selected cellules
        selected_cellules = request.form.getlist('Cellule_id')
        print(selected_cellules)
    
        # Process chief selection
        chief_cellules = {key: value for key, value in request.form.items() if key.startswith("chief_")}

        # Add the member to the selected cellules in the s_inscrire table
        for cellule_id in selected_cellules:
            est_chef = True if f"chief_{cellule_id}" in chief_cellules else False
            # Create an entry in the s_inscrire table (which tracks memberships)
            inscription = s_inscrire(Membre_id=new_member.Membre_id, Cellule_id=int(cellule_id), EstChef=est_chef)
            db.session.add(inscription)
    
        try:
            db.session.commit()
            flash('Member added successfully', 'success')
        except Exception as e:
            print(str(e))
            flash('An error occurred ', 'error')
            db.session.rollback()
            return redirect('/members/add_member')
        
        return redirect('/members')  # Redirect to the members page after successful submission
    
    return render_template('add_member.html')  # Render the form on GET request



# Route to delete a member
@app.route('/members/edit_member/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    member = Membre.query.get_or_404(id)
    
    if request.method == 'POST':
        # Fetch basic fields
        Nom = request.form['Nom']
        Prenom = request.form['Prenom']
        Email = request.form['Email']
        Role = request.form['Role']
        Club_id = request.form['Club_id']

        # Update member details
        member.Nom = Nom
        member.Prenom = Prenom
        member.Email = Email
        member.Role = Role
        member.Club_id = Club_id

        # Input validation
        if len(Nom) > 50:
            flash("The name cannot be longer than 50 characters.", 'error')
            return redirect('/members/edit_member/' + str(id))
        
        if len(Prenom) > 50:
            flash("The prénom cannot be longer than 50 characters.", 'error')
            return redirect('/members/edit_member/' + str(id))
        
        if len(Email) > 100:
            flash("The email cannot be longer than 100 characters.", 'error')
            return redirect('/members/edit_member/' + str(id))

        # Handle cellule assignments
        selected_cellules = request.form.getlist('Cellule_id')  # Selected Cellule IDs
        chief_cellules = {key for key in request.form if key.startswith("chief_")}  # Chief checkboxes

        # Remove existing cellule assignments
        s_inscrire.query.filter_by(Membre_id=id).delete()

        # Add new cellule assignments
        for cellule_id in selected_cellules:
            est_chef = f"chief_{cellule_id}" in chief_cellules  # Check if member is marked as chief
            new_inscription = s_inscrire(Membre_id=id, Cellule_id=cellule_id, EstChef=est_chef)
            db.session.add(new_inscription)

        try:
            # Commit all changes
            db.session.commit()
            flash('Member updated successfully', 'success')
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'An error occurred: {str(e)}', 'error')  # Display error message
            return redirect('/members/edit_member/' + str(id))
        
        return redirect('/members')  # Redirect to the members list
    
    # Pre-fill current cellule data for the form
    current_cellules = s_inscrire.query.filter_by(Membre_id=id).all()
    member_cellules = [inscription.Cellule_id for inscription in current_cellules]
    chief_status = {inscription.Cellule_id: inscription.EstChef for inscription in current_cellules}

    # Fetch all cellules for the form
    # cellules = Cellule.query.all()

    return render_template(
        'edit_member.html',
        member=member,
        # cellules=cellules,
        member_cellules=member_cellules,
        chief_status=chief_status
    )


@app.route('/members/delete_member/<int:id>', methods=['GET', 'POST'])
def delete_member(id):
    s_inscrire.query.filter_by(Membre_id=id).delete()
    member = Membre.query.get(id)
    db.session.delete(member)

    db.session.commit()
    flash('Member deleted successfully', 'success')
    return redirect('/members')


if __name__ == "__main__":
    app.run(debug=True)
