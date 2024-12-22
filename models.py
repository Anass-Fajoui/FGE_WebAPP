from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Membre(db.Model):
    __tablename__ = 'Membre'

    Membre_id = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(50))
    Prenom = db.Column(db.String(50))
    Email = db.Column(db.String(100))
    Role = db.Column(db.String(100))
    Club_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<Membre {self.Nom} {self.Prénom}>'

class s_inscrire(db.Model):
    __tablename__ = 's_inscrire'

    Membre_id = db.Column(db.Integer, primary_key=True)
    Cellule_id = db.Column(db.Integer, primary_key=True)
    EstChef = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<s_inscrire {self.Membre_id} {self.Cellule_id}>'
    
class Cellule(db.Model):
    __tablename__ = 'Cellule'

    Cellule_id = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(100))

    def __repr__(self):
        return f'<Cellule {self.Nom}>'
    
class entreprise(db.Model):
    __tablename__ = 'entreprise'

    Entreprise_id = db.Column(db.Integer, primary_key=True)
    Ent_Nom = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<entreprise {self.Nom}>'
    
class sponsoriser(db.Model):
    __tablename__ = 'sponsoriser'

    Year = db.Column(db.Integer, primary_key=True)
    Entreprise_id = db.Column(db.Integer, primary_key=True)
    Sponsor_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<sponsoriser {self.Year} {self.Entreprise_id}>'
    

class evenement(db.Model):
    __tablename__ = 'evenement'
    Year = db.Column(db.Integer, primary_key=True)
    Club_id = db.Column(db.Integer, nullable=False)


class participant(db.Model):
    __tablename__ = 'participant'

    Participant_id = db.Column(db.Integer, primary_key=True)
    P_Nom = db.Column(db.String(50))
    P_Prenom = db.Column(db.String(50))
    P_Email = db.Column(db.String(100))

class employe_rh(db.Model):
    __tablename__ = 'employe_rh'

    RH_id = db.Column(db.Integer, primary_key=True)
    RH_Nom = db.Column(db.String(50))
    RH_Prenom = db.Column(db.String(50))
    RH_email = db.Column(db.String(100))
    Entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprise.Entreprise_id'), nullable=False)
    entreprise = db.relationship('entreprise', backref='employes')

class postuler(db.Model):
    __tablename__ = 'postuler'

    Participant_id = db.Column(db.Integer, primary_key=True)
    RH_id = db.Column(db.Integer, primary_key=True)
    Entreprise_id = db.Column(db.Integer, primary_key=True)
    Year = db.Column(db.Integer, primary_key=True)
    Poste = db.Column(db.String(100), nullable=False)