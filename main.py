import pandas as pd
from datetime import datetime

import requests
from flask_mysqldb import MySQL
from flask import render_template, Flask, request, session
from sqlalchemy import  create_engine
from distance_calculation import get_postal_code_within_km

app = Flask(__name__)
app.secret_key = "thisismysecretkey"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MyNewPass'
app.config['MYSQL_DB'] = 'cc_schema'

mysql = MySQL(app)

db_connection_str = (f"mysql+pymysql://{app.config['MYSQL_USER']}" 
                    f":{app.config['MYSQL_PASSWORD']}@{app.config['MYSQL_HOST']}/{app.config['MYSQL_DB']}")
db_connection = create_engine(db_connection_str)


@app.route('/')
def start_app():
    """
    Initial page!
    :return: The first page with the questionnaire for parents to complete
    """
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def recommend():
    """
    Get the inputs from the recommendation form completed by parents
    and send to KIE to get recommendations
    :return: home.html with inputs
    """
    child_birthdate = request.form["child-birthdate"]
    child_enrolment = request.form["child-enrolment"]
    service_type = request.form["service-type"]
    location = request.form["location"]
    acceptable_distance = request.form["acceptable-distance"]
    citizenship_type = request.form["citizenship-type"]
    second_language = request.form["second-language"]
    dietary_restrictions = request.form["dietary-restrictions"]
    fee_range = request.form["fee-range"]

    dict_from_kie = get_api(fee_range, location, acceptable_distance, second_language,
                            dietary_restrictions, child_enrolment, child_birthdate, citizenship_type, service_type)

    return render_template('home.html', result=dict_from_kie,
                           child_birthdate=child_birthdate,
                           child_enrolment=child_enrolment,
                           study_level=dict_from_kie["studyLevel"],
                           service_type=service_type,
                           location=location,
                           acceptable_distance=acceptable_distance,
                           citizenship_type=citizenship_type,
                           second_language=second_language,
                           dietary_restrictions=dietary_restrictions,
                           fee_range=fee_range)


@app.route('/update_data', methods=['POST'])
def update():
    """
    Update the MySQL database
    :return:
    """
    data = request.form.to_dict(flat=False)
    child_id = data.pop('child-id', None)[0]
    contact_details = data.pop("contact-details", None)[0]
    child_birthdate = data.pop("child-birthdate", None)[0]
    child_enrolment = data.pop("child-enrolment", None)[0]
    study_level = data.pop("study-level", None)[0]
    location = data.pop("location", None)[0]
    service_type = data.pop("service-type", None)[0]
    acceptable_distance = data.pop("acceptable-distance", None)[0]
    fee_range = data.pop("fee-range", None)[0]
    second_language = data.pop("second-language", None)[0]
    dietary_restrictions = data.pop("dietary-restrictions", None)[0]
    data.pop("child-citizenship", None)

    child_exist_in_details_df = pd.read_sql(f'SELECT * from parent_details  '
                                            f'WHERE child_idno="{child_id}"', con=db_connection)
    # If child_idno already exist, then update. Else, insert the data
    if child_exist_in_details_df.empty:
        cur = mysql.connection.cursor()

        sql = (f"INSERT INTO parent_details (child_idno, child_birthdate, enrolment_date, " 
               f"study_level, ideal_location, acceptable_distance, acceptable_fees, "
               f"second_language, dietary_restrictions, service_type, parent_contact) "
               f"VALUES ('{child_id}', '{child_birthdate}', '{child_enrolment}', '{study_level}', "
               f"'{location}', '{acceptable_distance}', '{fee_range}', '{second_language}', '{dietary_restrictions}', "
               f"'{service_type}', '{contact_details}')")
        cur.execute(sql)

        mysql.connection.commit()
    else:
        cur = mysql.connection.cursor()
        sql = (f"UPDATE parent_details "
               f"SET child_birthdate='{child_birthdate}', enrolment_date='{child_enrolment}', "
               f"study_level='{study_level}', ideal_location='{location}', "
               f"acceptable_distance='{acceptable_distance}', second_language='{second_language}', "
               f"dietary_restrictions='{dietary_restrictions}', service_type='{service_type}', "
               f"parent_contact='{contact_details}' WHERE child_idno='{child_id}';")
        cur.execute(sql)
        mysql.connection.commit()

    # If child_idno AND rank already exist, then update. Else, insert the data
    now_str = datetime.now().strftime("%Y-%m-%d")
    for key, value in data.items():
        if value[0] != "":
            child_exist_in_choices_df = pd.read_sql(f'SELECT * from parent_choices '
                                                    f'WHERE child_idno="{child_id}" AND '
                                                    f'childcare_rank="{value[0]}"', con=db_connection)
            if child_exist_in_choices_df.empty:
                cur = mysql.connection.cursor()

                sql = ("INSERT INTO parent_choices (child_idno, centre_code, childcare_rank, "
                       "reg_date) VALUES (%s, %s, %s, %s)")
                val = (child_id, key, value[0], now_str)
                cur.execute(sql, val)

                mysql.connection.commit()
            else:
                cur = mysql.connection.cursor()
                sql = ("UPDATE parent_choices "
                       "SET centre_code=%s, reg_date=%s "
                       "WHERE child_idno=%s AND childcare_rank=%s")
                val = (key, now_str, child_id, value[0])
                cur.execute(sql, val)
                mysql.connection.commit()

    details_pdf = pd.read_sql(f'SELECT child_idno, parent_contact from parent_details  '
                              f'WHERE child_idno="{child_id}"', con=db_connection)
    choices_pdf = pd.read_sql(f'SELECT child_idno, centre_code, childcare_rank from parent_choices '
                              f'WHERE child_idno="{child_id}"', con=db_connection)
    full_df = details_pdf.merge(choices_pdf,
                                how="inner",
                                on="child_idno")
    full_json = full_df.to_dict('records')

    return render_template('submission.html', result=full_json)


def get_api(fee_range, location, distance, language, dietary_restrictions,
            enrolment_date, child_birthdate, citizenship_type, service):

    if "<" in distance:
        km = distance[-3:-2]
        within_km_list = get_postal_code_within_km(location, km)
    else:
        within_km_list = get_postal_code_within_km(location, "3")

    # api-endpoint
    url = "http://localhost:8080/addParent"

    # defining a params dict for the parameters to be sent to the API
    params = {"feeRange": fee_range,
              "location": location,
              "distance": distance,
              "language": language,
              "dietaryRestrictions": dietary_restrictions,
              "enrolmentDateStr": enrolment_date,
              "childBirthdateStr": child_birthdate,
              "citizenshipType": citizenship_type,
              "service": service,
              "postalList": ", ".join(within_km_list)}

    # sending get request and saving the response as response object
    r = requests.post(url=url, params=params)

    # extracting data in json format
    data = r.json()

    relevant_centre_code = []
    for ccDict in data["childcareList"]:
        relevant_centre_code.append(ccDict.get("centreCode"))

    full_childcare_list = data["childcareList"]
    full_childcare_list.extend(data["otherChildcareList"])
    data["fullChildcareList"] = []
    added_centres = []
    for ccDict in full_childcare_list:
        if ccDict["centreCode"] not in added_centres:
            added_centres.append(ccDict["centreCode"])
            ccDict["full_relevance"] = ccDict["centreCode"] in relevant_centre_code
            ccDict["rank"] = None
            data["fullChildcareList"].append(ccDict)

    centre_codes = []
    for cc in data["fullChildcareList"]:
        centre_codes.append(cc["centreCode"])

    centre_codes = "','".join(list(set(centre_codes)))

    reviews_df = pd.read_sql(f"SELECT * from reviews  "
                             f"WHERE centre_code IN ('{centre_codes}')", con=db_connection)
    for curr_cc in data["fullChildcareList"]:
        if curr_cc["centreCode"] in list(reviews_df["centre_code"]):
            filtered_reviews_df = reviews_df[reviews_df["centre_code"] == curr_cc["centreCode"]]
            filtered_reviews_df = filtered_reviews_df[["review", "score"]]
            curr_cc["reviews"] = dict(zip(filtered_reviews_df.review, filtered_reviews_df.score))
        else:
            curr_cc["reviews"] = {}

    return data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
    # print(get_api(fee_range="Any",
    #               location="520101",
    #               distance="< 1km",
    #               language="Chinese",
    #               dietary_restrictions="Any",
    #               enrolment_date="2020-12-17",
    #               # child_name="Serene",
    #               child_birthdate="2017-12-17",
    #               citizenship_type="SC",
    #               # child_id="T12345678A",
    #               service="Full Day"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
