### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Final Project
 
 
# Project Title
 
#### Final Project NASA Space Image Explorer  
## Description
 
NASA Space Image Explorer is a Django web application using SQLite and Bootstrap that provides users with easy access to current space images and scientific data from NASA’s public APIs.

Key features include:

* Browse NASA’s Astronomy Picture of the Day with detailed info.
* Search NASA’s image library by keyword.
* Explore Earth images via EPIC Gallery with slideshow and favorites.
* View solar flare data on the DONKI Space Weather page.
* Track near-Earth asteroids and known exoplanets.
* Save favorites across the app with user accounts.

This project offers a clean, user-friendly interface for space enthusiasts and learners to explore NASA’s latest space imagery and mission information all in one place.


## Getting Started
 
### Dependencies
Before running the project, ensure you have:

* Python 3.10+ installed
* Required Python packages (install via requirements.txt)
* SQLite (bundled with Python)
* Bootstrap 5 for responsive UI (included via CDN or local files)
* pip package manager
 
### Installing

1. Clone the repository:

```
git clone https://github.com/fhsuae/finalprojectAlexanderEscobedo.git
```

2. Create and activate a virtual environment:

Windows:

```
python -m venv venv
venv\Scripts\activate
```
macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:

```
pip install -r requirements.txt
```
#### Environment Setup


This project requires a NASA API key to access NASA’s public data APIs. To keep your key safe and ensure the app works correctly, follow these steps carefully:

1. **Get a NASA API Key:**  

>Visit https://api.nasa.gov and sign up for a free API key. You will receive a string of letters and numbers — this is your unique key.

2. **Create a `.env` File:**  

>In the main project folder (the same folder where you see the file manage.py), create a new text file named `.env`.

3. **Add Your API Key to `.env`:**  

>Open `.env` and add the following line, replacing `your_actual_nasa_api_key` with the key you received:

```
NASA_API_KEY=your_actual_nasa_api_key
```

4. **Use the `.env.example` as a Template (Optional):**  

>There's a file named .env.example included in this project that shows the format of the .env file. 
You can copy it and rename it to .env to save time:

macOS/Linux (in your terminal):

```
cp .env.example .env
```
Windows (in PowerShell):

```
copy .env.example .env

```

>Then open .env and replace the placeholder with your actual API key.


5. **Why Use a `.env` File?**

> The `.env` file is not included in the project’s public code repository (it’s listed in .gitignore), so your API key stays private and won’t be shared accidentally.

6. **Make Sure to Activate Your Virtual Environment Before Running the App:**

> When you start working, remember to activate your virtual environment (see “Installing” section). This ensures the project can load all required packages including python-dotenv.

### Executing program

#### Initialize the database:

Ensure your working directory is the main Django project folder (nasaexplorer/) 
1. Generate database migration files:
```
python manage.py makemigrations
```
> Django inspects your models and creates migration files — these are instructions for creating or updating database tables.
2. Apply migrations to the database:

```
python manage.py migrate
```
>Executes the migration files, creating or updating the actual database schema in SQLite.

3. Create an admin (superuser) account:

```
python manage.py createsuperuser
```
> Creates a new administrative user to access Django’s built-in admin dashboard. You’ll be prompted for a username, email, and password.
> 
4. Start the Django development server:

```
python manage.py runserver
```

>Starts Django’s built-in web server so you can view and interact with your app locally.

Open your web browser and go to:

```
http://127.0.0.1:8000/
```


### Admin Access 

To access the Django admin dashboard:

1. Go to:

```
http://127.0.0.1:8000/admin/
```

2. Log in using the credentials created with:

```
python manage.py createsuperuser
```

You can manage:

*  User favorites (saved NASA images by logged-in users)
*  User accounts (admins only)


### Using an IDE (Optional)

If you are using an IDE like PyCharm or VS Code:

* Open the project folder
* Go to Edit Configurations → Add New Configuration → Django Server.
* Set working directory to the project folder
* Enable Django Support (if using Pycharm) and set root point to nasaexplorer directory
* Point to settings.py file in nasaexplorer/mysite/settings.py
* Set Manage script to manage.py file in nasaexplorer/manage.py
* Click the Run ▶️ button to start the development server.

This lets you run and debug the Django app with one click.

If you are using another program that utilizes port 8000, you may change the port number by editing configurations and entering a port number that is not in use (8001 for example).

You may also use this command:

```
python manage.py runserver 8001
```

### Project Pages 

* **Home Page**: Displays NASA's Astronomy Picture of the Day with detailed explanation and image.
* **EPIC Gallery**: Gallery of Earth images from NASA's DSCOVR satellite with slideshow and ability to favorite images.
* **Image Search**: Allows users to search NASA's Image and Video Library API for space images by keyword.
* **DONKI Space Weather**: Lists recent solar flare events with summary information.
* **Asteroids Page**: Shows near-Earth asteroid data including sizes, distances, and close approach dates.
* **Exoplanets Page**: Displays information about known exoplanets discovered to date.
* **Favorites Page**: Logged-in users can view, manage, and download their favorite NASA images.
* **Login**: User login page.
* **Signup**: New user registration page.
* **Logout**: Logs out the current user.

 
## Authors
 
Alexander Escobedo 
 
## Version History

* 0.1
    * Initial Release

## Acknowledgments

* [Django Documentation](https://docs.djangoproject.com/en/5.2/)
* [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/getting-started/download/)
* [The Official Django Tutorial](https://docs.djangoproject.com/en/5.2/intro/tutorial01/) - Project structure adapted from this tutorial (Django version 5.2)
* [SQLite Documentation](https://sqlite.org/docs.html)
* [NASA Open APIs Documentation](https://api.nasa.gov/)

