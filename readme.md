# DDiligence
A parody application to help financiers make correlations with historic stock data and other historic data such as weather data, space weather, etc.

## Table of Contents
1. [Development Setup](#setup)
    - [Back End Flask Service Setup](#backend_setup)
    - [Front End React Client Setup](#frontend_setup)
    - [Database & Filesystem Setup](#db_setup)
    - [Build & Deployment Setup](#bnd_setup)
    - [CI/CD Testing Workflow Setup](#testing_setup)


# Setup <a name = "setup"></a>
This is a monorepo of the ddiligence project. Clone the repo and refer to each subproject's readme.md for more details
TODO create new readmes for each service.

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

## Front End React Client Setup: <a name="frontend_setup"></a>
Required software: Node.js, npm
after cloning the project
1. within the client_react directory:
    - run ```npm install```
        - this should automatically install the required npm packages
2. To deploy a local testing environment of the server run: ```npm start```
    - It should create an environment you can begin testing at ```http://localhost:3000```

## Database & Filesystem Setup <a name="db_setup"></a>

## Build & Deployment Setup <a name="bnd_setup"></a>
additional files for the final deployed project
1. images & icons (TODO figure out how to handle serving final files during deployment step)


## CI/CD Workflow Setup <a name="testing_setup"></a>
located in the `.github/workflows/` directory


# TODO generate documentation for each component
