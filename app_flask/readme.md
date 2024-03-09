## Back End Flask Service Setup: <a name = "backend_setup"></a>
<b>Required software:</b> Python (3.11.4)

After cloning the entire project and setting up python in your machine:
1. Create a python venv in the `app_flask` directory
2. Within the app_flask directory install the required libraries:
    - run ```pip install -r requirements.txt```
3. To begin create a development environment, add the following block in `api.py` (ensure to remove it before deploying to production branch) #TODO include this in validation step during build
    ```
    if __name__ == '__main__':
        app.run(debug=True)
    ```
    - To deploy a local testing environment of the server run: ```python <path_to_app_flask>/api.py``` through your activated virtual environment.
        - It should create an environment you can begin testing at `http://127.0.0.1:5000/`
4. Create unit tests under the `app_flask/tests/ directory`  ensure you also run the existing unit tests before submitting:
    - ```python -m unittest discover -s tests```


NOTE:
known required packages:
firebase_admin
flask
cors