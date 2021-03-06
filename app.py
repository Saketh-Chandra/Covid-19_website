from flask import Flask, render_template, json, request, jsonify, redirect, url_for
from graph_files import data_file
import numpy as np

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')


def data_in(Country, State=None):
    index_in, data_in_c = data_file.data_Confirmed(Country, State)
    data_in_r = data_file.data_Recovered(Country, State)
    data_in_d = data_file.data_Deaths(Country, State)

    return [index_in, data_in_c, data_in_r, data_in_d]


@app.route('/world_map', methods=['GET'])
def world_wide():
    list_of_data = data_file.data_of_world_wide()
    index = [['Country', 'Confirmed', 'Recovered']]
    for i in list_of_data:
        index.append(i)
    data_json = json.dumps(index)
    # print(index[0:2], type(index))

    return render_template('worldwide.html', list_data=data_json)


@app.route('/', methods=['GET'])
def index1():
    list_data = data_file.list_of_country_state()
    list_data = list(set([i[0] for i in list_data]))
    list_data.sort()
    # data = {
    #     'list_of_countries':list_data
    # }
    data_json = json.dumps(list_data)
    return render_template('list_of_countries.html', data_list=list_data)  # json.dumps(data)


@app.route('/country/', methods=['POST'])
def index2():
    country = request.form['country']
    # print(country)
    list_data = data_file.list_of_country_state()
    f = np.where(list_data == country)
    list_data = list_data[f[0]]
    # print(list_data)
    list_data = list(set([i[1] for i in list_data]))
    list_data.sort()
    # print(list_data == [''], list_data)
    if list_data == ['']:
        return redirect(url_for('home_view', Country=country, State=''))
    else:
        if request.method == 'POST':
            data_json = json.dumps(list_data)
            return render_template('list_of_state.html', data_list=list_data, country=country)

    pass


@app.route('/country/state', methods=['GET', 'POST'])
def index3():
    try:
        if request.method == 'POST':
            country = request.form['country']
            state = request.form['state']
            # print(country, state)
            return redirect(url_for('home_view', Country=country, State=state))
        else:
            return render_template('404_error.html')
    except:
        return render_template('404_error.html')


@app.route('/data/', methods=["GET"])
def home_view():
    try:
        Country = str(request.args.get('Country')).title()
        State = str(request.args.get('State')).title()

        if Country == "None":
            Country = 'India'
            State = ''
        if State == "None":
            State = ''

        data_arr = data_in(Country, State)
        # data_arr = data_in("India", '')

        # print(data_arr[0][-1])

        index = json.dumps(data_arr[0])
        data_c = json.dumps(data_arr[1])
        data_r = json.dumps(data_arr[2])
        data_d = json.dumps(data_arr[3])
        last_time = (data_arr[0][-1])
        return render_template('index.html', in_list_index=index, in_list_data_c=data_c, in_list_data_r=data_r,
                               in_list_data_d=data_d, last_time=last_time, Country=Country, State=State)
    except:
        return render_template('404_error.html')


@app.route('/api', methods=['GET'])
def home_api():  # http://127.0.0.1:5000/api?Country=India&State=
    Country = str(request.args.get('Country')).title()
    State = str(request.args.get('State')).title()

    if Country == "None":
        Country = ''
        State = ''
    if State == "None":
        State = ''
    data_arr = data_in(Country, State)

    index = data_arr[0]
    data_c = data_arr[1]
    data_r = data_arr[2]
    data_d = data_arr[3]
    # print(type(data_c))
    d = {
        "dates": index,
        "Confirmed": data_c,
        "Recovered": data_r,
        "Deaths": data_d
    }
    # print(d)
    return json.dumps(d)


@app.route('/new')
def new_home():
    Country = str(request.args.get('Country')).title()
    State = str(request.args.get('State')).title()
    # print(Country)

    if Country == "None":
        Country = ''
        State = ''
    if State == "None":
        State = ''
    index, c, r, d = data_file.new_cases_c(Country=Country, State=State)
    # print(index[-1], c[-1], r[-1], d[-1])
    return render_template('new.html', data_c=json.dumps(c), data_r=json.dumps(r), data_d=json.dumps(d),
                           index=json.dumps(index), Country=Country, State=State)


if __name__ == '__main__':
    app.run()
