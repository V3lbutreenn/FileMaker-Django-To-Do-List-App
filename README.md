# FileMaker To Do List

## About the Project

The application named **FileMaker To Do List** was developed to demonstrate data management between Django and a FileMaker database via an ODBC connection.

---

## Technologies Used

* **Backend:** Django (Python)  
* **Database:** FileMaker (via ODBC connection)  
* **Frontend:** HTML, CSS, JavaScript  

---

## Installation Instructions

To run this project locally, the following requirements must be met.

### Requirements

* **Python:** The project has been tested with Python 3.13 and above.  
* **FileMaker:** FileMaker Pro must be installed for the database.  
* **FileMakerODBC:** The official FileMaker ODBC driver must be installed to connect Python to the FileMaker database. (For installation details, please refer to FileMaker’s official documentation.)  
* **FileMaker Pro License:** An active FileMaker Pro license or subscription is required to access the database.  

### Steps

1. **Install Dependencies:** Install the Python libraries listed in the **`requirements.txt`** file located in the project root directory.  

    ```bash
    pip install -r requirements.txt
    ```

2. **Configure the FileMaker Database:**  
    * After installing the FileMaker ODBC driver, create a **Data Source Name (DSN)** called **'todolistwebuser'** in the **ODBC Manager**.  
    * Configure this DSN with the username and password of the **`todolistuser`** defined in the database.  
    * The `.fmp12` file must remain open for the project to run.  

3. **Check Connection Settings:**  
    * Open the **`utils.py`** file.  
    * Ensure that the `FM_DSN_NAME`, `FM_USERNAME`, and `FM_PASSWORD` variables match your DSN configuration and the `todolistuser` credentials.  

4. **Start the Django Server:**  

    ```bash
    python manage.py runserver
    ```

5. **Note:** Static files are served directly from the `Static/` folder, and there is no separate build process for the frontend.  

---

## Known Limitations

* There is no user feedback system (success, warning, error messages) after operations.  
* Database connection errors are not displayed in the user interface.  

---

## 📄 License

This project is licensed under the MIT License. See the **`LICENSE`** file for details.  

