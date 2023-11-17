base project setup:
project currently contains individual components:
    - React front end:
    - Flask back end service:
    - Database:
    - Tests
        - front end unit tests
        - flask unit tests
        - github actions test automation




# 1. Back End Flask Service Setup:
Required software: python
after cloning the entire project and setting up python in your machine:
1. create a python venv in the app_flask directory
2. within the app_flask directory:
    - run ```pip install -r requirements.txt```
3. to begin development, add the following block in server.py (ensure to remove it before deploying to production branch) #TODO include this in validation step during build
    ```
    if __name__ == '__main__':
        app.run(debug=True)
    ```
4.
5. Ensure your python interpreter is set correctly to the venv during development
6. Run unit tests:
    - ```python -m unittest discover -s tests```

# 2. front end setup:
Required software: Node.js, npm
after cloning the project
1. within the client_react directory:
    - run ```npm install```
        - this should automatically install the required npm packages
2. to begin testing the environment:
    - run ```npm start```
        - this should automatically start a development server in ```http://localhost:3000```

database setup:


testing setup:


deployment setup:



# Misc setup:
additional files for the final deployed project
1. images & icons (TODO figure out how to handle serving final files during deployment step)


