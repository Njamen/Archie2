from email.policy import default
from config import db
from datetime import datetime





#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Service(db.Model):
    __tablename__ = 'Service' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    activities = db.relationship("Activite", back_populates="service", cascade="all, delete-orphan")
    # activities = db.relationship('Activite', backref='service')    
    # activities = db.relationship("Activite", back_populates="service", lazy='joined', casc    ade="all, delete")

    def __repr__(self):
      return f'''<Service ID: {self.id},\n   name: {self.name }>''' 

class Activite(db.Model):
    __tablename__ = 'Activite' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    service_id = db.Column(db.Integer, db.ForeignKey("Service.id"), nullable=False)
    service = db.relationship("Service", back_populates="activities")
    fichiers = db.relationship("Fichier", back_populates="activite", cascade="all, delete-orphan")
    # service_id = db.Column(db.Integer, db.ForeignKey('Service.id'))
    # service = db.relationship("Service",back_populates="activities", lazy=False)

    def __repr__(self):
      return f'''<Activite ID: {self.id},\n   name: {self.name }>''' 

class Fichier(db.Model):
    __tablename__ = 'Fichier' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String,  nullable=True) 
    acivite_id = db.Column(db.Integer, db.ForeignKey("Activite.id"), nullable=False)
    activite = db.relationship("Activite", back_populates="fichiers")

    # service_id = db.Column(db.Integer, db.ForeignKey('Service.id'))
    # service = db.relationship("Service",back_populates="activities", lazy=False)

    def __repr__(self):
      return f'''<Fichier ID: {self.id},\n   name: {self.name }, 
      url: {self.url}>''' 


class Show(db.Model):
    __tablename__ = 'Show'
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime(timezone=True) , primary_key=True) 

    artist = db.relationship("Artist", back_populates="shows", lazy=False)
    venue = db.relationship("Venue",back_populates="shows", lazy=False)
 



class Venue(db.Model):
    __tablename__ = 'Venue' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String), nullable=False) 
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))   
    seeking_talent = db.Column( db.Boolean(), default=False ) 
    seeking_description = db.Column(db.String(200), default = "" )  
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))     
    shows = db.relationship("Show", back_populates="venue", lazy='joined', cascade="all, delete")

    def __repr__(self):
      return f'''<Venue ID: {self.id},\n   name: {self.name }, genres: {self.genres}, 
                  city: {self.city},   state: {self.state }, address: {self.address},
                  phone : {self.phone},   website: {self.website }, seeking_talent: {self.seeking_talent},
                  seeking_description : {self.seeking_description},   image_link: {self.image_link }, 
                  facebook_link: {self.facebook_link} , artist : {self.artist}>''' 

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String) 
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column( db.Boolean(), default=False, nullable=False ) 
    website =  db.Column(db.String(120))   
    seeking_description = db.Column(db.String(200), default = "" )  
    shows = db.relationship("Show", back_populates="artist", lazy='joined', cascade="all, delete")



    def __repr__(self):
      return f'''<Artist ID: {self.id},\n   name: {self.name }, genres: {self.genres}, 
                  city: {self.city},   state: {self.state }, phone : {self.phone},   
                  website: {self.website }, seeking_venue: {self.seeking_venue},
                  seeking_description : {self.seeking_description},   image_link: {self.image_link }, 
                  facebook_link: {self.facebook_link} >''' 




# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

