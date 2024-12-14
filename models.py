from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Membre(db.Model):
    __tablename__ = 'Membre'

    Membre_id = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(100))
    Prenom = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Role = db.Column(db.String(100))
    Club_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<Membre {self.Nom} {self.Prénom}>'
