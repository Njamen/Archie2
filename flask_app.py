
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
import json
from sqlite3 import DatabaseError
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for
)
from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from config import app
from flask_migrate import Migrate
from flask import jsonify
from datetime import (
    datetime,
    timezone
)
from models import db, Venue, Artist, Show

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# app = Flask(__name__)
# moment = Moment(app)
# app.config.from_object('config')
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)


# TODO: connect to a local postgresql database

from models import *


# db.create_all()

# migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/api/test')
def test():



    return render_template('pages/test.html')


@app.route('/alpha')
def hello_world():
    return 'Hello from Flask!'



@app.route('/')
def index():

    max = 10

    all_venue  = Venue.query.with_entities(Venue.id, Venue.name).order_by(desc(Venue.id)).limit(max).all()
    all_artist = Artist.query.with_entities(Artist.id, Artist.name).order_by(desc(Artist.id)).limit(max).all()

    recent_venues = [{
        'id' : venue.id,
        'name': venue.name
    } for venue in all_venue ]

    recent_artists = [{
        'id' : artist.id,
        'name': artist.name
    } for artist in all_artist ]



    return render_template('pages/home.html', venues=recent_venues, artists =recent_artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/fichier/create', methods=['GET'])
def create_fichier_form():
    
    all_activity =  [(
        activity.id  , activity.name       
    ) for activity in  Activite.query.all()] 

    form = FichierForm(all_activity)

    return render_template('forms/new_fichier.html', form=form)


@app.route('/fichier/create', methods=['POST'])
def create_fichier_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    form = FichierForm(request.form)
    try:
        show = Fichier(
            name=form.file.data,
            acivite_id=form.act.data,
            url=""
            # url=form.url.data,
        )

        db.session.add(show)
        db.session.commit()
        flash('File  was successfully upload!')
        db.session.close()
        # return render_template('pages/shows.html')
        return redirect(url_for('shows'))

    except Exception as e:
        db.session.rollback()
        error = True
        print(e)
        flash('An error occurred. show could not be listed.')
        form = FichierForm()
        db.session.close()
        return render_template('forms/new_show.html', form=form)


@app.route('/activity/create', methods=['GET'])
def create_activity_form():

    all_service = [(
        service.id  , service.name       
    ) for service in  Service.query.all()]

    form = ActivityForm(all_service)
    return render_template('forms/new_activity.html', form=form)

@app.route('/activity/create', methods=['POST'])
def create_activity_submission():


    form = ActivityForm(request.form)
    try:

        print(form.serv.data)
        activite = Activite(
            name=form.name.data,
            service_id= form.serv.data,
        )

        db.session.add(activite)
        db.session.commit()
        flash('Activity  was successfully listed!')
        db.session.close()
        # return render_template('pages/shows.html')
        return redirect(url_for('activities'))

    except Exception as e:
        db.session.rollback()
        error = True
        flash('An error occurred. Activity could not be listed.')
        form = ActivityForm()
        db.session.close()
        return render_template('forms/new_activity.html', form=form)


@app.route('/service/create', methods=['GET'])
def create_service_form():
    form = ServiceForm()
    return render_template('forms/new_service.html', form=form)

@app.route('/service/create', methods=['POST'])
def create_service_submission():

    form = ServiceForm(request.form)

    try:
        service = Service(
            name=form.name.data,
        )

        db.session.add(service)
        db.session.commit()
        flash('Service ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')

    except Exception as e:
        db.session.rollback()
        error = True
        print(e)
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        form = VenueForm()
        return render_template('forms/new_service.html', form=form)
    finally:
        db.session.close()


@app.route('/services/search', methods=['POST'])
def search_services():


    search_term = request.form.get('search_term', "")
    pattern = "%{}%".format(search_term)
    found_items = Service.query.filter(Service.name.ilike(pattern)).all()

    data = []
    for service in found_items:
        data.append({
            "id": service.id,
            "name": service.name,
            "activities": [{
                "id": activity.id,
                "name": activity.name,
            } for activity  in service.activities ]
        })

    return render_template('pages/services.html', areas=data)


@app.route('/activities/search', methods=['POST'])
def search_activities():


    search_term = request.form.get('search_term', "")
    pattern = "%{}%".format(search_term)
    found_items = Activite.query.filter(Activite.name.ilike(pattern)).all()


    data = []
    for activity in found_items:
        data.append({
            "id": activity.id,
            "name": activity.name,
            "service": {
                "id": activity.service.id,
                "name": activity.service.name,
            }
        })
    return render_template('pages/activities.html', areas=data)



@app.route('/service/<int:service_id>/activity/<int:activity_id>/fichiers')
def fichers(service_id, activity_id):

    service = Service.query.get_or_404(service_id)
    activite = Activite.query.get_or_404(activity_id)
    fichiers = [it for it in Fichier.query.all() if it.acivite_id == activity_id ]

    data = {
        "id_service" : service.id,
        "name_service" : service.name,
        "id_activite" : activite.id,
        "nom_activite" : activite.name,
        "fichiers" : [{
            "id" : fich.id,
            "name" :fich.name,
            "url" : fich.url
        } for fich in fichiers]
    }

    return render_template('pages/fichiers.html', areas=data)



@app.route('/activities')
def activities():

    all_service = Activite.query.all()

    data = []
    for activity in all_service:
        data.append({
            "id": activity.id,
            "name": activity.name,
            "service": {
                "id": activity.service.id,
                "name": activity.service.name,
            }
        })


    return render_template('pages/activities.html', areas=data)




@app.route('/services')
def services():

    all_service = Service.query.all()

    data = []
    for service in all_service:
        data.append({
            "id": service.id,
            "name": service.name,
            "activities": [{
                "id": activity.id,
                "name": activity.name,
            } for activity  in service.activities ]
        })

    return render_template('pages/services.html', areas=data)




@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

    all_Venue = Venue.query.all()

    all_city_state = Venue.query.with_entities(
        Venue.city, Venue.state).distinct().all()

    data = []
    for city_state in all_city_state:
        data.append({
            "city": city_state.city,
            "state": city_state.state,
            "venues": [{
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(list(filter(lambda it: it.start_time > datetime.now(tz=timezone.utc), venue.shows)))
            } for venue in all_Venue if venue.city == city_state.city and venue.state == city_state.state]
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term', "")
    pattern = "%{}%".format(search_term)
    found_items = Venue.query.filter(Venue.name.ilike(pattern)).all()
    current_time = datetime.now(tz=timezone.utc)

    response = {
        "count": len(found_items),
        "data": [{
            "id": it.id,
            "name": it.name,
            "num_upcoming_shows": len(list(filter(lambda x: x.start_time > current_time, it.shows))),
        } for it in found_items]
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    venue = Venue.query.get_or_404(venue_id)
    past_shows = []
    upcoming_shows = []

    for show in venue.shows:
        temp_show = {
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        }
        if show.start_time <= datetime.now(tz=timezone.utc):
            past_shows.append(temp_show)
        else:
            upcoming_shows.append(temp_show)

    data = vars(venue)
    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    form = VenueForm(request.form)

    try:

        venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            genres=form.genres.data,
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
            website=form.website_link.data,
            seeking_talent=form.seeking_talent.data,
            seeking_description=form.seeking_description.data
        )

        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')

    except Exception as e:
        db.session.rollback()
        error = True
        print(e)
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)
    finally:
        db.session.close()

    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash('Venue  was successfully deleted!')
        return redirect(url_for('venues'))
    except Exception as e:
        db.session.rollback()
        error = True
        print(e)
        flash('An error occurred. Venue  could not be deleted.')
        return redirect(url_for('show_venue', venue_id=venue_id))
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    # return None

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database

    all_artist = Artist.query.with_entities(Artist.id, Artist.name).all()

    data = [dict(v) for v in all_artist]

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get('search_term', "")
    pattern = "%{}%".format(search_term)
    found_items = Artist.query.filter(Artist.name.ilike(pattern)).all()
    current_time = datetime.now(tz=timezone.utc)

    response = {
        "count": len(found_items),
        "data": [{
            "id": it.id,
            "name": it.name,
            "num_upcoming_shows": len(list(filter(lambda x: x.start_time > current_time, it.shows))),
        } for it in found_items]
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id

    artist = Artist.query.get_or_404(artist_id)

    past_shows = []
    upcoming_shows = []

    for show in artist.shows:
        temp_show = {
            'venue_id': show.artist_id,
            'venue_name': show.artist.name,
            'venue_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        }
        if show.start_time <= datetime.now(tz=timezone.utc):
            past_shows.append(temp_show)
        else:
            upcoming_shows.append(temp_show)

    data = vars(artist)
    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    artist = Artist.query.get(artist_id)

    form.name.data = artist.name
    form.city.data = artist.city
    form.phone.data = artist.phone
    form.image_link.data = artist.image_link
    form.facebook_link.data = artist.facebook_link
    form.website_link.data = artist.website
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
    # form.genres.data = ['Alternative','Blues']
    # form.state.data =  "ID"

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    form = ArtistForm(request.form)
    try:
        artist = Artist.query.get(artist_id)

        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.genres = form.genres.data
        artist.facebook_link = form.facebook_link.data
        artist.image_link = form.image_link.data
        artist.website = form.website_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data

        db.session.commit()
        flash('Artist  was successfully updated!')
        return redirect(url_for('show_artist', artist_id=artist_id))

    except Exception as e:
        db.session.rollback()
        error = True
        print(e)
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be updated.')
        form = ArtistForm()
        return render_template('forms/edit_artist.html', form=form, artist=artist)
    finally:
        db.session.close()


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

    form = VenueForm()

    venue = Venue.query.get(venue_id)

    form.name.data = venue.name
    form.city.data = venue.city
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.image_link.data = venue.image_link
    form.facebook_link.data = venue.facebook_link
    form.website_link.data = venue.website
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    # form.genres.data = [2,3]
    # form.state.default =  "ID"



    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    form = VenueForm(request.form)

    try:
        venue = Venue.query.get(venue_id)

        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.genres = form.genres.data
        venue.facebook_link = form.facebook_link.data
        venue.image_link = form.image_link.data
        venue.website = form.website_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data

        db.session.commit()
        # db.session.close()
        flash('Venue  was successfully updated!')
        # return render_template('pages/home.html')
        return redirect(url_for('show_venue', venue_id=venue_id))

    except Exception as e:
        db.session.rollback()
        error = True
        print("ERRor: ")
        print(e)
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be updated.')
        form = VenueForm()

        return render_template('forms/edit_venue.html', form=form, venue=venue)
        # return redirect(url_for('show_venue', venue_id=venue_id))

    finally:
        db.session.close()


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

    form = ArtistForm(request.form)
    try:

        artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            genres=form.genres.data,
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
            website=form.website_link.data,
            seeking_venue=form.seeking_venue.data,
            seeking_description=form.seeking_description.data
        )

        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        db.session.close()
        return render_template('pages/home.html')

    except Exception as e:
        db.session.rollback()
        error = True
        print(e)
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        form = ArtistForm()
        db.session.close()
        return render_template('forms/new_artist.html', form=form)

    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.

    all_shows = Show.query.all()

    data = [{
        "venue_id": it.venue_id,
        "venue_name": it.venue.name,
        "artist_id": it.artist_id,
        "artist_name": it.artist.name,
        "artist_image_link": it.artist.image_link,
        "start_time": "{}".format(it.start_time)
    } for it in all_shows
    ]

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    form = ShowForm(request.form)
    try:
        show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data,
        )

        db.session.add(show)
        db.session.commit()
        flash('show  was successfully listed!')
        db.session.close()
        # return render_template('pages/shows.html')
        return redirect(url_for('shows'))

    except Exception as e:
        db.session.rollback()
        error = True
        print(e)
        flash('An error occurred. show could not be listed.')
        form = ShowForm()
        db.session.close()
        return render_template('forms/new_show.html', form=form)

    # on successful db insert, flash success
    # flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    # return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:

location = os.getenv("FLASK_ENV","development")
if location == "development":
    if __name__ == '__main__':
        app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
