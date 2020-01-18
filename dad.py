import requests
import time
#import json
#import pandas

#from bs4 import BeautifulSoup
import requests
from selenium import webdriver

url = 'https://www.cms.gov/apps/physician-fee-schedule/search/search-criteria.aspx'

def pick_location():
    location_value = '0'
    while (True):
        number = input(
'''
Enter the number of your desired location (do not include the period):
1. Fort Lauderdale
2. Miami
3. Rest of Florida
Location: ''')
        if (number == '1'):
            location_value = "0910203"
            break
        elif (number == '2'):
            location_value =  "0910204"
            break
        elif (number == '3'):
            location_value =  "0910299"
            break
        else:
            print("Sorry. I didn't get that.") 
    return location_value

def submit():
    driver.execute_script('document.getElementById(\'ctl00_ctl00_ctl00_CMSGMainContentPlaceHolder_ToolContentPlaceHolder_PFSSContentPlaceHolder_submit\').click()')
    
#TO-DO: Error checking with inputs
year = input("Please enter a year: ")
code = input("Please enter a valid HCPCS Code: ")
mac_locality = pick_location()
inputs = input("Please enter your units : ")

print('''
Searching...
'''
)

#TEST
#year = '2018'
#code = '95851'
#mac_locality = "0910203"

year += ';'
code += ';'
mac_locality += '\'' + ';' 

# define scripts
year_script = 'let year = document.getElementById(\'ctl00_ctl00_ctl00_CMSGMainContentPlaceHolder_ToolContentPlaceHolder_PFSSContentPlaceHolder_YearDropDown\');year.value ='
code_script = 'let code = document.getElementById(\'ctl00_ctl00_ctl00_CMSGMainContentPlaceHolder_ToolContentPlaceHolder_PFSSContentPlaceHolder_HCPC1Textbox\');code.value ='
visible_block_script = 'let vis_block = document.getElementById(\'ctl00_ctl00_ctl00_CMSGMainContentPlaceHolder_ToolContentPlaceHolder_PFSSContentPlaceHolder_CarrierLocalityPanel\');vis_block.style = \'block\''
modifier_script = 'let modifier = document.getElementById(\'ctl00_ctl00_ctl00_CMSGMainContentPlaceHolder_ToolContentPlaceHolder_PFSSContentPlaceHolder_ModifierDropDown\');modifier.value = \'%\''
locality_script = 'let locality = document.getElementById(\'ctl00_ctl00_ctl00_CMSGMainContentPlaceHolder_ToolContentPlaceHolder_PFSSContentPlaceHolder_CarrierLocalityDropDown\');locality.value=\''

price_script = 'table = document.getElementById(\'ctl00_ctl00_ctl00_CMSGMainContentPlaceHolder_ToolContentPlaceHolder_PFSSContentPlaceHolder_ResultsControl1_PFSSGridView\');var title_strings = table.rows[1].cells[0].innerText.split(\'\\n\');for (i = 0; i < title_strings.length; i++) {title_strings[i] = title_strings[i].trim();}var index = title_strings.indexOf("NON-FACILITY PRICE");index -= 1;var price = document.getElementsByClassName("gridviewRow")[0].cells[index].innerText;return price'

#add user inputs
year_script += year
code_script += code
locality_script += mac_locality 

#options = webdriver.ChromeOptions()
#options.add_argument('headless')
#driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
driver.get(url)

#fill out all forms
driver.execute_script('document.getElementById(\'ctl00_ctl00_ctl00_CMSGMainContentPlaceHolder_ToolContentPlaceHolder_PFSSContentPlaceHolder_accept\').click()')
driver.execute_script(year_script)
#driver.execute_script('let element2 = document.getElementById(\'ctl00_ctl00_ctl00_CMSGMainContentPlaceHolder_ToolContentPlaceHolder_PFSSContentPlaceHolder_CarrierTypeRadioButtonList_2\');element2.checked=true')
driver.execute_script('document.getElementById(\'ctl00_ctl00_ctl00_CMSGMainContentPlaceHolder_ToolContentPlaceHolder_PFSSContentPlaceHolder_CarrierTypeRadioButtonList_2\').click()')
driver.execute_script(code_script)
#driver.execute_script(visible_block_script)
driver.execute_script(modifier_script)
driver.execute_script(locality_script)
submit()
driver.execute_script(modifier_script)
driver.execute_script(locality_script)
try:
    submit()
except:
    pass
try:
    price = driver.execute_script(price_script)
    #delete dollar sign
    price = price[1:]

    price = float(price)

    total_value = price * 2 * float(inputs)

    print("Your non-facility price is: $" + str(format(round(price,2), '.2f')))
    print("Your total value: $" + str(format(round(total_value,2), '.2f')))
except:
    print("This code is contractor priced under the Physician Fee Schedule. Please contact your local Medicare Contractor for payment amounts.")


#TODO
# Figure out the column to use. And replace the chrome driver with simple javascript

#Old news
#url_req = requests.get(url)
#soup = BeautifulSoup(url_req.content, 'lxml')
#col = soup.find('div', class_="column_main")
#col_all = col.find_all('a')
#for link in col_all:
#   print(link.get('href'))