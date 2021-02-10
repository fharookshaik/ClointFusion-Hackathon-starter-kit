import ClointFusion as cf
import os
import pyperclip
from time import sleep,ctime
from tempfile import gettempdir
from configparser import ConfigParser
import re


cf.OFF_semi_automatic_mode()

def check_email(email):
    try:
        # Used RFC 5322 Official Standard General Email Validation regex.
        email_regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.search(email_regex, email):
            return True
        else:
            return False

    except Exception as ex:
        print("Error Validating email " + str(ex))



def read_config(filename='config.ini',section='google'):
    try:
        parser = ConfigParser()
        parser.read(filename)
        
        details = {}
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                details[item[0]] = item[1]

            # print(details)

        else:
            raise Exception('{0} not found in {1} file'.format(section,filename))

        return details
    
    except Exception as ex:
        print("Error in reading config file: " + str(ex))


def get_exe_file():
    try:
        operatingsystem = os.name
        if operatingsystem == 'nt':
            cf.message_counter_down_timer(strMsg='Generating bat file',start_value=3)
            bat_temp_file = gettempdir() + '\Cloint.bat'

            with open(bat_temp_file,'w+') as fp:
                fp.write('@ECHO OFF')
                fp.write('\n start cmd /c "pip install --upgrade jupyter_http_over_ws>=0.0.7 && jupyter serverextension enable --py jupyter_http_over_ws" ')
                fp.write('''\n start cmd /k "TITLE ClointSetup & jupyter notebook --NotebookApp.open_browser=False --NotebookApp.allow_origin='https://colab.research.google.com' --port=8888 --NotebookApp.port_retries=0" ''')
        
                fp.close()

            return bat_temp_file
        
    except Exception as ex:
        print("Error in Generating exe " + str(ex))

def getToken():
    try:
        token = None
        cf.message_counter_down_timer(strMsg='Extracting Token',start_value=3)
        cf.scrape_save_contents_to_notepad(folderPathToSaveTheNotepad=gettempdir())
        notepadPath = gettempdir() + r'\\notepad-contents.txt'
        f = open(notepadPath,'r')
        word = 'localhost:8888'
        tokenlist = []
        for line in f:
            if word in line.split('/'):
                tokenlist.append(line)
                        
        f.close()

        token = tokenlist[-1]        
        print("Token: " + token)        
        pyperclip.copy(token)
                
        if token != None:
            cf.message_pop_up(strMsg='Token Extracion Sucess',delay=3)
            sleep(5)
            return token
        else:
            cf.message_pop_up(strMsg='Token Extraction Failed Please close Everything and Try again',delay=10)

    except Exception as ex:
        print("Error in extracting token: " + str(ex))

def launch_website(token):
    try:

        d = read_config()
        # print(d)
        email = d['email']
        passwd = d['password']
                    
        if check_email(email):
            print("Valid Email found",email)
        else:
            email = cf.gui_get_any_input_from_user(msgForUser="Email Validation Failed. Please Enter Your email")

        if passwd == '' or passwd == 'yourpassword':
                passwd = cf.gui_get_any_input_from_user(msgForUser="Password not entered or Password Extraction failed. Please Enter your password to continue")
        else:
            print("Password Extraction Successful")

        cf.message_counter_down_timer(strMsg='Opening Browser',start_value=3)
        if cf.launch_website_h('https://colab.research.google.com/drive/1ZUpWVJCquGVK2B6T6e3_NK1xPwb2OeBo?usp=sharing'):
            cf.browser_mouse_click_h('Sign in')
            cf.browser_write_h(Value=email,User_Visible_Text_Element='Email or phone')
            cf.browser_mouse_click_h(User_Visible_Text_Element='Next')
            cf.browser_wait_until_h(text='Enter Your password')
            cf.browser_write_h(Value=passwd,User_Visible_Text_Element='Enter your password')
            cf.browser_mouse_click_h(User_Visible_Text_Element='Next')

            cf.mouse_click(*cf.mouse_search_snip_return_coordinates_x_y('images/downClick.png'),single_double_triple='single')
            cf.mouse_click(*cf.mouse_search_snip_return_coordinates_x_y('images/connectLocal.png'),single_double_triple='single')
            cf.key_press(strKeys='ctrl + a')
            cf.key_write_enter(strMsg=token,delay=0.5)
            cf.mouse_click(*cf.mouse_search_snip_return_coordinates_x_y('images/connect.png'),single_double_triple='single')

            sleep(5)
            cf.message_flash(msg=f'Success. Start Hacking {cf.show_emoji()}',delay=10)

    except Exception as ex:
        print("Error opening the Chrome Browser " + str(ex) + ". Please Close all the opened applications and try again.")

if __name__ == "__main__":
    try:
        operatingSystem = os.name

        if operatingSystem == 'nt':
            cf.window_show_desktop()
            cf.message_counter_down_timer(strMsg='Starting Process',start_value=5)

            exefile= get_exe_file()

            cf.launch_any_exe_bat_application(pathOfExeFile=exefile)

            sleep(4)

            l = cf.window_get_all_opened_titles_windows()

            jupyterNotebookwindow,cmdwindow = None,None

            for i in l:
                # if i[:9] == "Home Page":
                #     jupyterNotebookwindow = i
                if i[:11] == "ClointSetup":
                    cmdwindow = i
            # cf.window_minimize_windows(windowName=jupyterNotebookwindow)
            cf.window_activate_and_maximize_windows(windowName=cmdwindow)

            token = getToken()
            launch_website(token)
    
    except Exception as ex:
        print("Unexpected Exception occured " + str(ex))