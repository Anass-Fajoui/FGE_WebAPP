from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Membre, s_inscrire

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'AnassLpro165'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:anasslpro@localhost/fge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/members')
def list_members():
    club_id = request.args.get('Club_id')
    cellule_ids = request.args.getlist('Cellule_id')  

    search_query = request.args.get('search', '').lower() 

    query = Membre.query

    if search_query:
        query = query.filter(
            db.or_(
                Membre.Nom.ilike(f'%{search_query}%'),
                Membre.Prenom.ilike(f'%{search_query}%'),
                Membre.Email.ilike(f'%{search_query}%')
            )
        )
    
    if club_id:
        query = query.filter(Membre.Club_id == club_id)

    if cellule_ids!= [] and cellule_ids != ['']:
        query = query.join(s_inscrire, s_inscrire.Membre_id == Membre.Membre_id).filter(
            s_inscrire.Cellule_id.in_(cellule_ids)
        )

    members = query.all()

    return render_template('members.html', members=members)



@app.route('/members/add_member', methods=['POST', 'GET'])
def add_member():
    if request.method == 'POST':
        nom = request.form['Nom']
        prenom = request.form['Prenom']
        email = request.form['Email']
        role = request.form['Role']
        club_id = request.form['Club_id']
        
        
        if len(nom) > 50:
            flash("The name cannot be longer than 50 characters.", 'error')
            return redirect('/members/add_member')
        
        if len(prenom) > 50:
            flash("The prénom cannot be longer than 50 characters.", 'error')
            return redirect('/members/add_member')
        
        if len(email) > 100:
            flash("The email cannot be longer than 50 characters.", 'error')
            return redirect('/members/add_member')
        
       
        new_member = Membre(Nom=nom, Prenom=prenom, Email=email, Role=role, Club_id=club_id)
        db.session.add(new_member)
        
        
        selected_cellules = request.form.getlist('Cellule_id')
        # print(selected_cellules)
    
       
        chief_cellules = {key: value for key, value in request.form.items() if key.startswith("chief_")}

        
        for cellule_id in selected_cellules:
            est_chef = True if f"chief_{cellule_id}" in chief_cellules else False
            
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
        
        return redirect('/members') 
    
    return render_template('add_member.html')  



@app.route('/members/edit_member/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    member = Membre.query.get_or_404(id)
    
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
            flash("The email cannot be longer than 100 characters.", 'error')
            return redirect('/members/edit_member/' + str(id))

        
        selected_cellules = request.form.getlist('Cellule_id')  
        chief_cellules = {key for key in request.form if key.startswith("chief_")}  

        
        s_inscrire.query.filter_by(Membre_id=id).delete()

        
        for cellule_id in selected_cellules:
            est_chef = f"chief_{cellule_id}" in chief_cellules  
            new_inscription = s_inscrire(Membre_id=id, Cellule_id=cellule_id, EstChef=est_chef)
            db.session.add(new_inscription)

        try:
            
            db.session.commit()
            flash('Member updated successfully', 'success')
        except Exception as e:
            db.session.rollback()  
            flash(f'An error occurred: {str(e)}', 'error') 
            return redirect('/members/edit_member/' + str(id))
        
        return redirect('/members')  
    
   
    current_cellules = s_inscrire.query.filter_by(Membre_id=id).all()
    member_cellules = [inscription.Cellule_id for inscription in current_cellules]
    chief_status = {inscription.Cellule_id: inscription.EstChef for inscription in current_cellules}



    return render_template(
        'edit_member.html',
        member=member,
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
