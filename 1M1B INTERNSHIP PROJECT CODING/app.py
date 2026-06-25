from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "soilproject"

feedbacks = []


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "1234":
        session['user'] = username
        return redirect(url_for('home'))

    return "Invalid Username or Password"


@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')

    return render_template('index.html')


def recommend_crop(n, p, k, ph):
    if 6.0 <= ph <= 8.0:
        if n > 80:
            return "Rice"
        elif p > 50:
            return "Wheat"
        elif k > 45:
            return "Sugarcane"
        else:
            return "Maize"
    return "Cotton"


def recommend_soil(ph):
    if ph < 6:
        return "Acidic Soil"
    elif ph < 7.5:
        return "Loamy Soil"
    elif ph < 8:
        return "Clay Soil"
    else:
        return "Alkaline Soil"


def recommend_irrigation(crop):
    irrigation = {
        "Rice": "Flood Irrigation",
        "Wheat": "Sprinkler Irrigation",
        "Sugarcane": "Drip Irrigation",
        "Maize": "Sprinkler Irrigation",
        "Cotton": "Drip Irrigation"
    }
    return irrigation.get(crop, "General Irrigation")


def recommend_fertilizer(crop):
    fertilizers = {
        "Rice": "Urea + DAP",
        "Wheat": "NPK (20:20:20)",
        "Sugarcane": "Potash Rich Fertilizer",
        "Maize": "Nitrogen Fertilizer",
        "Cotton": "Organic Compost + NPK"
    }
    return fertilizers.get(crop, "Organic Compost")


def organic_recommendation():
    return """
Vermicompost
Farm Yard Manure (FYM)
Neem Cake
Green Manure
Biofertilizers
"""


@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect('/')

    n = float(request.form['nitrogen'])
    p = float(request.form['phosphorus'])
    k = float(request.form['potassium'])
    ph = float(request.form['ph'])

    crop = recommend_crop(n, p, k, ph)
    soil = recommend_soil(ph)
    irrigation = recommend_irrigation(crop)
    fertilizer = recommend_fertilizer(crop)
    organic = organic_recommendation()

    return render_template(
        'result.html',
        crop=crop,
        soil=soil,
        irrigation=irrigation,
        fertilizer=fertilizer,
        organic=organic,
        nitrogen=n,
        phosphorus=p,
        potassium=k,
        ph=ph
    )


@app.route('/feedback')
def feedback():
    if 'user' not in session:
        return redirect('/')

    return render_template('feedback.html')


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    message = request.form['message']

    feedbacks.append({
        'name': name,
        'message': message
    })

    return render_template('thankyou.html', name=name)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)