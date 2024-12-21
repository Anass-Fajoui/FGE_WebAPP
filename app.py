from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Membre, s_inscrire, entreprise, sponsoriser, evenement

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



@app.route('/sponsors', methods=['GET'])
# def entreprises():
#     filter_year = request.args.get('year')
#     filter_sponsor_type = request.args.get('sponsor_type')
#     search_query = request.args.get('search', '').strip()
    
#     query = db.session.query(
#         sponsoriser.Year,
#         sponsoriser.Sponsor_type,
#         entreprise.Entreprise_id,
#         entreprise.Ent_Nom
#     ).join(entreprise, sponsoriser.Entreprise_id == entreprise.Entreprise_id)
    
#     if search_query:
#         query = query.filter(entreprise.Ent_Nom.ilike(f"%{search_query}%"))

#     if filter_year:
#         query = query.filter(sponsoriser.Year == int(filter_year))
#     if filter_sponsor_type:
#         query = query.filter(sponsoriser.Sponsor_type == filter_sponsor_type)
    
#     entreprises = query.all()
    
#     # Fetch distinct years from the evenement table
#     years = [row[0] for row in db.session.query(evenement.Year).distinct()]
#     sponsor_types = ['Gold', 'Platinum', 'Silver']
    
#     return render_template(
#         'sponsors.html', 
#         entreprises=entreprises, 
#         years=years, 
#         sponsor_types=sponsor_types, 
#         selected_year=filter_year, 
#         selected_sponsor_type=filter_sponsor_type
#     )
@app.route('/sponsors', methods=['GET'])
def entreprises():
    filter_year = request.args.get('year')
    filter_sponsor_type = request.args.get('sponsor_type')
    search_query = request.args.get('search', '').strip()
    sponsors = entreprise.query

    if search_query:
        sponsors = sponsors.filter(entreprise.Ent_Nom.ilike(f"%{search_query}%"))
    
    sponsors = sponsors.join(sponsoriser, sponsoriser.Entreprise_id == entreprise.Entreprise_id)
    if filter_year:
        
        sponsors = sponsors.filter(sponsoriser.Year == int(filter_year))
    if filter_sponsor_type:
        
        sponsors = sponsors.filter(sponsoriser.Sponsor_type == filter_sponsor_type)

    entreprises = sponsors.all()
    years = [row[0] for row in db.session.query(evenement.Year).distinct()]
    

    return render_template(
        'sponsors.html', 
        entreprises=entreprises, 
        years=years, 
        selected_year=filter_year, 
        selected_sponsor_type=filter_sponsor_type
    )

@app.route('/sponsors/add_sponsor', methods=['GET', 'POST'])
def add_sponsor():
    if request.method == 'POST':
        
        sponsor_name = request.form.get('sponsor_name')
        
        selected_years = request.form.getlist('year')
        print(selected_years)
    
        # Check if the sponsor already exists
        existing_sponsor = entreprise.query.filter_by(Ent_Nom=sponsor_name).first()
        if not existing_sponsor:
            
            new_entreprise = entreprise(Ent_Nom=sponsor_name)
            db.session.add(new_entreprise)
            db.session.flush()  # Flush to get the new entreprise ID
            entreprise_id = new_entreprise.Entreprise_id
        else:
            entreprise_id = existing_sponsor.Entreprise_id

        # Add entries to the sponsoriser table
        for year in selected_years:
            new_sponsorship = sponsoriser(
                Year=int(year),
                Entreprise_id=entreprise_id,
                Sponsor_type=request.form.get(f'sponsor_type_{year}')
            )
            db.session.add(new_sponsorship)

        # Commit changes to the database
        db.session.commit()
        flash("Sponsor successfully added!", "success")
        return redirect('/sponsors')

    # Fetch all years from the evenement table
    years = [row[0] for row in db.session.query(evenement.Year).distinct()]

    return render_template('add_sponsor.html', years=years)

@app.route('/sponsors/edit_sponsor/<int:id>', methods=['GET', 'POST'])
def edit_sponsor(id):
    
    sponsor = entreprise.query.get_or_404(id)
    
    if request.method == 'POST':
        sponsor_name = request.form.get('sponsor_name')
        selected_years = request.form.getlist('year')
        
        # Update sponsor name if changed
        sponsor.Ent_Nom = sponsor_name
        
        # Get current sponsorships for this sponsor
        current_sponsorships = sponsoriser.query.filter_by(Entreprise_id=id).all()
        current_years = {s.Year for s in current_sponsorships}
        
        # Remove sponsorships for years that are no longer selected
        for sponsorship in current_sponsorships:
            if str(sponsorship.Year) not in selected_years:
                db.session.delete(sponsorship)
        
        # Add or update sponsorships for selected years
        for year in selected_years:
            year_int = int(year)
            sponsorship = sponsoriser.query.filter_by(
                Entreprise_id=id,
                Year=year_int
            ).first()
            
            if sponsorship:
                # Update existing sponsorship type
                sponsorship.Sponsor_type = request.form.get(f'sponsor_type_{year}')
            else:
                # Create new sponsorship
                new_sponsorship = sponsoriser(
                    Year=year_int,
                    Entreprise_id=id,
                    Sponsor_type=request.form.get(f'sponsor_type_{year}')
                )
                db.session.add(new_sponsorship)
        
        try:
            db.session.commit()
            flash("Sponsor successfully updated!", "success")
            return redirect('/sponsors')
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the sponsor.", "error")
            print(e)  # For debugging
            return redirect(f'/sponsors/edit_sponsor/{id}')
    
    # Get current sponsorships for pre-filling the form
    current_sponsorships = sponsoriser.query.filter_by(Entreprise_id=id).all()
    sponsor_years = [str(s.Year) for s in current_sponsorships]
    sponsor_types = {str(s.Year): s.Sponsor_type for s in current_sponsorships}
    
    # Fetch all years from the evenement table
    years = [str(row[0]) for row in db.session.query(evenement.Year).distinct()]
    
    return render_template('edit_sponsor.html', sponsor=sponsor, sponsor_years=sponsor_years, sponsor_types=sponsor_types,years=years)



@app.route('/sponsors/delete_sponsor/<int:id>', methods=['GET', 'POST'])
def delete_sponsor(id):
    sponsor = entreprise.query.get(id)
    sponsoriser.query.filter_by(Entreprise_id=id).delete()
    db.session.delete(sponsor)
    db.session.commit()
    flash('Sponsor deleted successfully', 'success')
    return redirect('/sponsors')

if __name__ == "__main__":
    
    app.run(debug=True)
