from flask import Flask, request, render_template_string, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_caching import Cache
import edgedb


class SchoolForm(FlaskForm):
    name = StringField('School Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    town = StringField('Town', validators=[DataRequired()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Aizen123'
app.config['CACHE_TYPE'] = 'SimpleCache'  
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Default cache timeout in seconds chose 300 to be safe

cache = Cache(app)

client = edgedb.create_client()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anxend Interview Mini Project</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>.city-img { cursor: pointer; width: 100%; }</style>
   <style>
        .city-img-wrapper {
            position: relative;
            width:200px;
            height: 100px; 
            overflow: hidden;
            margin-bottom: 15px;
        }
        .city-img {
            width: 200px;
            height: 100px;
            transition: opacity 0.5s ease;
            object-fit: cover;
        }
        .city-name {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background: rgba(0, 0, 0, 0.5);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0;
            transition: opacity 0.5s ease;
        }
        .city-img-wrapper:hover .city-img {
            opacity: 0.3;
        }
        .city-img-wrapper:hover .city-name {
            opacity: 1;
        }
    </style>


</head>
<body class="grey lighten-3">
<div class="container">
 <h1 class="header center-align">Anxend Interview Mini Project 1</h1>
    <div class="row">
        <div class="col s9">
            <h2 class="header">Add School</h2>
            <form class="col s12" method="post">
                {{ form.hidden_tag() }}
                <div class="input-field col s12">
                    {{ form.name.label }}
                    {{ form.name(class="validate") }}
                </div>
                <div class="input-field col s12">
                    {{ form.address.label }}
                    {{ form.address(class="validate") }}
                </div>
                <div class="input-field col s12">
                    {{ form.town.label }}
                    {{ form.town(class="validate") }}
                </div>
                {{ form.submit(class="btn waves-effect waves-light") }}
            </form>
        </div>
        <div class="col s3">
            <h5>Select Your Town:</h5>
            <div class="city-img-wrapper" onclick="selectCity('Cape Town')">
                <img src="{{ url_for('static', filename='CapeTown.webp') }}" alt="Cape Town" class="city-img">
                <div class="city-name">Cape Town</div>
            </div>
            <div class="city-img-wrapper" onclick="selectCity('London')">
                <img src="{{ url_for('static', filename='London.webp') }}" alt="London" class="city-img">
                <div class="city-name">London</div>
            </div>
            <div class="city-img-wrapper" onclick="selectCity('New York')">
                <img src="{{ url_for('static', filename='NewYork.webp') }}" alt="New York" class="city-img">
                <div class="city-name">New York</div>
            </div>
        </div>
    </div>
    <h2 class="header" id="schools-header">Schools in {{ selected_town or 'Your Town' }}</h2>
    <ul class="collection">
        {% for school in schools %}
            <li class="collection-item">{{ school.name }} - {{ school.address }}</li>
        {% endfor %}
    </ul>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
<script>
    function selectCity(city) {
        window.location.href = `/?town=${encodeURIComponent(city)}`;
    }
</script>
</body>
</html>
"""

def get_cache_key(town):
    """Generates a unique cache key based on the town name."""
    return f"school_data_{town}"


@app.route('/', methods=['GET', 'POST'])
def school_form():
    form = SchoolForm()
    selected_town = request.args.get('town', '')

    if form.validate_on_submit():
        # Invalidate cache for this town
        cache_key = get_cache_key(selected_town)
        cache.delete(cache_key)
        
        # Insert new school data into th db
        client.query("""
            INSERT School {
                name := <str>$name,
                address := <str>$address,
                town := <str>$town
            };
        """, name=form.name.data, address=form.address.data, town=form.town.data)
        return redirect(url_for('school_form', town=selected_town))

    cache_key = get_cache_key(selected_town)
    schools = cache.get(cache_key)

    if schools is None:
        # Fetch data from the database if not cached already
        schools_query = client.query("""
            SELECT School {
                name,
                address
            } FILTER .town ILIKE <str>$town;
        """, town=selected_town)

        # Convert EdgeDB results to a list of dictionaries for caching
        schools = [{'name': school.name, 'address': school.address} for school in schools_query]
        cache.set(cache_key, schools)  # Cache the converted result

    return render_template_string(HTML_TEMPLATE, form=form, schools=schools, selected_town=selected_town)

if __name__ == '__main__':
    app.run(debug=True)
