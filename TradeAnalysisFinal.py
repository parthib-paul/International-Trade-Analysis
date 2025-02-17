import pandas as pd
from flask import Flask, render_template, render_template_string, request, redirect, url_for
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import base64
from io import BytesIO
from matplotlib.figure import Figure

df = pd.read_csv("Final/global_combined_no_na.csv")
df_cleaned = df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"])
# print(df_cleaned[130:160])
# df_cleaned.loc[df_cleaned["Country"] == "Korea, Rep.", "Country"] = "South Korea"
# print(df_cleaned[130:160])
df_cleaned.loc[:,'trade_balance'] = df_cleaned['trade_balance'].mul(1_000)
unique_countries = df_cleaned["Country"].unique()

app = Flask("My first app")
my_data = {}

global_dict = {"country": "", "level": "", "prediction": ""}

@app.route('/')
def welcome_page():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Economic Trade Analysis</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <style>
            @keyframes slide {
                0% { transform: translateX(100%); }
                100% { transform: translateX(-100%); }
            }
            .ticker {
                white-space: nowrap;
                overflow: hidden;
                position: relative;
                background: #f8d210;
                color: #333;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            .ticker span {
                display: inline-block;
                animation: slide 20s linear infinite;
            }
            .cartoon-container {
                text-align: center;
                margin-top: 20px;
            }
            .cartoon img {
                width: 300px;
                height: auto;
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <div class="ticker">
            <span>📈 Bull vs Bear Market! | 🏦 Federal Reserve Interest Rate Adjustments! | 💰 Inflation vs Wage Growth! | 📊 Stock Market Trends | 💸 Economic Recession vs Expansion | 🏛️ Global Trade Agreements in Action!</span>
        </div>
        <div class="container text-center mt-5">
            <div class="header bg-primary text-white p-4 rounded">
                <h1>Welcome to Economic Trade Analysis</h1>
                <p>Explore trade balance predictions and economic insights!</p>
            </div>
            <div class="cartoon-container">
                <img src="https://tse4.mm.bing.net/th?id=OIF.MaJaNl6ynj9cRpmpHQqEHg&pid=Api" alt="Trump Tariff Cartoon" class="cartoon">
            </div>
            <a href="/analysis" class="btn btn-success mt-4">Explore Trade Analysis</a>
            <a href="/model" class="btn btn-warning mt-4">Run Economic Model</a>
        </div>
    </body>
    </html>
    ''')
    # return welcome_message

variables_to_compare = ["CPI", "GDP", "unemployment", "exports", "imports", "interest_rate", "exchange_rate"]

@app.route('/analysis')
def analysis_page():
    response = ""
    response += "<h1>ANALYSIS OF HISTORICAL DATA</h1>"
    response += "<br>"
    response += "<b>What is a trade balance? </b>"
    response += "<br>"
    response += "A trade balance is the difference between the monetary value of a nation's exports and imports of goods over a certain time period with a specific country (Wikipedia)."
    response += "<br>"
    response += "A country has a <b>trade deficit</b> when the value of imported goods is larger than the value of its exports."
    response += "<br>"
    response += "A country has a <b>trade surplus</b> when the value of exported goods is larger than the value of its imports."
    response += "<br>"
    response += "<br>"
    response += "<b>The perspective: </b>"
    response += "<br>"
    response += "The US is considered to be the <i>home</i> country. In this analysis, the US's historic trade levels with its major trading partners are evaluated."
    response += "<br>"
    response += "<br>"
    response += "<b>Figure 1</b>"
    # Tariff % vs Trade Balance
    plt.figure(figsize=(10, 6))
    for country in unique_countries:
        country_data = df_cleaned[df_cleaned["Country"] == country]
        plt.scatter(country_data["tariff%"], country_data["trade_balance"], label=country, alpha=0.6)
    plt.xlabel("Tariff rate, weighted mean on all traded products (%)")
    # New line
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x/1e9)}'))  # Converts values to "B" (billion) format
    plt.ylabel("Trade Balance (Billions USD)")
    plt.title("Tariff vs Trade Balance")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    response += f"<img src='data:image/png;base64,{data}'/>"
    response += "<br>"
    response += "Each datapoint in <u>Figure 1</u> represents the <b>US trade balance</b> with a specific country in a given year, along with the <b>tariff rate</b> imposed by the US on imports from that country. "
    response += "Most of the datapoints are clustered together around an area which represents the US imposing a low tariff rate and the US having a relatively low trade deficit. "
    response += "The combination of all of the datapoints together loosely take on the shape of <b>logarithmic growth</b>. "
    response += "This relationship between tariff rate and trade balance can be interpretted as follows: <u>Initially, as the tariff rate rises, the trade deficit shrinks sharply. However, beyond a certain threshold, the trade balance becomes less sensitive to further tariff increases.</u> "
    response += "This occurs because when the US imposes higher tariffs on a trading partner, imports from that country become more expensive, reducing demand and consumption for tariffed goods."
    response += "<br>"
    response += "<br>"
    response += "It appears that the US has consistently imposed a low tariff and had a low trade deficit with <b>Canada</b>, <b>Germany</b>, <b>Japan</b>, <b>South Korea</b>, <b>India</b>, and <b>Ireland</b>. "
    response += "Despite the US imposing a higher tariff level on <b>Brazil</b> than the previously mentioned countries, the US's historic trade balance with Brazil has been the highest of any relationship. "
    response += "The US's tariff rate and trade balance with <b>Mexico</b> has varied a bit, altogether following a positive, linear shape. "
    response += "The trading partner with the most variation in tariff rates and trade balance is <b>China</b>, which exhibits the highest tariff rates and largest trade deficit. As shown in the graph, the data points for China follow a logarithmic pattern. "
    response += "<br>"
    response += "<br>"

    # Tariff % over the years
    response += "<b>Figure 2</b>"
    plt.figure(figsize=(12, 6))
    for country in unique_countries:
        country_data = df_cleaned[df_cleaned["Country"] == country]
        plt.plot(country_data["Year"], country_data["tariff%"], label=country)
    plt.xlabel("Year")
    plt.ylabel("Tariff rate, weighted mean on all traded products (%)")
    plt.title("Tariff Rate Across Time")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    response += f"<img src='data:image/png;base64,{data}'/>"
    response += "<br>"
    response += "<u>Figure 2</u> demonstrates the US imposed tariffs on its major trading partners across time. "
    response += "As seen, the amount of historical tariff data varies by country. "
    response += "It appears that the highest tariff implementation rate in recent history was above 30% and imposed upon <b>China</b> in the 90s. "
    response += "Since 2005, the tariff rates imposed on the US's major trading partners have settled to below 10%. "
    response += "However, beginning in 2021, there have been large increases in tariff rates on <b>India</b>, <b>South Korea</b>, <b>Mexico</b>, and <b>China</b>. "
    response += "<br>"
    response += "<br>"

    # Tariff vs GDP
    response += "<b>Figure 3</b>"
    plt.figure(figsize=(10, 6))
    for country in unique_countries:
        country_data = df_cleaned[df_cleaned["Country"] == country]
        plt.scatter(country_data["tariff%"], country_data["GDP"], label=country, alpha=0.6)
    plt.xlabel("Tariff rate, weighted mean on all traded products (%)")
    plt.ylabel("GDP per capita (USD)")
    plt.title("Tariff vs GDP per capita")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    response += f"<img src='data:image/png;base64,{data}'/>"
    response += "<br>"
    response += "Each data point in this visualization represents the  <b>GDP per capita</b> of a US trading partner and <b>tariff rate</b> imposed by the US that year. "
    response += "The data exhibits a pattern of <b>exponential decay</b>, meaning that as a country's GDP per capita decreases, the tariff rate imposed by the US tends to increase, following an asymptotic trend. "
    response += "A lower GDP per capita is often linked to lower labor costs, resulting in cheaper goods. "
    response += "To counteract these low prices, tariffs are often imposed to make imported goods more expensive, reducing their appeal to domestic consumers. "
    response += "<br>"
    response += "<br>"
    
    # Trade Balance over the years
    response += "<b>Figure 4</b>"
    plt.figure(figsize=(12, 6))
    for country in unique_countries:
        country_data = df_cleaned[df_cleaned["Country"] == country]
        plt.plot(country_data["Year"], country_data["trade_balance"], label=country)
    plt.xlabel("Year")
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x/1e9)}'))
    plt.ylabel("Trade Balance (Billions USD)")
    plt.title("Trade Balance Across Time")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    response += f"<img src='data:image/png;base64,{data}'/>"
    response += "<br>"
    response += "<u>Figure 4</u> illustrates that the US's trade deficits with most of its major trading partners have been <b>relatively steady</b> in the recent past. "
    response += "Notably, the only country the US has had a trade surplus with during this time period is <b>Brazil</b>. "
    response += "Most of the trade deficits with major trading partners have remained above 100 billion USD, excluding <b>China</b>. "
    response += "The US's trade deficit with <b>China</b> multiplied in size from the 90s to 2016. "
    response += "This deficit shrunk during Trump's presidency (2016-2020) yet returned to growing during the Biden administration. "
    response += "<br>"
    response += "<br>"

    # Trade Balance vs interest rate
    response += "<b>Figure 5</b>"
    plt.figure(figsize=(10, 6))
    for country in unique_countries:
        country_data = df_cleaned[df_cleaned["Country"] == country]
        plt.scatter(country_data["interest_rate"], country_data["trade_balance"], label=country, alpha=0.6)
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x/1e9)}'))
    plt.ylabel("Trade Balance (Billions USD)")
    plt.xlabel("Interest Rate")
    plt.title("Trade Balance vs Interest Rate")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    response += f"<img src='data:image/png;base64,{data}'/>"
    response += "<br>"
    response += "Similar to <u>Figure 1</u>, the data in <u>Figure 5</u> exhibit a pattern of <b>logarithmic growth</b>. "
    response += "Upon closer examination, the data appear to form three distinct groupings. "
    response += "The first segment, characterized by a steep slope and an almost linear relationship between trade balance and interest rate, consists of datapoints from <b>China</b>. "
    response += "The second grouping forms a cluster around a relatively small trade defecit and low interest rates, comprised of data from <b>Canada</b>, <b>Mexico</b>, <b>Germany</b>, <b>Japan</b>, <b>South Korea</b>, <b>India</b>, and <b>Ireland</b>. "
    response += "The final section consist of datapoints from <b>Brazil</b>, the trading partner with the smallest trade balance and highest interest rates. "
    response += "One possible explanation for this relationship is that when a country's interest rate rises, it attracts foreign capital seeking higher returns, increasing demand for the currency.  "
    response += "As a result, the currency appreciates relative to the US dollar. "
    response += "A stronger currency makes the country's exports more expensive and US imports cheaper, ultimately reducing the trade deficit. "
    response += "<br>"
    response += "<br>"
    response += "<a href='/'>Return<a>"
    return response

@app.route('/model')
def user_inputs():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Select a Country - Economic Model</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <style>
            body {
                background-color: #f4f4f4;
                font-family: Arial, sans-serif;
            }
            .container {
                max-width: 700px;
                background: white;
                padding: 20px;
                margin-top: 50px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }
            .country-list {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                justify-content: center;
            }
            .country-btn {
                background: linear-gradient(to right, #ff7e5f, #feb47b);
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
                cursor: pointer;
                transition: transform 0.3s, background 0.3s;
                font-weight: bold;
            }
            .country-btn:hover {
                transform: scale(1.1);
                background: linear-gradient(to right, #feb47b, #ff7e5f);
            }
            .fun-fact {
                text-align: center;
                font-style: italic;
                margin-top: 20px;
                color: #555;
            }
            .animated-img {
                display: block;
                margin: 100px auto;
                width: 200px;
                animation: bounce 2s infinite;
            }
            @keyframes bounce {
                0%, 100% {
                    transform: translateY(0);
                }
                50% {
                    transform: translateY(-10px);
                }
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h2>Select a Country</h2>
            <p>Choose a country to analyze its trade balance.</p>
            <img src="https://cdn.pixabay.com/animation/2023/03/20/19/07/19-07-39-28_512.gif" class="animated-img" alt="Animated Money">
            <form action="/process_country" method="post">
                <div class="country-list">
                    <button type="submit" name="country" value="Brazil" class="country-btn">Brazil</button>
                    <button type="submit" name="country" value="Canada" class="country-btn">Canada</button>
                    <button type="submit" name="country" value="China" class="country-btn">China</button>
                    <button type="submit" name="country" value="Germany" class="country-btn">Germany</button>
                    <button type="submit" name="country" value="India" class="country-btn">India</button>
                    <button type="submit" name="country" value="Ireland" class="country-btn">Ireland</button>
                    <button type="submit" name="country" value="Japan" class="country-btn">Japan</button>
                    <button type="submit" name="country" value="Mexico" class="country-btn">Mexico</button>
                    <button type="submit" name="country" value="Korea, Rep." class="country-btn">South Korea</button>
                </div>
            </form>
            <p class="fun-fact">💡 Fun Fact: Despite of the DeepSeek & TikTok war,The United States and China are the world's largest trading partners!</p>
        </div>
    </body>
    </html>
    ''')

global_df = df_cleaned
global_df_dummies = pd.get_dummies(global_df, columns= ['Country'], drop_first= True)
countries = ['Canada',
             'China',
             'Mexico',
             'Germany',
             'Japan',
             'Korea, Rep.',
             'Brazil', 
             'India',
             'Ireland'
             ]
input_cols = ['tariff%',
              'CPI',
              'GDP',
              'unemployment',
              'interest_rate',
              'exchange_rate',
              'Country_Canada',
              'Country_China',
              'Country_Germany',
              'Country_India',
              'Country_Ireland',
              'Country_Japan',
              'Country_Korea, Rep.',
              'Country_Mexico'
              ]
output_col = 'trade_balance'


def get_interesting_fact(country):
    facts = {
        "Canada": "Canada has more lakes than the rest of the world combined!",
        "China": "China is home to the Great Wall, which stretches over 13,000 miles.",
        "Mexico": "Mexico introduced chocolate, chilies, and corn to the world.",
        "Germany": "Germany has over 1,500 different types of sausages!",
        "Japan": "Japan has the world's most vending machines—one for every 23 people.",
        "Korea, Rep.": "South Korea has the fastest internet speed in the world.",
        "Brazil": "Brazil is home to the Amazon Rainforest, which covers 60% of the country.",
        "India": "India has the largest democracy and the famous Taj Mahal.",
        "Ireland": "Ireland has over 30,000 castles!"
    }
    return facts.get(country, "This country has a rich history and vibrant culture!")


@app.route('/level')
def receive_template():
    country = global_dict.get('country', None)
    if not country:
        return "Error: No country selected", 400
    
    tariff_min_max = get_tariff_percent(country)

    # Ensure JSON values are valid
    tariff_labels = [tariff_min_max[0], (tariff_min_max[0] + tariff_min_max[1]) / 2, tariff_min_max[1]] if tariff_min_max else [0, 0, 0]
    trade_balance_values = [1000, 5000, 8000]  # Replace this with real predictions

    return render_template("level.html", 
                           country=country, 
                           tariff_range=tariff_min_max or [0, 0],
                           fun_fact=get_interesting_fact(country),
                           tariff_labels=tariff_labels,
                           trade_balance_values=trade_balance_values)


@app.route('/process_country', methods=['POST'])
def receive_country():
    user_input_country = request.form.get('country')
    
    if not user_input_country:
        return "Error: No country received", 400  # Prevents `None` values
    
    global_dict['country'] = user_input_country  # Store selected country
    return redirect('/level')  # Redirect to tariff input page


def train_model():
    train_df, test_df = train_test_split(global_df_dummies)
    # Initiate model
    model = LinearRegression()
    # Set up the model
    train_X = train_df[input_cols]
    train_Y = train_df[output_col]
    model.fit(train_X, train_Y)
    return model

model = train_model()

def get_tariff_percent(country):
    country_df = global_df[global_df['Country'] == country]
    
    if country_df.empty:  # 🚨 Handle case where no data exists
        return [0, 0]  # Default values
    
    tariff_min = country_df['tariff%'].min()
    tariff_max = country_df['tariff%'].max()
    return [tariff_min, tariff_max]


def make_prediction(country, tariff):
    # Use the previously made model to predict the trade balance value
    # Create a feature vector initialized with zeros
    input_data = pd.DataFrame([0] * len(input_cols), index=input_cols).T

    # Set tariff% value
    input_data['tariff%'] = tariff

    # Set dummy variables for the selected country
    country_col = f'Country_{country}'
    if country_col in input_data.columns:
        # Set selected country to 1 (others remain 0)
        input_data[country_col] = 1  

    # Predict trade balance
    trade_balance = model.predict(input_data)[0]
    return trade_balance



@app.route('/home')
def receive_post():
    tariff_min_max = get_tariff_percent(global_dict['country'])
    statement = ""
    statement += f"<img src='static/{global_dict['country']}_flag.jpg' width='75' height='50' alt='{global_dict['country']} Flag'>"
    statement += "<br>"
    statement += f"Please type in a tariff level in the range of {tariff_min_max[0]}% and {tariff_min_max[1]}%."
    statement += f"<form action='/process_level' method='post'>"
    statement += "<label for='tariff_level'>Tariff Level: </label>"
    statement += "<input type='text' id='tariff_level' name='tariff_level'>"
    statement += "<input type='submit'>"
    statement += "</form>"
    statement += "<br>"
    statement += "<a href='/model'>Return<a>"
    statement += "<br>"
    return statement

@app.route('/process_level', methods=['POST'])
def receive_level():
    print(request.form)
    tariff_level = request.form.get('tariff_level')

    if tariff_level is None or tariff_level == "":
        return "Error: No tariff level received", 400  # Prevents errors from empty input

    try:
        tariff_level = float(tariff_level)  # Convert to float
    except ValueError:
        return "Error: Invalid tariff level", 400  # Prevents non-numeric input

    min_tariff, max_tariff = get_tariff_percent(global_dict['country'])

    if min_tariff <= tariff_level <= max_tariff:
        global_dict['level'] = tariff_level
        global_dict['prediction'] = make_prediction(global_dict['country'], tariff_level)
        return redirect(f'/profile/{global_dict["country"]}')  # ✅ Redirect correctly
    else:
        return redirect("/try_again")  # ✅ If out of range, ask again


@app.route('/try_again')
def try_again():
    response = ""
    response += "Invalid input. Please try again."
    response += "<br>"
    response += "<a href='/level'>Return<a>"
    return response


@app.route('/profile/<country>')
def country_page(country):
    request = ""
    if global_dict["country"] == 'Korea, Rep.':
        south_korea = 'South Korea'
        request += f"<h1>{south_korea}</h1>"
    else:
        request += f"<h1>{global_dict['country']}</h1>"
    before_res = int(global_dict["prediction"])
    res = "{:,}".format(before_res)
    request += f"The US's predicted trade balance with {global_dict['country']} when the tariff is {global_dict['level']}% on imports is {res} (USD)."    
    request += "<br>"
    if global_dict['prediction'] < 0:
        request += f"Since the trade balance is negative, the U.S. is importing more than they are exporting to {global_dict['country']}."
    elif global_dict['prediction'] > 0:
        request += f"Since the trade balance is positive, the U.S. is exporting more than they are importing from {global_dict['country']}."
    else:
        request += f"Since the trade balance is zero, the U.S. is importing the same amount as they are exporting with {global_dict['country']}."
    request += "<br>"
    plt.figure(figsize=(10, 6))
    country_data = df_cleaned[df_cleaned["Country"] == global_dict['country']]
    plt.scatter(country_data["tariff%"], country_data["trade_balance"], label=country, alpha=0.6)
    new_x = float(global_dict["level"])
    new_y = float(global_dict["prediction"])
    plt.scatter(new_x, new_y, color='red', marker='x')
    plt.text(new_x,new_y,"Model Prediction")
    plt.xlabel("Tariff rate, weighted mean on all traded products (%)")
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x/1e9)}'))  # Converts values to "B" (billion) format
    plt.ylabel("Trade Balance (Billions USD)")
    plt.title("Tariff (%) vs Trade Balance")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    request += f"<img src='data:image/png;base64,{data}'/>"
    request += "<br>"
    request += "<a href='/level'>Try a different tariff level<a>"
    request += "<br>"
    request += "<a href='/'>Main Menu<a>"
    return request

app.run(host="localhost", port="8080", debug=True)