# COMS 4170 UI Design Final Project (tdt2128, fvc2109, ik2536, pa2658)

To generate a private key for the Firebase:
- In Firebase Console, go to Project Settings → Service Accounts
- Click Generate New Private Key
- Download the JSON file
- Rename it to: UIserviceAccountKey.json
- Place it in the root directory of this project

Then rename the .env.example file in this repo to .env

And for running the server, make use firebase-admin and dotenv are installed:
- pip install firebase-admin
- pip install dotenv

The server should be able to run after that!
