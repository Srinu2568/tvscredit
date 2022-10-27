import streamlit as st
import requests
import os
import uuid
from deta import Deta
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import time
import datetime as dt
import streamlit_authenticator as stauth
import database as db
from datetime import datetime
import streamlit.components.v1 as components
import base64

load_dotenv('.env')

DETA_KEY = os.getenv('DETA_KEY') # Load the deta key from .env file

# Initialzie deta object with a project key

# Initialize with a Project Key
deta = Deta(DETA_KEY)


# This how to connect to or create a database.
drive = deta.Drive("user_drive")

# Car and bike data
db2 = deta.Base('car_db')
db3 = deta.Base('bike_db')

# Car data
cardata = db2.get('car')
bikedata = db3.get('bike')

# ---data for selecting in the form---
carlist = cardata['carlist']
loclist = cardata['loclist']
yearlist = cardata['yearlist']
ownerlist = cardata['ownerlist']
fuellist = cardata['fuellist']

# ---Data for decoding---
dctcar = cardata['dctcar']
dctloc = cardata['dctloc']
dctyear = cardata['dctyear']
dctowner = cardata['dctowner']
dctfuel = cardata['dctfuel']

# ----data for the bike-------
dctbike = bikedata['dctbike']

dctbrand = bikedata['dctbrand']

dctcity = bikedata['dctcity']

dctownerbike = bikedata['dctownerbike']

# ----list data for bike------
bikelist = bikedata['bikelist']

brandlist = bikedata['brandlist']

citylist = bikedata['citylist']

ownerlistbike = bikedata['ownerlistbike']

# set page config
st.set_page_config(page_title='TVS CREDIT Vehicle Valuation', page_icon='./logo/api.png', layout='wide')

html = f"""<a href='{'https://www.tvscredit.com/'}'><img src='https://www.tvscredit.com/media/1927/tvs-credit-logo-01.png' width='200' height='50'></a>"""
st.markdown(html, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# User Authentication

users = db.fetch_all_users() # It will return a json containing key, name, password(hashed), isEval(boolean)


usernames = [user['key'] for user in users]
names = [user['name'] for user in users]
hashed_passwords = [user['password'] for user in users]
isEval = [user['isEval'] for user in users]


credentials = {"usernames":{}}


for un, name, pw in zip(usernames, names, hashed_passwords):
    user_dict = {"name":name,"password":pw}
    credentials["usernames"].update({un:user_dict})

authenticator = stauth.Authenticate(credentials,
'some_cookie_name','some_signature_key',cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')
    



# if authentication_status True and user is not evaluator
if authentication_status and not db.get_user(username)['isEval']:
    # Sidebar
    with st.sidebar:
        selected = option_menu(
            menu_title = 'Menu',
            options = ['Home', 'Car', 'Bike', 'Contact'],
            icons = ['house', 'speedometer', 'bicycle', 'envelope'],
            menu_icon = 'cast',
        )
        # Logout
        authenticator.logout('Logout', 'main')



#     # Home Page
    if selected == 'Home':
        def load_lottieurl(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            else:
                return r.json()
        # API DOC URL FOR CAR
        URL = 'https://tvs-price-predictor.herokuapp.com/docs'
        # API DOC URL FOR BIKE
        URL2 = 'https://tvs-price-predictor-bike.herokuapp.com/docs'

        # ---stack lottie transition---
        lottie_api = load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_8NYY2Y.json')

        with st.container():
            # ------ HEADER SECTION-------
            left_column, right_column = st.columns(2)
            with left_column:
                st.title('TVS CREDIT - Effortless Price Predictions by AI:speech_balloon:')
                st.subheader('As per the trends in market :chart_with_upwards_trend:')
                st.write('''A few years ago, the ratio of new cars to used cars 
                was 1:1.2 which is now at 1:2.2. The used car market in India 
                has been the center of attention in the slow growing 
                automotive industry in India.''')
                st.subheader('How our API is helpful :star:')
                st.write('''Keeping the demand of used cars in mind, 
                This website helps users to predict the price to sell/buy the car
                with the help of AI and ML.''')
                st.subheader('How to use? :hushed:')
                st.write('The API is encoded, only the website can decode and call it.')
                st.write('Check out the API here :fire:')
                st.write('[Learn More >](https://tvs-price-predictor.herokuapp.com/docs)')
            # Lottie element
            with right_column:
                st_lottie(lottie_api, height=300, key='api')

    # Car Page
    form_data = {}
    if selected == 'Car':
        st.header('GET THE PRICE OF USED CAR')
        # Form to take data from user
        col1, col2 = st.columns(2)
        with col1:
            with st.form(key='form1'):
                # car = st.text_input('Car Model')
                car = st.selectbox('Car Model', options=carlist)
                car_data = car # For storing in database we use this variable
                car = dctcar[car]
                # location = st.text_input('Location')
                location = st.selectbox('Location', options=loclist)
                location_data = location
                location = dctloc[location]
                # year = st.text_input('Year')
                year = st.selectbox('Year', options=yearlist)
                year_data = year
                year = dctyear[year]
                km_driven = st.text_input('Kms Driven (Enter accurate value for better results)')
                # owner_type = st.text_input('Owner Type')
                owner_type = st.selectbox('Owner Type', options=ownerlist)
                owner_type_data = owner_type
                owner_type = dctowner[owner_type]
                # fuel_type = st.text_input('Fuel Type')
                fuel_type = st.selectbox('Fuel Type', options=fuellist)
                fuel_type_data = fuel_type
                fuel_type = dctfuel[fuel_type]
                power = st.text_input('Power in bhp')
                # power = int(power)
                price = st.text_input('Original Price in lakhs(Example: 13.56 lakhs)')


                # ---Submit Button---
                submit_button = st.form_submit_button(label='Get Car Price')
                # if submit_button:
                #     st.success('Thanks for using!')


                if submit_button and (km_driven=="" or power == "" or price == ""):
                    # st.success('Thanks for using!')
                    st.warning('You have missed some fields to fill in!')
                elif km_driven=="" or power == "" or price == "":
                    st.warning('Please fill out all the fields!')
                else:
                    st.success('Thanks for Filling!')
                    # ---Calling the API---
                    URL = 'https://tvs-price-predictor.herokuapp.com/predict'

                    # Best Condition Pred
                    PARAMS = {
                    "Car": car,
                    "Location": location,
                    "Year": year,
                    "Kilometers_Driven": km_driven,
                    "Owner_Type": owner_type,
                    "Fuel_Type": fuel_type,
                    "Power": power
                    }
                    # Good condition Pred
                    PARAMS2 = {
                    "Car": car,
                    "Location": location,
                    "Year": int(year-3),
                    "Kilometers_Driven": km_driven,
                    "Owner_Type": owner_type,
                    "Fuel_Type": fuel_type,
                    "Power": power
                    }
                    # if submit_button:    
                    #     response = requests.post(URL, json=PARAMS)
                        # st.write(response.json()['prediction'])

            # # Storing the predicted price in a session state
            # if 'pred_price' not in st.session_state:
            #     st.session_state['pred_price'] = 0
            # ---Result---
            if submit_button and not (km_driven=="" or power == "" or price == ""):
                # Wait transition
                with st.spinner('Wait for it...'):
                    response = requests.post(URL, json=PARAMS)
                    response2 = requests.post(URL, json=PARAMS2)
                # st.success('Done!')
                # response = requests.post(URL, json=PARAMS)
                # st.write(response.json()['prediction'])

                # ---Progress bar---
                # Original Price
                org_price = float(price)
                st.write('Original Price', org_price)

                # For Best Price
                resp_result = response.json()['prediction']
                st.write('Best Price ', resp_result)
                my_bar = st.progress(100) # set to original price



                perc_resp = int((resp_result/org_price)*100)
                for percent_complete in range(perc_resp):
                    time.sleep(0.001)
                    my_bar.progress(percent_complete + 1)

                # For Average Price
                resp_result2 = response2.json()['prediction']
                st.write('Average Price ', resp_result2)
                perc_resp2 = int((resp_result2/org_price)*100)
                my_bar2 = st.progress(100) # set to original price

                for percent_complete in range(perc_resp2):
                    time.sleep(0.001)
                    my_bar2.progress(percent_complete + 1)

                # Storing the predicted price in a session state
                if 'pred_price' not in st.session_state:
                    st.session_state['pred_price'] = 0
                st.session_state['pred_price'] = resp_result
            # Handling session state
            if 'pred_price' not in st.session_state:
                st.session_state['pred_price'] = 0
            # Json for DB
            form_data = {
            "Car": car_data,
            "Location": location_data,
            "Year": year_data,
            "Kilometers_Driven": km_driven,
            "Owner_Type": owner_type_data,
            "Fuel_Type": fuel_type_data,
            "Power": power,
            "Original_Price": price,
            "Predicted_price": st.session_state['pred_price'],
            "Type": 'car',
            'Feedback': '',
            'Time_Stamp': time.time(),
            'Evaluator_Id': None,
            'isEvaluated': False,
            'Eval_Price': 0
            }

            st.write('---')
            st.write('For vehicle Inspection and Final Valuation Please Upload the Images of Your Car')
            # Image upload
            uploaded_files = st.file_uploader("Choose photos to upload", accept_multiple_files=True, type=['png', 'jpeg', 'jpg'])
            st.set_option('deprecation.showfileUploaderEncoding', False) # file encoding deprecated set to false
            submit_button_photos = st.button(label='Upload Photos')


            # Save the file in local storage and delete later
            pic_names = []
            pics = []
            for uploaded_file in uploaded_files:
                file = uploaded_file.read()
                image_result = open(uploaded_file.name, 'wb') # create a writable image and write the decoding result
                image_result.write(file) # And finally save to current path -> './'
                # st.write("filename:", uploaded_file.name)
                pic_names.append(uploaded_file.name)
                image_result.close()
                
            # If submit upload it to the cloud    
            if submit_button_photos:
                with st.spinner('Uploading....'):
                    for i in range(len(pic_names)):
                        unique_id = str(uuid.uuid4())
                        name = 'car-'+ form_data['Car'] + '-' +unique_id + '-' + uploaded_file.name # car was added infront of string to seperate it from bikes
                        path_file = path='./'+pic_names[i]
                        drive.put(name, path=path)
                        os.remove(pic_names[i]) # Removes the files in local storage
                        pics.append(name)
                    # Get the data of current user
                    user_data = db.get_user(username)
                    res_pics = user_data['images']
                    pics = pics + res_pics
                    forms = user_data['form_data']
                    mod_forms = []
                    # Creating a dictionary by removing Time_Stamp from db_form and recieved_form
                    for form in forms:
                        res = {k:v for k, v in zip(form.keys(), form.values()) if k!='Time_Stamp' and k!='Bike' and k!='Feedback' and k!='Type'}
                        mod_forms.append(res)
                    mod_form_data = {k:v for k, v in zip(form_data.keys(), form_data.values()) if k!= 'Time_Stamp' and k!='Bike' and k!='Feedback' and k!='Type'}
                    if mod_form_data not in mod_forms:
                        forms.append(form_data)
                    car_list = user_data['type_data']
                    if 'car' not in car_list:
                        car_list = list(car_list)
                        car_list.append('car')
                    # Update the user's images with uploaded images
                    db.update_user(username, updates={'images':pics, 'type_data':car_list, 'form_data':forms})
                    st.success('Thanks for uploading!')

        st.subheader('Upload link of 360 Interior view for your car(BETA)')
        with st.form(key='form360'):
            link = st.text_input('Upload 360 interior link')
            link_button = st.form_submit_button('Submit Link')
        if link_button:
            db.update_user(username, updates={'link':link})
        st.write('[Learn More >](https://panoraven.com/blog/en/how-to-take-360-images-with-a-smartphone/)')
        


        with col2:
            def load_lottieurl(url):
                r = requests.get(url)
                if r.status_code != 200:
                    return None
                else:
                    return r.json()
            lottie_api = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_kqfglvmb.json')
            st_lottie(lottie_api, height=500, key='api')

#     # Bike Page
    if selected == 'Bike':
        st.header('GET THE PRICE OF USED BIKE')
        # Form to take data from user
        col1, col2 = st.columns(2)
        with col1:
            with st.form(key='form2'):
                bike = st.selectbox('Bike Model', options=bikelist)
                bike_data = bike # To store in the database
                bike = dctbike[bike]
                # location = st.text_input('Location')
                city = st.selectbox('Location', options=citylist)
                city_data = city
                city = dctcity[city]
                # year = st.text_input('Year')
                bike_year = st.selectbox('Year', options=yearlist)
                if bike_year == 'less than 2003':
                    bike_year = 2002
                age = int(dt.date.today().year)-int(bike_year)                # Present year - selling year
                # Km_driven by bike
                km_driven_bike = st.text_input('Kms Driven (Enter accurate value for better results)')
                # owner_type = st.text_input('Owner Type')
                owner_type_bike = st.selectbox('Owner Type', options=ownerlistbike)
                owner_type_bike_data = owner_type_bike
                owner_type_bike = dctownerbike[owner_type_bike]
                # brand of bike
                bike_brand = st.selectbox('Brand', options=brandlist)
                bike_brand_data = bike_brand
                bike_brand = dctbrand[bike_brand]
                # Power of bike (Horse Power)
                bike_power = st.text_input('Power in bhp')
                # power = int(power)
                bike_price = st.text_input('Original Price')


                # ---Submit Button---
                submit_button2 = st.form_submit_button(label='Get Bike Price')
                # if submit_button:
                #     st.success('Thanks for using!')


                if submit_button2 and (km_driven_bike=="" or bike_power == "" or bike_price == ""):
                    # st.success('Thanks for using!')
                    st.warning('You have missed some fields to fill in!')
                elif km_driven_bike=="" or bike_power == "" or bike_price == "":
                    st.warning('Please fill out all the fields!')
                else:
                    st.success('Thanks for Filling!')
                    # ---Calling the API---
                    URL = 'https://tvs-price-predictor-bike.herokuapp.com/bike-predict'

                    # Best Condition Pred
                    PARAMS = {
                    "bike_name": bike,
                    "city": city,
                    "kms_driven": km_driven_bike,
                    "owner": owner_type_bike,
                    "age": age,
                    "power": bike_power,
                    "brand": bike_brand
                    }
                    # Good condition Pred
                    PARAMS2 = {
                    "bike_name": bike,
                    "city": city,
                    "kms_driven": km_driven_bike,
                    "owner": owner_type_bike,
                    "age": int(int(age)+3),
                    "power": bike_power,
                    "brand": bike_brand
                    }
                    # if submit_button:    
                    #     response = requests.post(URL, json=PARAMS)
                        # st.write(response.json()['prediction'])


            # ---Result---
            pred_price_bike = 0
            if submit_button2 and not (km_driven_bike=="" or bike_power == "" or bike_price == ""):
                # Wait transition
                with st.spinner('Wait for it...'):
                    bike_response = requests.post(URL, json=PARAMS)
                    bike_response2 = requests.post(URL, json=PARAMS2)
                # st.success('Done!')
                # response = requests.post(URL, json=PARAMS)
                # st.write(response.json()['prediction'])

                # ---Progress bar---
                # Original Price
                bike_org_price = float(bike_price)
                st.write('Original Price', bike_org_price)

                # For Best Price
                bike_resp_result = bike_response.json()['bike_price_prediction']
                bike_pred_price = bike_resp_result
                st.write('Best Price ', bike_resp_result)
                my_bar_bike = st.progress(100) # set to original price

                bike_perc_resp = int((bike_resp_result/bike_org_price)*100)
                for percent_complete in range(bike_perc_resp):
                    time.sleep(0.001)
                    my_bar_bike.progress(percent_complete + 1)

                # For Average Price
                bike_resp_result2 = bike_response2.json()['bike_price_prediction']
                st.write('Average Price ', bike_resp_result2)
                bike_perc_resp2 = int((bike_resp_result2/bike_org_price)*100)
                bike_my_bar2 = st.progress(100) # set to original price

                for percent_complete in range(bike_perc_resp2):
                    time.sleep(0.001)
                    bike_my_bar2.progress(percent_complete + 1)

                # Storing the predicted price in a session state
                if 'bike_pred_price' not in st.session_state:
                    st.session_state['bike_pred_price'] = 0
                st.session_state['bike_pred_price'] = bike_resp_result
            # Handling session state
            if 'bike_pred_price' not in st.session_state:
                st.session_state['bike_pred_price'] = 0        
            # Json for DB
            bike_form_data = {
            "Bike": bike_data,
            "City": city_data,
            "Year": bike_year,
            "Kilometers_Driven": km_driven_bike,
            "Owner_Type": owner_type_bike_data,
            "Bike_Brand": bike_brand_data,
            "Power": bike_power,
            "Original_Price": bike_price,
            "Predicted_price": st.session_state['bike_pred_price'],
            "Type": 'bike',
            "Feedback": '',
            "Time_Stamp": time.time(),
            "Evaluator_Id": None,
            "isEvaluated": False,
            "Eval_Price": 0
            }

            st.write('---')
            st.write('For vehicle Inspection and Final Valuation Please Upload the Images of Your Bike')
            # Image upload
            uploaded_files = st.file_uploader("Choose photos to upload", accept_multiple_files=True, type=['png', 'jpeg', 'jpg'])
            st.set_option('deprecation.showfileUploaderEncoding', False) # file encoding deprecated set to false
            submit_button_photos_bike = st.button(label='Upload Photos')


            # Save the file in local storage and delete later
            pic_names = []
            bike_pics = []
            for uploaded_file in uploaded_files:
                file = uploaded_file.read()
                image_result = open(uploaded_file.name, 'wb') # create a writable image and write the decoding result
                image_result.write(file) # And finally save to current path -> './'
                # st.write("filename:", uploaded_file.name)
                pic_names.append(uploaded_file.name)
                image_result.close()
                
            # If submit upload it to the cloud    
            if submit_button_photos_bike:
                with st.spinner('Uploading....'):
                    for i in range(len(pic_names)):
                        unique_id = str(uuid.uuid4())
                        name = 'bike-'+ bike_form_data['Bike'] + '-' +unique_id + '-' + uploaded_file.name # car was added infront of string to seperate it from bikes
                        path_file = path='./'+pic_names[i]
                        drive.put(name, path=path)
                        os.remove(pic_names[i]) # Removes the files in local storage
                        bike_pics.append(name)
                    # Get the data of current user
                    user_data = db.get_user(username)
                    bike_res_pics = user_data['images']
                    bike_pics = bike_pics + bike_res_pics
                    forms = user_data['form_data']
                    mod_forms = []
                    # Creating a dictionary by removing Time_Stamp from db_form and recieved_form
                    for form in forms:
                        res = {k:v for k, v in zip(form.keys(), form.values()) if k!='Time_Stamp' and k!='Car' and k!='Feedback' and k!='Type'}
                        mod_forms.append(res)
                    mod_form_data = {k:v for k, v in zip(bike_form_data.keys(), bike_form_data.values()) if k!= 'Time_Stamp' and k!='Car' and k!='Feedback' and k!='Type'}
                    if mod_form_data not in mod_forms:
                        forms.append(bike_form_data)
                    bike_list = user_data['type_data']
                    if 'bike' not in bike_list:
                        bike_list = list(bike_list)
                        bike_list.append('bike')
                    # Update the user's images with uploaded images
                    db.update_user(username, updates={'images':bike_pics, 'type_data':bike_list, 'form_data':forms})
                    st.success('Thanks for uploading!')

        with col2:
            def load_lottieurl(url):
                r = requests.get(url)
                if r.status_code != 200:
                    return None
                else:
                    return r.json()
            lottie_api = load_lottieurl('https://assets8.lottiefiles.com/packages/lf20_ztjvhpit.json')
            st_lottie(lottie_api, height=500, key='api')

#     # Contact Page
    if selected == 'Contact':
        st.header(':mailbox: Get In touch With Me!')

        # ---Contact Form---
        contact_form = """
        <form action="https://formsubmit.co/mnvsrinivas1@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here"></textarea>
            <button type="submit">Send</button>
        </form>
        """

        st.markdown(contact_form, unsafe_allow_html=True)

        # Use Local CSS File
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        local_css("style/style.css")

        st.subheader('Follow me on')
        html = f"""<ul>
                <li style="display:inline-block;">
                    <a href='{'https://www.linkedin.com/in/srinivas-menta-b96977214/'}'><img src='https://www.sfdcamplified.com/wp-content/uploads/2019/04/linkedin-logo-copy.png' width='25' height='25'></a>
                </li>
                <li style="display:inline-block;">
                    <a href='{'https://github.com/Srinu2568'}'><img src='https://icones.pro/wp-content/uploads/2021/06/icone-github-bleu.png' width='25' height='25'></a>
                </li>
                <li style="display:inline-block;">
                    <a href='{'https://www.instagram.com/mnv_srinivas/'}'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/2048px-Instagram_icon.png' width='25' height='25'></a>
                </li>
                <li style="display:inline-block;">
                    <a href='{'https://medium.com/@mnvsrinivas1'}'><img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4tZSzY3tgMrgLEyJWY0fChWR-7gwDCHep0UEy_PE0sSiu_gUdXo6pM402iTW-jS4W0XY&usqp=CAU' width='25' height='25'></a>
                </li>
            </ul>"""
        # html = f"<a href='{'https://www.linkedin.com/in/srinivas-menta-b96977214/'}'><img src='https://www.sfdcamplified.com/wp-content/uploads/2019/04/linkedin-logo-copy.png' width='25' height='25'></a>"
        st.markdown(html, unsafe_allow_html=True)
        # 'https://png.pngtree.com/png-clipart/20180626/ourmid/pngtree-instagram-icon-instagram-logo-png-image_3584853.png'

# if auth status is true and user in evaluator
if authentication_status and db.get_user(username)['isEval']:
    # Car session_states
    if 'usercars' not in st.session_state:
        st.session_state.usercars = []
    if 'desired_user' not in st.session_state:
        st.session_state.desired_user = None
    if 'i' not in st.session_state:
        st.session_state.i = {}
    if 'val' not in st.session_state:
        st.session_state.val = []

    # Bike session_states
    if 'userbikes' not in st.session_state:
        st.session_state.userbikes = []
    if 'desired_user_bike' not in st.session_state:
        st.session_state.desired_user_bike = None
    if 'i2' not in st.session_state:
        st.session_state.i2 = {}
    if 'val2' not in st.session_state:
        st.session_state.val = []
    
    with st.sidebar:
        selected = option_menu(
            menu_title = 'Menu',
            options = ['Home', 'Car', 'Bike', 'Evaluated Vehicles'],
            icons = ['house', 'speedometer', 'bicycle', 'check2-circle'],
            menu_icon = 'cast',
        )
        # Logout
        authenticator.logout('Logout', 'main')

    # Home
    if selected == 'Home':
        st.write('Hello Evaluator')
        # test_user = db.get_user('test_user') # Getting user details
        # res_image = test_user['images'][0] # Getting image name from deta drive
        # res_image2 = test_user['images'][1]
        # arr_im = [res_image, res_image2]
        # im = drive.get(res_image)
        # im2 = drive.get(res_image2)
        # # with open(im, 'rb') as image2string:
        # contents = im.read()
        # data_url = base64.b64encode(contents).decode('utf-8')
        # contents2 = im2.read()
        # data_url2 = base64.b64encode(contents2).decode('utf-8')
        # file_bytes = np.asarray(bytearray(im.read()), dtype=np.uint8) # Converting image(deta object) to bytearray using numpy
        # cs = base64.b64encode(im.read())
        # st.write()
        # opencv_image = cv2.imdecode(file_bytes, 1) # Decoding the bytearray to image(Byte stream)
        # file_bytes2 = np.asarray(bytearray(im2.read()), dtype=np.uint8)
        # opencv_image2 = cv2.imdecode(file_bytes2, 1)
        # arr = [opencv_image, opencv_image2]
        # st.image(arr, channels = 'BGR', output_format='PNG', width=150)
        # res = f"""<iframe width="90%" height="500px" allowFullScreen="true" allow="accelerometer; magnetometer; gyroscope" style="display:block; margin:20px auto; border:0 none; max-width:880px;border-radius:8px; box-shadow: 0 1px 1px rgba(0,0,0,0.11),0 2px 2px rgba(0,0,0,0.11),0 4px 4px rgba(0,0,0,0.11),0 6px 8px rgba(0,0,0,0.11),0 8px 16px rgba(0,0,0,0.11);" src="https://panoraven.com/en/slider/vpUsXjEe0F"></iframe>
        #         """
        # components.html(res, height=600, scrolling=True)
    
    # Car
    car_form = {}
    val = []
    cars = []
    usercars = []
    needed_data = []
    if selected == 'Car':
        left, mid, right = st.columns(3)
        with mid:
            st.header('EVALUATOR DASHBOARD')
        st.write('SELECT VEHICLE TO EVALUATE')
        users = db.fetch_all_users()
        usecase = {user['name']:user['key'] for user in users}
        car_users = [user for user in users if 'car' in user['type_data'] and not user['isEval']]
        data = [{l['name']:(l['form_data'], l['images'])} for l in car_users]
        car_usernames = [list(x.keys())[0] for x in data]
        col1, col2 = st.columns(2)
        with col1:
            with st.form(key='form1'):
                car_user = st.selectbox('Users',options=car_usernames)
                car_user_button = st.form_submit_button(label='Select User')
            if car_user_button:
                if 'car_user_button' not in st.session_state:
                    st.session_state['car_user_button'] = True
                for i in data:
                    if list(i.keys())[0] == car_user:
                        val = i[car_user][0]
                st.session_state.val = val # Saving for later - eval feedback
                for i in val:
                    if i['Type'] == 'car' and not i['isEvaluated']:
                        cars.append(i['Car'])

                for i in val:
                    if i['Type'] == 'car' and not i['isEvaluated']:
                        usercars.append(i)
                    
                
                # print(val)
                # for i in val:
                #     if i['Type'] == 'bike' or not i['isEvaluated']:
                #         needed_data.append(i)
                
                        
        #######################################
                st.session_state.usercars = usercars # Used later for eval feedback form
                if len(usercars) != 0:
                    i = usercars[0] # Selecting the first form in the form data(which is the first uploaded one)
                    try:
                        st.session_state.val.remove(i)
                    except:
                        pass
                    st.session_state.i = i
                    st.write(f'Car : {i["Car"]}')
                    st.write(f'Fuel Type : {i["Fuel_Type"]}')
                    st.write(f'Kilometers Driven : {i["Kilometers_Driven"]}')
                    st.write(f'Location : {i["Location"]}')
                    st.write(f'Original Price : {i["Original_Price"]}')
                    st.write(f'Owner Type : {i["Owner_Type"]}')
                    st.write(f'Power : {i["Power"]}')
                    st.write(f'Predicted Price : {i["Predicted_price"]}')
                    st.write(f'Date of Request : {datetime.fromtimestamp(i["Time_Stamp"]).date()}')
                    st.write(f'Year : {i["Year"]}')
                    # Image display
                    desired_user = usecase[car_user]
                    st.session_state.desired_user = desired_user # Saving for later
                    test_user = db.get_user(desired_user) # Getting user details
                    user_res = db.get_user(desired_user) # Getting cur user details
                    user_images = user_res['images'] # Getting the name of images from user_db
                    # res_image = test_user['images'] # Getting image name from deta drive
                    arr2 = [] # Contains user specific images
                    for j in range(len(user_images)):
                        str_manip = f'car-{i["Car"]}-'
                        if user_images[j].startswith(str_manip):
                            arr2.append(user_images[j])
                    if len(arr2) != 0:
                        arr = [] # Contains actual images
                        mark2 = """  """     # html dynamic image generate string
                        for k in range(len(arr2)):
                            im = drive.get(arr2[k])
                            contents = im.read()
                            data_url = base64.b64encode(contents).decode('utf-8')
                            if k == 0:  # If the image item is first one keep the first slide to active
                                des_str = f""" <div class="carousel-item active">
                                <img class="d-block w-100" src="data:image/png;base64, {data_url}" alt="First slide">
                                </div> """
                            elif k != 0:  # If the image item is not first one keep the -- keep the remaining slides without active tag
                                des_str = f""" <div class="carousel-item">
                                <img class="d-block w-100" src="data:image/png;base64, {data_url}" alt="First slide">
                                </div> """
                            mark2 += des_str



                        ######################################################################################### 
                        # Import bootstrap cdn to html  
                        mark1 = """ <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
                                    <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
                                <style>
                                    .carousel {{
                                    width:640px;
                                    height:360px;
                                    }}
                                    image{{
                                        height:640px;
                                        width:360px;
                                    }}
                                </style>
                                <div class="carousel-inner"> """
                        mark3 = """ </div>
                                <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
                                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                    <span class="sr-only">Previous</span>
                                </a>
                                <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
                                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                    <span class="sr-only">Next</span>
                                </a>
                                </div>

                                <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                                    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.3/dist/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
                                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script> """
                    
                        # html rendering
                        res_html = mark1 + mark2 + mark3
                        components.html(res_html, height=350, width=600)

                        try:
                            if user_res['link']:
                                res = f"""<iframe width="90%" height="500px" allowFullScreen="true" allow="accelerometer; magnetometer; gyroscope" style="display:block; margin:20px auto; border:0 none; max-width:880px;border-radius:8px; box-shadow: 0 1px 1px rgba(0,0,0,0.11),0 2px 2px rgba(0,0,0,0.11),0 4px 4px rgba(0,0,0,0.11),0 6px 8px rgba(0,0,0,0.11),0 8px 16px rgba(0,0,0,0.11);" src="{user_res['link']}"></iframe>
                                        """
                                components.html(res, height=600, scrolling=True)
                        except:
                            pass

                        #     file_bytes = np.asarray(bytearray(im.read()), dtype=np.uint8) # Converting image(deta object) to bytearray using numpy
                        #     opencv_image = cv2.imdecode(file_bytes, 1) # Decoding the bytearray to image(Byte stream)
                        #     arr.append(opencv_image)
                        # st.image(arr, channels = 'BGR', output_format='PNG', width=150)

                        # im = drive.get(res_image)
                        # im2 = drive.get(res_image2)
                        # file_bytes2 = np.asarray(bytearray(im2.read()), dtype=np.uint8)
                        # opencv_image2 = cv2.imdecode(file_bytes2, 1)
                        # arr = [opencv_image, opencv_image2]
                        # st.image(arr, channels = 'BGR', output_format='PNG', width=150)
                    
                    else: # if no pics
                        st.warning("User have not uploaded any images")
                    
                else: # If no cars to evaluate
                    st.warning("No cars to evaluate for the selected user")

                    
                # Evaluator feedback form
            st.header("This is feedback form of evaluator")
            with st.form(key='feed_form', clear_on_submit=True):
                feedback = st.text_input('Give feedback to the vehicle')
                evaluated_price = st.text_input('Evaluated Price')
                submit_button_feedback = st.form_submit_button(label='Submit Feedback')
                # alternate way
                # if 'submit_button_feedback' not in st.session_state:
                #     st.session_state.feedback = submit_button_feedback
                if submit_button_feedback and not evaluated_price == "" and not feedback == "":
                    # final form -> get the old form and modify it
                    final_form = st.session_state.i
                    # final_usercars -> form data which contains all the user forms in an array
                    final_usercars = st.session_state.usercars
                    new_form_data = {
                    "Car": final_form['Car'],
                    "Eval_Price": evaluated_price,
                    "Evaluator_Id": username,
                    "Feedback": feedback,
                    "Fuel_Type": final_form['Fuel_Type'],
                    "Kilometers_Driven": final_form['Kilometers_Driven'],
                    "Location": final_form['Location'],
                    "Original_Price": final_form['Original_Price'],
                    "Owner_Type": final_form['Owner_Type'],
                    "Power": final_form['Power'],
                    "Predicted_price": final_form['Predicted_price'],
                    "Time_Stamp": final_form['Time_Stamp'],
                    "Type": final_form['Type'],
                    "Year": final_form['Year'],
                    "isEvaluated": True
                    }
                    st.session_state.val.append(new_form_data) # Appending the updated form data to the end
                    db.update_user(st.session_state.desired_user, updates={'form_data':st.session_state.val})
                    st.success("Feedback submitted!")

#############################################################################################################################

    bike_form = {}
    val2 = []
    bikes = []
    userbikes = []
    needed_data2 = []
    # Bike
    if selected == 'Bike':
        left, mid, right = st.columns(3)
        with mid:
            st.header('EVALUATOR DASHBOARD')
        st.write('SELECT VEHICLE TO EVALUATE')
        users = db.fetch_all_users()
        usecase = {user['name']:user['key'] for user in users}
        bike_users = [user for user in users if 'bike' in user['type_data'] and not user['isEval']]
        data2 = [{l['name']:(l['form_data'], l['images'])} for l in bike_users]
        bike_usernames = [list(x.keys())[0] for x in data2]
        col1, col2 = st.columns(2)
        with col1:
            with st.form(key='form2'): # Bike form
                bike_user = st.selectbox('Users',options=bike_usernames)
                bike_user_button = st.form_submit_button(label='Select User')
            if bike_user_button:
                if 'bike_user_button' not in st.session_state:
                    st.session_state['bike_user_button'] = True
                for i in data2:
                    if list(i.keys())[0] == bike_user:
                        val2 = i[bike_user][0]
                st.session_state.val2 = val2 # Saving for later - eval feedback
                for i in val2:
                    if i['Type'] == 'bike' and not i['isEvaluated']:
                        bikes.append(i['Bike'])

                for i in val2:
                    if i['Type'] == 'bike' and not i['isEvaluated']:
                        userbikes.append(i)
                    
                
                # print(val)
                # for i in val:
                #     if i['Type'] == 'bike' or not i['isEvaluated']:
                #         needed_data.append(i)
                
                        
        #######################################
                st.session_state.userbikes = userbikes # Used later for eval feedback form
                if len(userbikes) != 0:
                    i2 = userbikes[0] # Selecting the first form in the form data(which is the first uploaded one)
                    try:
                        st.session_state.val2.remove(i2)
                    except:
                        pass
                    st.session_state.i2 = i2
                    st.write(f'Bike : {i2["Bike"]}')
                    st.write(f'Brand : {i2["Bike_Brand"]}')
                    st.write(f'Kilometers Driven : {i2["Kilometers_Driven"]}')
                    st.write(f'City : {i2["City"]}')
                    st.write(f'Original Price : {i2["Original_Price"]}')
                    st.write(f'Owner Type : {i2["Owner_Type"]}')
                    st.write(f'Power : {i2["Power"]}')
                    st.write(f'Predicted Price : {i2["Predicted_price"]}')
                    st.write(f'Date of Request : {datetime.fromtimestamp(i2["Time_Stamp"]).date()}')
                    st.write(f'Year : {i2["Year"]}')
                    # Image display
                    desired_user_bike = usecase[bike_user]
                    st.session_state.desired_user_bike = desired_user_bike # Saving for later
                    test_user = db.get_user(desired_user_bike) # Getting user details
                    user_res = db.get_user(desired_user_bike) # Getting cur user details
                    user_images = user_res['images'] # Getting the name of images from user_db
                    # res_image = test_user['images'] # Getting image name from deta drive
                    arr2 = [] # Contains user specific images
                    for j in range(len(user_images)):
                        str_manip = f'bike-{i2["Bike"]}-'
                        if user_images[j].startswith(str_manip):
                            arr2.append(user_images[j])
                    if len(arr2) != 0:
                        arr = [] # Contains actual images
                        mark2 = """  """     # html dynamic image generate string
                        for k in range(len(arr2)):
                            im = drive.get(arr2[k])
                            contents = im.read()
                            data_url = base64.b64encode(contents).decode('utf-8')
                            if k == 0:  # If the image item is first one keep the first slide to active
                                des_str = f""" <div class="carousel-item active">
                                <img class="d-block w-100" src="data:image/png;base64, {data_url}" alt="First slide">
                                </div> """
                            elif k != 0:  # If the image item is not first one keep the -- keep the remaining slides without active tag
                                des_str = f""" <div class="carousel-item">
                                <img class="d-block w-100" src="data:image/png;base64, {data_url}" alt="First slide">
                                </div> """
                            mark2 += des_str



                        ######################################################################################### 
                        # Import bootstrap cdn to html  
                        mark1 = """ <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
                                    <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
                                <style>
                                    .carousel {{
                                    width:640px;
                                    height:360px;
                                    }}
                                    image{{
                                        height:640px;
                                        width:360px;
                                    }}
                                </style>
                                <div class="carousel-inner"> """
                        mark3 = """ </div>
                                <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
                                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                    <span class="sr-only">Previous</span>
                                </a>
                                <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
                                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                    <span class="sr-only">Next</span>
                                </a>
                                </div>

                                <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                                    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.3/dist/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
                                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script> """
                    
                        # html rendering
                        res_html = mark1 + mark2 + mark3
                        components.html(res_html, height=350, width=600)

                        #     file_bytes = np.asarray(bytearray(im.read()), dtype=np.uint8) # Converting image(deta object) to bytearray using numpy
                        #     opencv_image = cv2.imdecode(file_bytes, 1) # Decoding the bytearray to image(Byte stream)
                        #     arr.append(opencv_image)
                        # st.image(arr, channels = 'BGR', output_format='PNG', width=150)

                        # im = drive.get(res_image)
                        # im2 = drive.get(res_image2)
                        # file_bytes2 = np.asarray(bytearray(im2.read()), dtype=np.uint8)
                        # opencv_image2 = cv2.imdecode(file_bytes2, 1)
                        # arr = [opencv_image, opencv_image2]
                        # st.image(arr, channels = 'BGR', output_format='PNG', width=150)
                    
                    else: # if no pics
                        st.warning("User have not uploaded any images")
                    
                else: # If no cars to evaluate
                    st.warning("No bikes to evaluate for the selected user")

                    
                # Evaluator feedback form
            st.header("This is feedback form of evaluator")
            with st.form(key='feed_form_bike', clear_on_submit=True):
                feedback = st.text_input('Give feedback to the vehicle')
                evaluated_price = st.text_input('Evaluated Price')
                submit_button_feedback = st.form_submit_button(label='Submit Feedback')
                # alternate way
                # if 'submit_button_feedback' not in st.session_state:
                #     st.session_state.feedback = submit_button_feedback
                if submit_button_feedback and not evaluated_price == "" and not feedback == "":
                    # final form -> get the old form and modify it
                    final_form = st.session_state.i2
                    # final_userbikes -> form data which contains all the user forms in an array
                    final_userbikes = st.session_state.userbikes
                    new_form_data = {
                    "Bike": final_form['Bike'],
                    "Bike_Brand": final_form['Bike_Brand'],
                    "City": final_form['City'],
                    "Eval_Price": evaluated_price,
                    "Evaluator_Id": username,
                    "Feedback": feedback,
                    "Kilometers_Driven": final_form['Kilometers_Driven'],
                    "Original_Price": final_form['Original_Price'],
                    "Owner_Type": final_form['Owner_Type'],
                    "Power": final_form['Power'],
                    "Predicted_price": final_form['Predicted_price'],
                    "Time_Stamp": final_form['Time_Stamp'],
                    "Type": final_form['Type'],
                    "Year": final_form['Year'],
                    "isEvaluated": True
                    }
                    st.session_state.val2.append(new_form_data) # Appending the updated form data to the end
                    db.update_user(st.session_state.desired_user_bike, updates={'form_data':st.session_state.val2})
                    st.success("Feedback submitted!")

#############################################################################################################################

    if selected == 'Evaluated Vehicles':
        st.write("This is where evaluated vehicles stay")
        usecase = {user['name']:user['key'] for user in users}
        # All users
        all_users = {user['name']:user['key'] for user in users if not user['isEval']}
        col1, col2 = st.columns(2)
        with col1:
            with st.form(key='eval_form'):
                user = st.selectbox('Choose a User', options=list(all_users.keys()))
                vehicle_submit_button = st.form_submit_button('Choose')
            if vehicle_submit_button:
                users = db.fetch_all_users()
                our_users = [user for user in users if 'car' in user['type_data'] and not user['isEval']]
                data = [{l['name']:(l['form_data'], l['images'])} for l in our_users]
                user_key = all_users[user]
                des_user_data = [x for x in data if list(x.keys())[0] == user][0]
                des_user_form_data = des_user_data[user][0]
                final_data = [x for x in des_user_form_data if x['isEvaluated']]
                # Bootstrap cards and collapse combined for evaluated vehicles
                mark1 = """ <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous"> 
                        <style>
                            body{
                                margin-top:20px;
                                background:#FAFAFA;
                            }
                            .order-card {
                                color: #fff;
                            }

                            .bg-c-blue {
                                background: linear-gradient(45deg,#4099ff,#73b4ff);
                            }

                            .bg-c-green {
                                background: linear-gradient(45deg,#2ed8b6,#59e0c5);
                            }

                            .bg-c-yellow {
                                background: linear-gradient(45deg,#FFB64D,#ffcb80);
                            }

                            .bg-c-pink {
                                background: linear-gradient(45deg,#FF5370,#ff869a);
                            }


                            .card {
                                border-radius: 5px;
                                -webkit-box-shadow: 0 1px 2.94px 0.06px rgba(4,26,55,0.16);
                                box-shadow: 0 1px 2.94px 0.06px rgba(4,26,55,0.16);
                                border: none;
                                margin-bottom: 30px;
                                -webkit-transition: all 0.3s ease-in-out;
                                transition: all 0.3s ease-in-out;
                            }

                            .card .card-body {
                                padding: 25px;
                            }

                            .order-card i {
                                font-size: 26px;
                            }

                            .f-left {
                                float: left;
                            }

                            .f-right {
                                float: right;
                            }
                        </style>
                        """
                mark3 = """ <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                                        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.3/dist/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
                                        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
                                        <script>$("#demoAccordion").accordion({ collapsible: true, active: false});</script> """
                                        
                for form in final_data:
                    if form['Type'] == 'car':
                        mark2 = f""" <div id="accordion">

                            <div class="card bg-c-blue order-card">
                                <div class="card-header" id="headingOne">
                                <h5 class="mb-0">
                                    <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                    {form['Car']}
                                    </button>
                                </h5>
                                </div>

                                <div class="card-body">
                                    <blockquote class="blockquote mb-0">
                                        <div><i><small>Location : {form['Location']}</small></i></div>
                                        <div><i><small>Year : {form['Year']}</small></i></div>
                                        <div><i><small>Fuel Type : {form['Fuel_Type']}</small></i></div>
                                        <div><i><small>Kilometers Driven : {form['Kilometers_Driven']}</small></i></div>
                                    </blockquote>
                                </div>

                                <div id="collapseOne" class="collapse" aria-labelledby="headingOne" data-parent="#accordion">
                                <div class="card-body">
                                    <div><b>Description of Car</b></div>
                                    <div><em>Car Model : {form['Car']} </em></div>
                                    <div><em>Owner Type : {form['Owner_Type']} </em></div>
                                    <div><em>Fuel Type : {form['Fuel_Type']} </em></div>
                                    <div><em>Power : {form['Power']} </em></div>
                                    <div><em>Original Price : {form['Original_Price']}  </em></div>
                                    <div><em>Evaluated Price : {form['Eval_Price']} lakhs</em></div>
                                    <div><em>Predicted Price : {form['Predicted_price']} </em></div>
                                    <div><em>Evaluated by : {form['Evaluator_Id']} </em></div>
                                    <div><em>Feedback by Evaluator : {form['Feedback']} </em></div>
                                    <div><em>Submitted date for Evaluation : {datetime.fromtimestamp(form['Time_Stamp']).date()} </em></div>

                                </div>
                                </div>
                            </div> """

                    if form['Type'] == 'bike':
                        mark2 = f""" <div id="accordion">

                            <div class="card bg-c-green order-card">
                                <div class="card-header" id="headingOne">
                                <h5 class="mb-0">
                                    <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                    {form['Bike']}
                                    </button>
                                </h5>
                                </div>

                                <divrr class="card-body">
                                    <blockquote class="blockquote mb-0">
                                    <div><i><small>City : {form['City']}</small></i></div>
                                        <div><i><small>Year : {form['Year']}</small></i></div>
                                        <div><i><small>Bike Brand : {form['Bike_Brand']}</small></i></div>
                                        <div><i><small>Kilometers Driven : {form['Kilometers_Driven']}</small></i></div>
                                    </blockquote>
                                </div>

                                <div id="collapseOne" class="collapse" aria-labelledby="headingOne" data-parent="#accordion">
                                <div class="card-body">
                                    <div><b>Description of Bike</b></div>
                                    <div><em>Bike Model : {form['Bike']} </em></div>
                                    <div><em>Bike Brand : {form['Bike_Brand']} </em></div>
                                    <div><em>Owner Type : {form['Owner_Type']} </em></div>
                                    <div><em>Power : {form['Power']} </em></div>
                                    <div><em>Original Price : {form['Original_Price']}  </em></div>
                                    <div><em>Evaluated Price : {form['Eval_Price']}</em></div>
                                    <div><em>Predicted Price : {form['Predicted_price']} </em></div>
                                    <div><em>Evaluated by : {form['Evaluator_Id']} </em></div>
                                    <div><em>Feedback by Evaluator : {form['Feedback']} </em></div>
                                    <div><em>Submitted date for Evaluation : {datetime.fromtimestamp(form['Time_Stamp']).date()} </em></div>

                                </div>
                                </div>
                            </div> """
                    mark_html = mark1+mark2+mark3
                    components.html(mark_html, height=300, scrolling=True)

# Auth edge cases
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
