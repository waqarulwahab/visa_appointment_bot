import streamlit as st
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import time
from zenrows import ZenRowsClient
from datetime import datetime


st.set_page_config(layout="wide")
st.title("Germany Visa Appointment BOT")

# Load secrets
sender_email    = st.secrets["email"]["sender_email"]
password        = st.secrets["email"]["password"]
receiver_emails = st.secrets["receiver"]["receiver_emails"]
scraperapi_key  = st.secrets["scraper"]["api_key"]

# Function to check the div count
def check_div_count(url, headers):
    try:
        # st.write("TRY EXECUTE")
        client = ZenRowsClient("407ac46574b7d648d46d6fe1d2f030cdcba7105e")
        url = "https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kara&realmId=771&categoryId=1416"
        response = client.get(url)

        # response = requests.get(f"http://api.scraperapi.com?api_key={scraperapi_key}&url={url}", headers=headers)
        # st.write(response.status_code)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            wrapper_div = soup.find('div', class_='wrapper')
            captcha = soup.find('captcha')
            div_count = len(wrapper_div.find_all('div'))
            return div_count
        else:
            st.error(f"Error with Status code {response.status_code}")
    except requests.RequestException as e:
        st.sidebar.error("App Stopped")
        logging.error(f"Failed to retrieve the webpage. Error: {e}")
        return None

# Function to send email
def send_email(message, sender_email, receiver_emails, password):
    # Check if the essential credentials are set
    if not sender_email or not receiver_emails or not password:
        logging.error("Email credentials not set.")
        return

    # Loop through each receiver email
    for receiver_email in receiver_emails:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Visa Categories Updated"
        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            st.sidebar.info(f"Email sent successfully to {receiver_email}.")
            logging.info(f"Email sent successfully to {receiver_email}.")
        except Exception as e:
            logging.error(f"Failed to send email to {receiver_email}. Error: {e}")

def main():
    url = "https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kara&realmId=771&categoryId=1416&dateStr=24.10.2024"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # scraperapi_key = st.sidebar.text_input("SCRAPER API")

    max_iterations         = st.sidebar.number_input("Enter Maximum No. Of Iterations..", step=5, value=50)
    waiting_time_in_mins   = st.sidebar.number_input("Waiting Time In Mins..", value=6)

    waiting_time_in_sec = waiting_time_in_mins * 60

    col1 , col2    = st.sidebar.columns([1,1])
    with col1:
        start_button = st.button("START")
    with col2:
        stop_button  = st.button("STOP")


    if 'iteration_count' not in st.session_state:
        st.session_state['iteration_count'] = 0

    st.sidebar.info(f"Iteration Count: {st.session_state['iteration_count']}")
    
    if start_button and max_iterations:
        st.title("LOGS")

        while st.session_state['iteration_count'] < max_iterations:

            st.session_state['iteration_count'] += 1
            div_count = check_div_count(url, headers)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.write(f"No Visa Found , {div_count} Div Found at {current_time}")

            if div_count is not None:
                if div_count != 110:
                    message = f"The number of visa categories have been changed."
                    send_email(message, sender_email, receiver_emails, password)
                    st.success(f"Email Send Successfully to {receiver_emails}")
                else:
                    logging.info(f"No change in div count. Current count: {div_count}")
            else:
                logging.error("Could not retrieve the div count.")
            time.sleep(waiting_time_in_sec)

        st.sidebar.info("Reached maximum iterations. Stopping the loop.")



    elif stop_button:
        st.session_state.clear()  # This will clear all session variables
        st.sidebar.success("Application is stopped")

if "__main__":
    main()





# http://api.scraperapi.com?api_key=83b5f03c34f9a50d4e6ec8c81cebdef0&url=https://service2.diplo.de/rktermin/extern/appointment_refreshCaptchamonth.do
# https://service2.diplo.de/rktermin/extern/choose_realmList.do?locationCode=isla&request_locale=en
# https://service2.diplo.de/rktermin/extern/appointment_refreshCaptchamonth.do
# https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kara&realmId=771&categoryId=1416&dateStr=23.10.2024



# https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kara&realmId=771&categoryId=1416&dateStr=03.10.2024

# http://api.scraperapi.com?api_key=83b5f03c34f9a50d4e6ec8c81cebdef0&url=https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kara&realmId=771&categoryId=1416&dateStr=03.10.2024


# https://service2.diplo.de/rktermin/extern/choose_category.do?locationCode=kara&realmId=771&categoryId=1416
# https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kara&realmId=771&categoryId=1416

# AFTER CAPTCHA

# https://service2.diplo.de/rktermin/extern/appointment_showMonth.do


# AFTER CAPTCHA SPECIFIC MONTH

# https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kara&realmId=771&categoryId=1416&dateStr=24.10.2024