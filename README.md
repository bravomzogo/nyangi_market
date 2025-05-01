# NyangiProject

NyangiProject is a Django-based web application designed to facilitate online market operations. The project is structured to include various components such as media management, application logic, and static files for a seamless user experience.

## Project Structure

The project is organized as follows:

- **media/**: Contains documents, signatures, and stamps.
- **nyangi_market/**: The main Django project folder, which includes:
  - `db.sqlite3`: The SQLite database file.
  - `manage.py`: Django's command-line utility for administrative tasks.
  - `requirements.txt`: Lists the Python dependencies for the project.
  - `settings.py`: Configuration settings for the Django project.
  - **lplp/**: Virtual environment for the project.
    - `bin/`: Contains executables like `python`, `pip`, and activation scripts.
    - `lib/`: Includes Python libraries.
  - **media/**: Stores product images and other media files.
  - **myapp/**: A Django app with the following components:
    - `models.py`: Defines the database models.
    - `views.py`: Handles the application logic.
    - `templates/`: Contains HTML templates for the app.
    - `static/`: Holds static files like CSS and JavaScript.
  - **online_market/**: Another Django app for managing the online market.
  - **staticfiles/**: Stores static files for the admin interface and other components.

## Features

- **Media Management**: Handles product images and other media files.
- **Django Admin**: Provides an administrative interface for managing the application.
- **Localization**: Includes translation files for multiple languages.
- **Virtual Environment**: Isolated Python environment for managing dependencies.

## Getting Started

1. Clone the repository.
2. Activate the virtual environment located in `nyangi_market/lplp/`.
3. Install dependencies using `pip install -r requirements.txt`.
4. Run the development server with `python manage.py runserver`.

## Contact

For inquiries, contact us at customer1@gmail.com.