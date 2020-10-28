from flask import Flask, render_template, json, request, jsonify
from graph_files import data_file

app = Flask(__name__)


def data_in(Country, State=None):
    index_in, data_in_c = data_file.data_Confirmed(Country, State)
    data_in_r = data_file.data_Recovered(Country, State)
    data_in_d = data_file.data_Deaths(Country, State)

    return [index_in, data_in_c, data_in_r, data_in_d]


@app.route('/', methods=["GET"])
def home_view():
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
    return render_template('index.html', in_list_index=index, in_list_data_c=data_c, in_list_data_r=data_r,
                           in_list_data_d=data_d)


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
    print(type(data_c))
    d = {
        "dates": index,
        "Confirmed": data_c,
        "Recovered": data_r,
        "Deaths": data_d
    }
    print(d)
    return json.dumps(d)


@app.route('/new')
def new_home():
    Country = str(request.args.get('Country')).title()
    State = str(request.args.get('State')).title()
    print(Country)

    if Country == "None":
        Country = ''
        State = ''
    if State == "None":
        State = ''
    index, c, r, d = data_file.new_cases_c(Country = Country,State=State)
    print(index[-1], c[-1], r[-1], d[-1])
    return render_template('new.html', data_c=json.dumps(c), data_r=json.dumps(r), data_d=json.dumps(d),
                           index=json.dumps(index))


if __name__ == '__main__':
    app.debug(True)
    app.run()
