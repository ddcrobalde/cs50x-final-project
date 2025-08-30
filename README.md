# CartGo

### Description
CartGo is a simple Flask application for managing a personal grocery list that comes with login functionality, item and quantity tracking, and status toggling, among others.

### Features
#### Registration and login
Users have the ability to register for an account and log in to the web application. The main reason this functionality was implemented is to allow for multiple user support, with the grocery list of each user being independent from each other. This means that same items across multiple users would be unaffected if a user modifies or removes these items.

Users may also save their grocery lists beforehand, and if, for example, specific items were not presently purchased, they may still save their existing grocery lists for a later date.

#### Add, edit quantity, or remove items
Once the user is logged in, they can add items to the grocery list through the fields at the top of the page, wherein they must indicate the name of the item and its corresponding quantity. If the user enters an item already existing in the list, it will then be added to that item's existing quantity.

Below the input fields for adding items, the grocery list is displayed as a table with four columns. The `Status` column indicates if the item has already been added to the cart, which can be updated in real time. The `Item` column displays the name of the item, while the `Quantity` column indicates its current quantity. The value indicated in the `Quantity` column can also be modified for each item in the list, so that the user need not remove the item altogether and add it back with the desired quantity. The `Action` column hosts a button which allows the user to remove an item and its current quantity from the list.

#### Toggle item status
This feature, located in the `Status` column, allows the user to check off an item once it is added to the cart. If the checkbox is ticked, the item name in the `Item` column will become strikethrough text, and the color of the entire row corresponding to that item will change from light blue to light gray, allowing for easier reference.

#### Sort items
This feature, which uses a select menu, allows the user to sort the items displayed in the table, with the available options being sort by `Name`, `Quantity` (ascending or descending), `Status` (i.e., is the item added to the cart or not yet), and `Date Added` (default). This is especially useful for longer lists, where, for example, the user might decide to sort the items based on `Status` in order to quickly determine the items yet to be added to the cart or purchased.

#### Clear entire list
Once the user is done with the current grocery list, or for any other reason, they can clear the entire list using the `Clear List` button at the bottommost part of the page.

### Project files
The project files includes the main implementation in `app.py`, another python file for the helper functions named `helpers.py`, a SQLite database schema named `schema.sql`, a list of dependencies in `requirements.txt`, the `templates` folder which includes all of the templates used for this application, and the `static` folder containing `styles.css`.
* `app.py` - contains the routes of the application that implements the various features specified above. The routes include the index `/` where the list is displayed; `/add` for adding items to the list; `/clear` for clearing the entire list; `/edit` for editing the quantity of a specific item; `/login`, `/logout`, and `/register`, which were adapted from CS50 Finance to allow a user to register and log in to the app; `/remove` to remove a specific item from the list; and `/toggle` to toggle the status of an item.
* `helpers.py` - contains various helper functions for `app.py`, including rendering error templates, a helper function for creating a connection to the SQLite database, and the login_required decorator, which was also adapted from CS50 Finance.
* `schema.sql` - a SQLite database schema with two tables: `users` for storing user info including username and password hash, and `lists` which stores the grocery lists of each user.
* `requirements.txt` - a list of Python packages the project depends on, which includes `flask`, `flask-session`, and `python-dotenv`, the latter of which I used to set environment variables for the Flask project.
* `templates` - contains the templates used in the project, which includes `layout.html`, `index.html`, `register.html`, `login.html`, and `error.html`.
* `static` - contains `styles.css` or the CSS code for the web pages.

### Frameworks, libraries, and tools
* Python 3.13
* Flask, Flask-Session
* SQLite
* HTML, JavaScript, CSS, Bootstrap
* Werkzeug (for password hashing)
* Black, Prettier (for code formatting)

### Installation
In order to run the app locally:
1. Save the project files in a local repository.
2. Create a virtual environment using `py -m venv venv` and activate it using `venv\Scripts\activate` (for Windows) or `source venv/bin/activate` (for macOS/Linux).
3. Install the dependencies using `pip install -r requirements.txt`.
4. Create a new SQLite database file named `grocery.db` using `sqlite3 grocery.db < schema.sql`.
5. Run the app using `flask run`.

### Usage
1. Once the app is running locally, access it using port 5000.
2. Register a new user. If an existing user, log in.
3. In the grocery list, add, edit, or remove items.
4. Sort items based on your preference.
5. Toggle each item's status if they have already been added to the cart or purchased.
6. Once done with the grocery list, clear all items and logout.

### Acknowledgments
This Flask application was submitted as the final project for **CS50x 2025** and developed with guidance from the CS50 staff, course materials, and lectures. It also incorporates concepts from previous problem sets, most notably **CS50 Finance**.  

Additional resources include **Bootstrap** for webpage design, **Werkzeug** for password hashing, and formatting tools such as **Black** and **Prettier**.  

Some assistance was provided by **ChatGPT** and **GitHub Copilot** during development.
