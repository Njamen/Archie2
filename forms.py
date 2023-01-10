import re
from datetime import datetime
from flask_wtf import FlaskForm as Form
from enums import Genre, State
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
    FileField
)
from wtforms.validators import (
    DataRequired,
    AnyOf,
    URL
)




def is_valid_phone(number):
    regex = re.compile('^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
    return regex.match(number)



class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
         choices = State.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices= Genre.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

    website_link = StringField(
        'website_link'
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if not is_valid_phone(self.phone.data):
            self.phone.errors.append('Invalid phone.')
            return False
        if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
            self.genres.errors.append('Invalid genres.')
            return False
        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append('Invalid state.')
            return False
        return True



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices = State.choices()
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices = Genre.choices()
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
     )

    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if not is_valid_phone(self.phone.data):
            self.phone.errors.append('Invalid phone.')
            return False
        if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
            self.genres.errors.append('Invalid genres.')
            return False
        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append('Invalid state.')
            return False
        return True

# class ShowForm(Form):
#     artist_id = StringField(
#         'artist_id'
#     )
#     venue_id = StringField(
#         'venue_id'
#     )
#     start_time = DateTimeField(
#         'start_time',
#         validators=[DataRequired()],
#         default= datetime.today()
#     )

class ActivityForm(Form):

    serv  = SelectField(
        'service', validators=[DataRequired()]
    )    

    def __init__(self, services):
        Form.__init__(self) 
        self.serv.choices = services
    
    service_id = StringField(
        'service_id',  validators=[DataRequired()]
    )

    name = StringField(
        'name', validators=[DataRequired()]
    )
            






class ServiceForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )


class FichierForm(Form):

    act  = SelectField(
        'Activity', validators=[DataRequired()]
    )    

    def __init__(self, activities):
        Form.__init__(self) 
        self.act.choices = activities

    name = StringField(
        'name', validators=[DataRequired()]
    )

    # url =   StringField(
    #     'url', validators=[DataRequired()]
    # )

    file = FileField('select File')

    activity_id = StringField(
        'service_id',  validators=[DataRequired()]
    )