from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean(), unique=False, nullable=False)
    firstname = db.Column(db.String(80), nullable=True)
    lastname = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
            # Do not serialize the password, its a security breach
        return {"id": self.id,
                "email": self.email,
                "username": self.username,
                'firstname': self.firstname,
                'lastname': self.lastname,
                'is_active': self.is_active,
                'is_admin': self.is_admin,
            }


class Posts(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_to = db.relationship('Users', foreign_keys=[user_id], backref=db.backref('post_to', lazy='select'))

    def __repr__(self):
        return f'<Post {self.user_id}>'

    def serialize(self):
        return{"user.id": self.user_id}


class Followers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_from_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_from_to = db.relationship('Users', foreign_keys=[user_from_id])
    user_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_to_to = db.relationship('Users', foreign_keys=[user_to_id])

    def __repr__(self):
        return f'<Followers {self.user_from_id} - {self.user_to_id}>'

    def serialize(self):
        return{"user_from_id": self.user_from_id,
                "user_to_id": self.user_to_id
        }


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comments_text = db.Column(db.String(200), unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author_to = db.relationship('Users', foreign_keys=[author_id])
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', foreign_keys=[user_id], backref=db.backref('comment_to', lazy='select'))

    def __repr__(self):
        return f'Comments {self.comments_text}'

    def serialize(self):
        return{ "id": self.id,
                "user_from_id": self.comment_text,
                "author_id": self.author_id,
                "user_id": self.user_id
        }


class Medias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media_type = db.Column(db.Enum('video', 'image', 'sounds', name='media_type'), unique=True, nullable=False)
    url = db.Column(db.String, unique=False, nullable=False) 
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id')) 
    post_to = db.relationship('Posts', foreign_keys=[post_id])    

    def __repr__(self):
        return f'medias{self.medias_type}'

    def serialize(self):
        return{ "id":self.id,
                "medias_type":self.medias_type,
                "url":self.url,
                "post_id":self.post_id

    }  


""" StarWars Models """ 

class Characters(db.Model):
    __tablename__ = "characters"
    usid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return f'<characters {self.name}>'

    def serialize(self): 
        return{
            "usid": slef.usid,
            "name": self.name 
        }

class CharactersDetails(db.Model):
    __tablename__ = "characters_details"
    usid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    gender = db.Column(db.String, unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    eye_color = db.Column(db.String, unique=False, nullable=False)
    hair_color = db.Column(db.String, unique=False, nullable=False)
    transport = db.Column(db.String, unique=False, nullable=False)
    planet_origin = db.Column(db.Integer, db.ForeignKey('planets.usid'))
    planet_to = db.relationship('Planets', foreign_keys=[planet_origin], backref=db.backref('planet_origin', lazy='select') )
    character_id = db.Column(db.Integer, db.ForeignKey('characters.usid'), unique=True)
    characters_to = db.relationship('Characters', foreign_keys=[character_id], backref=db.backref('characters_to', lazy='select'))

    def __repr__(self):
        return f'<Character {self.name} - {self.planet_origin}>'

    def serialize(self):
        return{ "usid":self.usid,
                "name":self.name,
                "gender":self.gender,
                "height":self.height,
                "eye_color":self.eye_color,
                "hair_color":self.hair_color,
                "transport":self.transport,
                "planet_origin":self.planet_origin,
        }

class Planets(db.Model):
    __tablename__= "planets"
    usid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return f'<Planets{self.usid}>'

    def serialize(self):
        return{
                "usid":self.usid,
                "name":self.name,
        }


class PlanetsDetails(db.Model):
    __tablename__ = "planet_details"
    usid = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String, unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    orbital_period = db.Column(db.Integer, unique=False, nullable=False)
    gravity = db.Column(db.String, unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    climate = db.Column(db.String, unique=False, nullable=False)
    terrain = db.Column(db.String, unique=False, nullable=False)
    surface_water = db.Column(db.Integer, unique=False, nullable=False)
    created = db.Column(db.Integer, unique=False, nullable=False)
    edited = db.Column(db.Integer, unique=False, nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.usid'), unique=True)
    planet_to = db.relationship('Planets', foreign_keys=[planet_id], backref=db.backref('planet_to', lazy='select'))

    def __repr__(self):
        return f'<Planet{self.planet_name}>'

    def serialize(self):
        return{
            "usid":self.usid,
            "planet_name":self.planet_name,
            "diameter":self.diameter,
            "orbital_period":self.orbital_period,
            "gravity":self.gravity,
            "population":self.population,
            "climate":self.climate,
            "terrain":self.terrain,
            "surface_water":self.surface_water,
            "created":self.created,
            "edited":self.edited,
        }

class Starships(db.Model):
    __tablename__="starships"
    usid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return f'<Starships{self.usid}>'

    def serialize(self):
        return{
                "usid":self.usid,
                "name":self.name,
        }



class StarshipsDetails(db.Model):
    __tablename__ = "starship_detail"
    usid = db.Column(db.Integer, primary_key=True)
    starship_name = db.Column(db.String, unique=False, nullable=False)
    starship_model = db.Column(db.String, unique=False, nullable=False)
    starship_class = db.Column(db.String, unique=False, nullable=False)
    manufacturer = db.Column(db.String, unique=False, nullable=False)
    cost_in_credits = db.Column(db.Integer, unique=False, nullable=False)
    length = db.Column(db.Integer, unique=False, nullable=False)
    crew = db.Column(db.Integer, unique=False, nullable=False)
    passengers = db.Column(db.Integer, unique=False, nullable=False)
    max_atmosphering_speed = db.Column(db.String, unique=False, nullable=False)
    hyperdrive_rating = db.Column(db.Integer, unique=False, nullable=False)
    mglt = db.Column(db.Integer, unique=False, nullable=False)
    cargo_capacity = db.Column(db.Integer, unique=False, nullable=False)
    consumables = db.Column(db.String, unique=False, nullable=False)
    created = db.Column(db.Integer, unique=False, nullable=False)
    edited = db.Column(db.Integer, unique=False, nullable=False)
    pilot = db.Column(db.String, unique=False, nullable=False)
    starship_id = db.Column(db.Integer, db.ForeignKey('starships.usid'), unique=True)
    starship_to = db.relationship('Starships', foreign_keys=[starship_id], backref=db.backref('starship_to', lazy='select'))
    
    def __repr__(self):
        return f'<Starship{self.starship_name}>'

    def serialize(self):
        return{
            "usid":self.usid,
            "starship_name":self.starship_name,
            "starship_model":self.starship_model,
            "starship_class":self.starship_class,
            "manufacturer":self.manufacturer,
            "cost_in_credits":self.cost_in_credits,
            "length":self.length,
            "crew":self.crew,
            "passengers":self.passengers,
            "max_atmosphering_speed":self.max_atmosphering_speed,
            "hyperdrive_rating":self.hyperdrive_rating,
            "mglt":self.mglt,
            "consumables":self.consumables,
            "created":self.created,
            "pilot":self.pilot,
        }