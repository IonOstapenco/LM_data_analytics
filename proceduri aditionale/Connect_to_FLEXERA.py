import webbrowser
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time



#driver  =webdriver.Chrome()

#driver.get("https://ibm.app.flexera.eu/login")

#time.sleep(3)  # --> asteptam sa incarce pagina

# cauta/ gaseste campuri (cu id reale din pagina webb)
#username = driver.find_element(By.ID, "okta-signin-username") # --> acesta pentru user name
#password = driver.find_element()



# se deschide browser
webbrowser.open('https://ibm.app.flexera.eu/login')

res = requests.get('https://ibm.app.flexera.eu/login')
"""
try:
    res.raise_for_status()
except Exception as exc:
    print('este o problema: %s' % (exc))  
    """  
