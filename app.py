from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

@app.route("/")
def main():
    df = pd.read_csv('data/countries.csv')
    countries = list(df['name'])
    return render_template("home.html", countries=countries)

@app.route('/link_redirect/<path:url>')
def link_redirect(url):
    print(url, "\n\n")
    return redirect(url, code=302)

@app.route("/beach_choice" , methods=['GET', 'POST'])
def beach_choice():
    select = request.form.get('country')
    beaches = pd.read_csv('data/beaches.csv')
    beaches = beaches[(beaches.country==select)].to_dict()
    beach_id = list(beaches['id'])
    df = pd.read_csv('data/countries.csv')
    desc = list(df[(df.name=='India')]['description'])[0]
    return render_template("test.html", data=[beach_id, beaches, desc]) # just to see what select is

@app.route("/sport" , methods=['GET', 'POST'])
def sport():
    beach = request.form.get('beach')
    sport = request.form.get('sport')
    if sport == "Snorkelling":
        desc = "Snorkeling is swimming along the surface of the water and enjoying the underwater world equipped with a mask (or googles), a snorkel (a shaped breathing tube), and usually swim fins (or flippers). The mask allows having a clear vision underwater, the snorkel to breathe with the face submerged by water, and the swim fins to move with less effort and more control. \nSnorkeling does not require any special training, major expenses, or strong physical effort. It allows us to see the beauty of the underwater world, and like any water-based exercise, also provides amazing health benefits. If you like taking pictures, snorkeling is also an amazing opportunity to take epic underwater shots or marine life. For that, all you’ll need is a waterproof camera."
    elif sport == "Scuba Diving":
        desc = "Scuba diving is mainly done for the attraction of the unattainable undersea world.  It is one area of nature that mankind has not been able to fully control, we simply are not able to breathe underwater.  Hence, scuba diving gives us an opportunity to be in that underwater world, even if it is just for a limited amount of time. \nOf course, the underwater world is beautiful as well, with many people opting for scuba diving in Asia or scuba diving in the Red Sea or the Great Barrier Reef, said to be some of the world’s best scuba diving locations.  The different colors and marine wildlife are so impressive in all these locations that people find themselves returning over and over again."
    elif sport == "Parasailing":
        desc = "Parasailing is a sport where one person or multiple people are towed through the air behind a vehicle while attached to a device similar to a parachute, which catches the wind like a kite and lifts the participants into the air. Most parasailing occurs over water, with a large speedboat providing propulsion, but cars and trucks can also be used to parasail over land. The trailers are attached to the parasail via a harness, and the parasail, in turn, is connected to the anchor vehicle by a tow rope. Traditionally, parasailing involves either one or two parasailing, but there can also be accommodated on certain occasions."
    elif sport == "Jet Skiing":
        desc = "Many of us likely had an introduction to the thrills of jet skiing whilst on holiday, but it’s not just the beaches of the Caribbean or some other exotic location that are the places to go. Jet skiing is a high speed water sport that is great for developing your balance and coordination skills as well as your leg muscles. There are many great locations where you can get a great introduction to jet skiing. Of all the water sports, jet skiing is probably the easiest to pick up. It’s also probably the fastest, and it’s the adrenaline attached to that speed that attracts thousands of people to the sport. \nEven if you have jet skied before, it’s worth doing it to ensure you have the skills to ride safely. But it’s not just for safety reasons; more and more launch sites are now demanding you have the certificate before allowing you to gain access to the water."
    print(sport, beach)
    return render_template('sport.html', data=[sport, desc])


if __name__=="__main__":
    app.run(debug=True)