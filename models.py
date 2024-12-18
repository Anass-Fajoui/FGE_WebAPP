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