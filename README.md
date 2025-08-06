July 29th, 2025

Understanding the Code

main.py 
This file is where all the files in the project come together and where you launch the actual web application
To be able to open the website online, we have to import certain libraries to manage where and how the website is being run 
We ended up using flask, redirect, and session to set up the web routes and manage the user sessions
For allowing us to access our google accounts, we had to import google authorization libraries
To work with gmails, we had to import the gmail api that essentially allows access to the api 
The load_dotenv is imported to load environment variables from the .env file in the python environment
Environment variables are secret items, so they are stored outside of your source code
They live in the computer’s or server’s environment (like in system settings)
Json is imported because its a data format for storing structured information, its universal
The json libraries can be used to filter out the information provided in this format
base64 is the last thing you import from a readymade library, this is used to decode the gmails encoded messages

After the imports, you load the environment variables through a function load_dotenv(), which actually loads the env info
Then you need to actually make the web app instance through flask. This sets up everything like the routing and the serve pages
The instance is created through app = Flask(_name_)


August 3rd, 2025

After finishing step 5 (ranker.py file), we moved onto the next step where it can draft simple responses and email back. 
We are avoiding checking the entire context for now, and just focusing on simple drafts
Goal:
# v1 of this file will essentially check if the emails it accessed require a response
# if so, the file will draft an appropriate/professional response (assuming the context)
# This file will also need to prompt the user back some deterministic questions regarding the context
# i.e. it could ask whether "you" can go ahead with the interview, whether "you" can finalize the date
The second list in the response from the rank_emails function will have its locations directly corresponding to the most recently received email to the last. 
For example email x, y, z have been received (x being the earliest and z being the last). The rankings could be [0, 2, 1], making the most relevant email the email which was received most recently (email x) corresponding to a label of 0.
Now to determine which emails require a reply or not, the list will simply be determined in the same way the AI views them x, y, z. A possible reply list could be [1, 0 , 0], meaning email x requires further attention because it needs a response. 

August 6th, 2025

A modification to email_list we have to do is including the rank of an email in its respective “email_list.” Once that's figured out, we can display the actual emails in that specific order. If they are not accessible through this manner, (as an email id in email_list), it will be difficult to access it otherwise. 
