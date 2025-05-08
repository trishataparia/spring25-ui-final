# COMS 4170 UI Design Final Project (tdt2128, fvc2109, ik2536, pa2658)

To generate a private key for the Firebase:
- In Firebase Console, go to Project Settings → Service Accounts
- Go to the Firebase Admin SK panel
- Click the "Generate new private key" button
- Download the JSON file
- Rename it to: UIserviceAccountKey.json
- Move the file into project directory, outside of the static and template folders (so in the same place as server.py)

Then rename the .env.example file to .env

And for running the server, make use firebase-admin and dotenv are installed:
- pip install firebase-admin
- pip install dotenv

The server should be able to run with "python server.py" now!

Additionally, to check the collected user data, please go to /debug page.
This provides information for when a user entered each lesson page and each review page.
