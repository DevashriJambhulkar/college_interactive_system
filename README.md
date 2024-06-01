# college_interactive_system
Instruction Manual for Opening and Running the Project
This manual provides step-by-step instructions for opening the project in VS Code, setting up the database in XAMPP, and running the project in a local browser.
## Prerequisites
1. Visual Studio Code (VS Code)
2. XAMPP Server
3. MySQL Workbench
Step 1: Open the Project folder named main in VS Code
- Click on `File` in the top menu bar.
- Select `Open Folder...`.
- Navigate to the location of your project folder and select it.
- Click `main`.
The project structure is like this:
main
├── .vscode
│ ├── launch.json
│ ├── settings.json
├── Forum
│ ├── _pychace_
│ ├── static
│ ├── templetes
│ ├── connection.py
└── mydatabase(1).sql
 Step 2: Set Up the Database in XAMPP
1. Start XAMPP:
- Open the XAMPP Control Panel from your applications or start menu.
- Start the `Apache` server by clicking the `Start` button next to it.
- Start the `MySQL` server by clicking the `Start` button next to it.
2. Access phpMyAdmin:
- Click on Admin in the row of MySQL or Open your web browser and go to `http://localhost/phpmyadmin`.
- In phpMyAdmin, create a new database named `mydatabase `.
- Import the ‘mydatabase’ database from the folder ‘main’.
 Step 3: Set Up and Run the Backend Server
1. Make sure that main folder is open.
2. Click on ‘connection.py’ under the explorer drop-down list:
3. Right click on the ‘connection.py’ and click on Run Python File in Terminal.
Step 4: Run the project on local browser:
1. In the terminal you’ll see the link. CTRL + click to follow the link.
2. The local server will look like this http://127.0.0.1:5000
3. By clicking ‘Explore’ you can explore my project.
By following these steps, you should be able to open the project in VS Code, set up the database in XAMPP, and run the project in a local browser.
