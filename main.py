import streamlit as st
import requests
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import time


# ---data for selecting in the form---
carlist = ('Maruti Wagon', 'Hyundai Creta', 'Honda Jazz', 'Maruti Ertiga', 'Audi A4', 'Nissan Micra', 'Toyota Innova', 'Volkswagen Vento', 'Tata Indica', 'Maruti Ciaz', 'Honda City', 'Maruti Swift', 'Land Rover', 'Mitsubishi Pajero', 'Honda Amaze', 'Renault Duster', 'Mercedes-Benz New', 'BMW 3', 'Audi A6', 'Hyundai i20', 'Maruti Alto', 'Toyota Corolla', 'Mahindra Ssangyong', 'Maruti Vitara', 'Mahindra KUV', 'Mercedes-Benz M-Class', 'Volkswagen Polo', 'Tata Nano', 'Hyundai Elantra', 'Hyundai Xcent', 'Hyundai Grand', 'Renault KWID', 'Hyundai i10', 'Maruti Zen', 'Ford Figo', 'Mahindra XUV500', 'Nissan Terrano', 'Honda Brio', 'Ford Fiesta', 'Hyundai Santro', 'Tata Zest', 'Maruti Ritz', 'BMW 5', 'Toyota Fortuner', 'Ford Ecosport', 'Hyundai Verna', 'Maruti Omni', 'Toyota Etios', 'Jaguar XF', 'Maruti Eeco', 'Honda Civic', 'Mercedes-Benz B', 'Mahindra Scorpio', 'Honda CR-V', 'Chevrolet Beat', 'Skoda Rapid', 'Mercedes-Benz S', 'Skoda Superb', 'Hyundai EON', 'BMW X5', 'Chevrolet Optra', 'Mercedes-Benz E-Class', 'Maruti Baleno', 'Skoda Laura', 'Skoda Fabia', 'Tata Indigo', 'Audi Q3', 'Skoda Octavia', 'Mini Cooper', 'Hyundai Santa', 'BMW X1', 'Hyundai Accent', 'Mercedes-Benz GLE', 'Maruti A-Star', 'BMW X3', 'Ford EcoSport', 'Audi Q7', 'Volkswagen Jetta', 'Mercedes-Benz GLA', 'Maruti Celerio', 'Honda Accord', 'Tata Manza', 'Chevrolet Spark', 'Maruti 800', 'Mercedes-Benz GL-Class', 'Mahindra Bolero', 'Audi Q5', 'Ford Endeavour', 'Maruti SX4', 'Toyota Camry', 'Honda Mobilio', 'Fiat Linea', 'Jeep Compass', 'Ford Ikon', 'Chevrolet Aveo', 'Mahindra Xylo', 'Nissan Sunny', 'Maruti Dzire', 'Chevrolet Cruze', 'Volkswagen Ameo', 'Mercedes-Benz CLA', 'Tata Tiago', 'BMW 7', 'Hyundai Getz', 'Hyundai Elite')
loclist = ('Mumbai', 'Pune', 'Chennai', 'Coimbatore', 'Jaipur', 'Kochi', 'Kolkata', 'Delhi', 'Bangalore', 'Hyderabad', 'Ahmedabad')
yearlist = ('less than 2003', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022')
ownerlist = ('First', 'Second', 'Third or later')
fuellist = ('CNG', 'Diesel', 'Petrol')


# ---Data for decoding---
dctcar = {'Maruti Wagon': 67, 'Hyundai Creta': 32, 'Honda Jazz': 29, 'Maruti Ertiga': 61, 'Audi A4': 0, 'Nissan Micra': 80, 'Toyota Innova': 100, 'Volkswagen Vento': 104, 'Tata Indica': 90, 'Maruti Ciaz': 58, 'Honda City': 27, 'Maruti Swift': 65, 'Land Rover': 46, 'Mitsubishi Pajero': 79, 'Honda Amaze': 24, 'Renault Duster': 83, 'Mercedes-Benz New': 76, 'BMW 3': 5, 'Audi A6': 1, 'Hyundai i20': 43, 'Maruti Alto': 55, 'Toyota Corolla': 97, 'Mahindra Ssangyong': 50, 'Maruti Vitara': 66, 'Mahindra KUV': 48, 'Mercedes-Benz M-Class': 75, 'Volkswagen Polo': 103, 'Tata Nano': 93, 'Hyundai Elantra': 34, 'Hyundai Xcent': 41, 'Hyundai Grand': 37, 'Renault KWID': 84, 'Hyundai i10': 42, 'Maruti Zen': 68, 'Ford Figo': 21, 'Mahindra XUV500': 51, 'Nissan Terrano': 82, 'Honda Brio': 25, 'Ford Fiesta': 20, 'Hyundai Santro': 39, 'Tata Zest': 95, 'Maruti Ritz': 63, 'BMW 5': 6, 'Toyota Fortuner': 99, 'Ford Ecosport': 18, 'Hyundai Verna': 40, 'Maruti Omni': 62, 'Toyota Etios': 98, 'Jaguar XF': 44, 'Maruti Eeco': 60, 'Honda Civic': 28, 'Mercedes-Benz B': 69, 'Mahindra Scorpio': 49, 'Honda CR-V': 26, 'Chevrolet Beat': 12, 'Skoda Rapid': 88, 'Mercedes-Benz S': 77, 'Skoda Superb': 89, 'Hyundai EON': 33, 'BMW X5': 10, 'Chevrolet Optra': 14, 'Mercedes-Benz E-Class': 71, 'Maruti Baleno': 56, 'Skoda Laura': 86, 'Skoda Fabia': 85, 'Tata Indigo': 91, 'Audi Q3': 2, 'Skoda Octavia': 87, 'Mini Cooper': 78, 'Hyundai Santa': 38, 'BMW X1': 8, 'Hyundai Accent': 31, 'Mercedes-Benz GLE': 74, 'Maruti A-Star': 54, 'BMW X3': 9, 'Ford EcoSport': 17, 'Audi Q7': 4, 'Volkswagen Jetta': 102, 'Mercedes-Benz GLA': 73, 'Maruti Celerio': 57, 'Honda Accord': 23, 'Tata Manza': 92, 'Chevrolet Spark': 15, 'Maruti 800': 53, 'Mercedes-Benz GL-Class': 72, 'Mahindra Bolero': 47, 'Audi Q5': 3, 'Ford Endeavour': 19, 'Maruti SX4': 64, 'Toyota Camry': 96, 'Honda Mobilio': 30, 'Fiat Linea': 16, 'Jeep Compass': 45, 'Ford Ikon': 22, 'Chevrolet Aveo': 11, 'Mahindra Xylo': 52, 'Nissan Sunny': 81, 'Maruti Dzire': 59, 'Chevrolet Cruze': 13, 'Volkswagen Ameo': 101, 'Mercedes-Benz CLA': 70, 'Tata Tiago': 94, 'BMW 7': 7, 'Hyundai Getz': 36, 'Hyundai Elite': 35}
dctloc = {'Mumbai': 9, 'Pune': 10, 'Chennai': 2, 'Coimbatore': 3, 'Jaipur': 6, 'Kochi': 7, 'Kolkata': 8, 'Delhi': 4, 'Bangalore': 1, 'Hyderabad': 5, 'Ahmedabad': 0}
dctyear = {'2022':20,'2021':19,'2020':18,'2019':17,"2018":16,"2017":15,"2016":14,"2015":13,"2014":12,"2013":11,"2012":10,"2011":9,"2010":8,"2009":7,"2008":6,"2007":5,"2006":4,"2005":3,"2004":2,"2003":1,"less than 2003":0}
dctowner = {'First':2, 'Second':1, 'Third or later':0}
dctfuel = {'CNG':0, 'Diesel':1, 'Petrol':0}



# set page config
st.set_page_config(page_title='TVS CREDIT Vehicle Valuation', page_icon='./logo/api.png', layout='wide')

html = f"""<a href='{'https://www.tvscredit.com/'}'><img src='https://www.tvscredit.com/media/1927/tvs-credit-logo-01.png' width='200' height='50'></a>"""
st.markdown(html, unsafe_allow_html=True)

# st.image('./logo/tvs_logo.png')

    

with st.sidebar:
    selected = option_menu(
        menu_title = 'Menu',
        options = ['Home', 'Car', 'Bike', 'Contact'],
        icons = ['house', '', 'bicycle', 'envelope'],
        menu_icon = 'cast',
    )

# Home Page
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
if selected == 'Car':
    st.header('SELL YOUR CAR AT THE BEST PRICE')
    # Form to take data from user
    col1, col2 = st.columns(2)
    with col1:
        with st.form(key='form1'):
            # car = st.text_input('Car Model')
            car = st.selectbox('Car Model', options=carlist)
            car = dctcar[car]
            # location = st.text_input('Location')
            location = st.selectbox('Location', options=loclist)
            location = dctloc[location]
            # year = st.text_input('Year')
            year = st.selectbox('Year', options=yearlist)
            year = dctyear[year]
            km_driven = st.text_input('Kms Driven (Enter accurate value for better results)')
            # owner_type = st.text_input('Owner Type')
            owner_type = st.selectbox('Owner Type', options=ownerlist)
            owner_type = dctowner[owner_type]
            # fuel_type = st.text_input('Fuel Type')
            fuel_type = st.selectbox('Fuel Type', options=fuellist)
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
    with col2:
        def load_lottieurl(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            else:
                return r.json()
        lottie_api = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_kqfglvmb.json')
        st_lottie(lottie_api, height=500, key='api')


if selected == 'Bike':
    st.title(f'You have selected{selected}')
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
