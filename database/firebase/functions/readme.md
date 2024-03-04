

# running tests

currently using unittest to run unit tests for these python cloud funcs. 

to run the mandatory testsuite, nagivate to the database/firebase/functions directory and run:
`python -m unittest discover -s tests`

to run individual module unittests, stay in the functions directory and update the arguement to the module you want to test for example:
`python -m unittest discover -s logic/tests`

tag [cloud_functions] in your pull request to  execute only the cd pipeline for cloud functions (otherwise you will be running the entire project's test suite.)


# Deploying Functions
on venv run
`firebase deploy --only functions`