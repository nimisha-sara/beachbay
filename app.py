from flask import Flask, render_template, request, redirect
import pandas as pd
from csv import DictWriter

app = Flask(__name__)

def sport_desc(sport):
    if sport == "Snorkelling":
        description = "Snorkeling is swimming along the surface of the water and enjoying the underwater world equipped with a mask (or googles), a snorkel (a shaped breathing tube), and usually swim fins (or flippers). The mask allows having a clear vision underwater, the snorkel to breathe with the face submerged by water, and the swim fins to move with less effort and more control. \nSnorkeling does not require any special training, major expenses, or strong physical effort. It allows us to see the beauty of the underwater world, and like any water-based exercise, also provides amazing health benefits. If you like taking pictures, snorkeling is also an amazing opportunity to take epic underwater shots or marine life. For that, all you’ll need is a waterproof camera."
    elif sport == "Scuba Diving":
        description = "Scuba diving is mainly done for the attraction of the unattainable undersea world.  It is one area of nature that mankind has not been able to fully control, we simply are not able to breathe underwater.  Hence, scuba diving gives us an opportunity to be in that underwater world, even if it is just for a limited amount of time. \nOf course, the underwater world is beautiful as well, with many people opting for scuba diving in Asia or scuba diving in the Red Sea or the Great Barrier Reef, said to be some of the world’s best scuba diving locations.  The different colors and marine wildlife are so impressive in all these locations that people find themselves returning over and over again."
    elif sport == "Parasailing":
        description = "Parasailing is a sport where one person or multiple people are towed through the air behind a vehicle while attached to a device similar to a parachute, which catches the wind like a kite and lifts the participants into the air. Most parasailing occurs over water, with a large speedboat providing propulsion, but cars and trucks can also be used to parasail over land. The trailers are attached to the parasail via a harness, and the parasail, in turn, is connected to the anchor vehicle by a tow rope. Traditionally, parasailing involves either one or two parasailing, but there can also be accommodated on certain occasions."
    elif sport == "Jet Skiing":
        description = "Many of us likely had an introduction to the thrills of jet skiing whilst on holiday, but it’s not just the beaches of the Caribbean or some other exotic location that are the places to go. Jet skiing is a high speed water sport that is great for developing your balance and coordination skills as well as your leg muscles. There are many great locations where you can get a great introduction to jet skiing. Of all the water sports, jet skiing is probably the easiest to pick up. It’s also probably the fastest, and it’s the adrenaline attached to that speed that attracts thousands of people to the sport. \nEven if you have jet skied before, it’s worth doing it to ensure you have the skills to ride safely. But it’s not just for safety reasons; more and more launch sites are now demanding you have the certificate before allowing you to gain access to the water."
    return description

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
    beaches_df = pd.read_csv('data/beaches.csv')
    sports_df = pd.read_csv('data/sports.csv')
    beach = beaches_df['name'][int(request.form.get('beach'))]
    sport = request.form.get('sport')
    desc = sport_desc((sport))

    data = sports_df[(sports_df.sport_name==sport)&(sports_df.beach_name==beach)]
    beach_id = list(data['Unnamed: 0'])
    return render_template('sport.html', data=[sport, desc, beach_id, data, beach])

@app.route("/add" , methods=['GET', 'POST'])
def add():
    sports_df = pd.read_csv('data/sports.csv')
    
    sid = len(sports_df['sport_name'])
    name = request.form.get('beach').split(' in ')
    beach_name = name[1]
    sport_name = name[0]
    organizer_name = request.form.get('name')
    time = request.form.get('time')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    cost = request.form.get('cost')

    data2 = {
        "": sid,
        "sport_name": sport_name,
        "beach_name": beach_name,
        "organizer_name": organizer_name,
        "phone": mobile,
        "email": email,
        "timings": time,
        "cost": cost,
        "user_name": "Anonymous"
    }

    headersCSV = ['','sport_name','beach_name','organizer_name','phone','email','timings','cost','user_name']   

    with open('data/sports.csv', 'a', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        dictwriter_object.writerow(data2)
        f_object.close()

    # sports_df.append(data2, ignore_index=True)
    # del sports_df['Unnamed: 0']
    # sports_df.to_csv('data/sports.csv')

    beaches_df = pd.read_csv('data/beaches.csv')
    sports_df = pd.read_csv('data/sports.csv')
    
    print(sport_name, "\n==================\n")
    desc = sport_desc((sport_name))

    data = sports_df[(sports_df.sport_name==sport_name)&(sports_df.beach_name==beach_name)]
    beach_id = list(data['Unnamed: 0'])
    return render_template('sport.html', data=[sport_name, desc, beach_id, data, beach_name])

if __name__=="__main__":
    app.run(debug=True, use_reloader=True)