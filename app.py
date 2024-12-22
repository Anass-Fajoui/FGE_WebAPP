# from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, url_for, render_template, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Membre, s_inscrire, entreprise, sponsoriser, evenement, participant, employe_rh, postuler
from functools import wraps

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'AnassLpro165'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:anasslpro@localhost/fge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

USERNAME = "admin"
PASSWORD_HASH = generate_password_hash("yourpassword")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
            session['user'] = username  
            return redirect("/dashboard")  

        flash('Invalid credentials', 'error')

    return render_template('login.html')  

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    
    return decorated_function


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/members')
@login_required
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
@login_required
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
@login_required
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
@login_required
def delete_member(id):
    s_inscrire.query.filter_by(Membre_id=id).delete()
    member = Membre.query.get(id)
    db.session.delete(member)

    db.session.commit()
    flash('Member deleted successfully', 'success')
    return redirect('/members')


@app.route('/sponsors', methods=['GET'])
@login_required
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

    sponsors = sponsors.order_by(entreprise.Entreprise_id)
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
@login_required
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
@login_required
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
@login_required
def delete_sponsor(id):
    sponsor = entreprise.query.get(id)
    sponsoriser.query.filter_by(Entreprise_id=id).delete()
    db.session.delete(sponsor)
    db.session.commit()
    flash('Sponsor deleted successfully', 'success')
    return redirect('/sponsors')


@app.route('/events', methods=['GET'])
@login_required
def events():
    filter_club = request.args.get('filter_club')
    print(filter_club)

    search_query = request.args.get('search', '').strip()
    query = evenement.query

    if search_query:
        query = query.filter(evenement.Year.ilike(f"%{search_query}%"))
    if filter_club:
        query = query.filter(evenement.Club_id == filter_club)
    
    events = query.all()
    

    return render_template('events.html', events=events, selected_club=filter_club)


@app.route('/events/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        year = int(request.form.get('Year'))
        club_id = int(request.form.get('Club_id'))
        
        existing_event = evenement.query.filter_by(Year=year).first()

        if existing_event:
            flash("Event already exists!", "error")
            return redirect('/events/add_event')
        
        new_event = evenement(Year=year, Club_id=club_id)
        try :
            db.session.add(new_event)
            db.session.commit()
            flash("Event added successfully!", "success")
            return redirect('/events')
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred:", "error")
            return redirect('/events/add_event')
        
    return render_template('add_event.html')

@app.route('/events/edit_event/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = evenement.query.get_or_404(id)
    
    if request.method == 'POST':
        year = int(request.form.get('Year'))
        club_id = int(request.form.get('Club_id'))
        
        event.Year = year
        event.Club_id = club_id
        
        try :
            db.session.commit()
            flash("Event updated successfully!", "success")
            return redirect('/events')
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred:", "error")
            return redirect(f'/events/edit_event/{id}')
    
    return render_template('edit_event.html', event=event)

@app.route('/events/delete_event/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_event(id):
    event = evenement.query.get(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully', 'success')
    return redirect('/events')


@app.route('/employe_rh')
@login_required
def manage_employe_rh():
    entreprise_id = request.args.get('entreprise_id')
    search = request.args.get('search')

    
    entreprises = entreprise.query.all()
    query = employe_rh.query
    if entreprise_id:
        query = query.filter_by(Entreprise_id=entreprise_id)
    if search:
        query = query.filter((employe_rh.RH_Nom.like(f"%{search}%")) | (employe_rh.RH_Prenom.like(f"%{search}%")) | (employe_rh.RH_email.like(f"%{search}%")))

    employes = query.all()
    return render_template('employe_rh.html', employes=employes, entreprises=entreprises, selected_entreprise_id=entreprise_id, search=search)


@app.route('/employe_rh/add_employe_rh', methods=['GET', 'POST'])
@login_required
def add_employe_rh():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        entreprise_id = request.form['entreprise_id']

        new_employe = employe_rh(RH_Nom=nom, RH_Prenom=prenom, RH_email=email, Entreprise_id=entreprise_id)
        try :
            db.session.add(new_employe)
            db.session.commit()
            flash('Employe added successfully!', 'success')
            return redirect('/employe_rh')
        except Exception as e:
            db.session.rollback()
            print(str(e))
            flash('An error occurred', 'error')
            return redirect('/employe_rh/add_employe_rh')

    entreprises = entreprise.query.all()
    return render_template('add_employe_rh.html', entreprises=entreprises)

@app.route('/employe_rh/edit_employe_rh/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employe_rh(id):
    employe = employe_rh.query.get_or_404(id)
    entreprises = entreprise.query.all()
    if request.method == 'POST':
        employe.RH_Nom = request.form['nom']
        employe.RH_Prenom = request.form['prenom']
        employe.RH_email = request.form['email']
        employe.Entreprise_id = request.form['entreprise_id']
        try:
            db.session.commit()
            flash('Employe updated successfully!', 'success')
            return redirect("/employe_rh")
        except Exception as e:
            db.session.rollback()
            print(str(e))
            flash('An error occurred', 'error')
            return redirect("/employe_rh")
        

    return render_template('edit_employe_rh.html', employe=employe, entreprises=entreprises)

@app.route('/employe_rh/delete_employe_rh/<int:id>')
@login_required
def delete_employe_rh(id):
    employe = employe_rh.query.get_or_404(id)
    try:
        db.session.delete(employe)
        db.session.commit()
        flash('Employe deleted successfully!')
        return redirect("/employe_rh")
    except Exception as e:
        db.session.rollback()
        print(str(e))
        flash('An error occurred', 'error')
        return redirect("/employe_rh")
   

@app.route('/participants')
@login_required
def list_participants():
    year = request.args.get('year')
    search_query = request.args.get('search', '')

    query = participant.query

    if search_query:
        query = query.filter(
            db.or_(
                participant.P_Nom.ilike(f'%{search_query}%'),
                participant.P_Prenom.ilike(f'%{search_query}%'),
                participant.P_Email.ilike(f'%{search_query}%')
            )
        )

    if year:
        query = query.join(postuler, postuler.Participant_id == participant.Participant_id).filter(postuler.Year==year)

    evenements = evenement.query.all()
    participants = query.all()

    return render_template('participants.html', participants=participants, evenements=evenements,year=year, search=search_query)

@app.route('/participants/add_participant', methods=['GET', 'POST'])
@login_required
def add_participant():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']

        new_participant = participant(P_Nom=nom, P_Prenom=prenom, P_Email=email)
        try:
            db.session.add(new_participant)
            db.session.commit()
            flash('Participant added successfully!', 'success')
            return redirect('/participants')
        except Exception as e:
            db.session.rollback()
            print(str(e))
            flash('An error occurred', 'error')
            return redirect('/participants/add_participant')
        

    return render_template('add_participant.html')

@app.route('/participants/edit_participant/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_participant(id):
    participant_ = participant.query.get_or_404(id)

    if request.method == 'POST':
        participant_.P_Nom = request.form['nom']
        participant_.P_Prenom = request.form['prenom']
        participant_.P_Email = request.form['email']

        try:
            db.session.commit()
            flash('Participant updated successfully!', 'success')
            return redirect("/participants")
        except Exception as e:
            db.session.rollback()
            print(str(e))
            flash('An error occurred', 'error')
            return redirect("/participants/edit_participant/" + str(id))
        

    return render_template('edit_participant.html', participant=participant_)

@app.route('/participants/delete_participant/<int:id>')
@login_required
def delete_participant(id):
    participant_ = participant.query.get_or_404(id)
    try:
        db.session.delete(participant_)
        db.session.commit()
        flash('Participant deleted successfully!')
        return redirect("/participants")
    except Exception as e:
        db.session.rollback()
        print(str(e))
        flash('An error occurred', 'error')
        return redirect("/participants")


@app.route('/participants/<int:id>/interviews', methods=['GET', 'POST'])
@login_required
def participant_interviews(id):
    participant_ = participant.query.get_or_404(id)
    selected_year = request.args.get('year')
    print(selected_year)
    interviews = postuler.query.filter_by(Participant_id=id)

    if selected_year:
        interviews = interviews.filter_by(Year=selected_year)

    evenements = evenement.query.all()
    return render_template('interviews.html', interviews=interviews, participant=participant_, evenements=evenements, selected_year=selected_year)
        
@app.route('/participants/<int:id>/add_interview', methods=['GET', 'POST'])
@login_required
def add_interview(id):
    employes = employe_rh.query.all()
    entreprises = entreprise.query.all()
    years = evenement.query.all()

    if request.method == 'POST':
        
        year = request.form['year']
        rh_id = request.form['rh_id']
        poste = request.form['poste']
        entreprise_id = request.form['entreprise']

        new_interview = postuler(Participant_id=id, RH_id=rh_id, Entreprise_id=entreprise_id, Year=year, Poste=poste)
        try:
            db.session.add(new_interview)
            db.session.commit()
            flash('Interview added successfully!', 'success')
            return redirect(f'/participants/{id}/interviews')
        except Exception as e:
            db.session.rollback()
            print(str(e))
            flash('An error occurred', 'error')
            return redirect(f'/participants/{id}/interviews/add_interview')

    
    return render_template('add_interview.html', employes=employes, entreprises=entreprises, years=years)


@app.route('/participants/<int:id>/edit_interview/<int:interview_id>', methods=['GET', 'POST'])
@login_required
def edit_interview(id, interview_id):
    interview = postuler.query.get_or_404(interview_id)
    employes = employe_rh.query.all()
    entreprises = entreprise.query.all()
    years = evenement.query.all()

    if request.method == 'POST':
        interview.Year = request.form['year']
        interview.RH_id = request.form['rh_id']
        interview.Poste = request.form['poste']
        interview.Entreprise_id = request.form['entreprise']

        try:
            db.session.commit()
            flash('Interview updated successfully!', 'success')
            return redirect(f'/participants/{id}/interviews')
        except Exception as e:
            db.session.rollback()
            print(str(e))
            flash('An error occurred', 'error')
            return redirect(f'/participants/{id}/interviews/edit_interview/{interview_id}')

    return render_template('edit_interview.html', interview=interview, employes=employes, entreprises=entreprises, years=years)

@app.route('/participants/<int:id>/delete_interview/<int:interview_id>')
@login_required
def delete_interview(id, interview_id):
    interview = postuler.query.get_or_404(interview_id)
    try:
        db.session.delete(interview)
        db.session.commit()
        flash('Interview deleted successfully!')
        return redirect(f'/participants/{id}/interviews')
    except Exception as e:
        db.session.rollback()
        print(str(e))
        flash('An error occurred', 'error')
        return redirect(f'/participants/{id}/interviews')


@app.route('/logout')
@login_required
def logout():
    session.pop('user', None) 
    return redirect("/login")

if __name__ == "__main__":
    
    app.run(debug=True)
 
