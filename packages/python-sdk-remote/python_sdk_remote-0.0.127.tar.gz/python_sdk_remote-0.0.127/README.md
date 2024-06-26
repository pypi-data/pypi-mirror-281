# python-sdk-package

https://github.com/grosser/repo_dependency_graph Ruby, Graph the dependencies of your repositories
https://github.com/thebjorn/pydeps Python

To create local package and remote package layers (not to create GraphQL and REST-API layers)

#database Python scripts in /db folder
Please place <table-name>.py in /db<br>
No need for seperate file for _ml table<br>
Please delete the example file if not needed<br>

# Create the files to create the database schema, tables, view and populate Meta Data and Test Date

/db/<table-name>.py - CREATE SCHEMA ... CREATE TABLE ... CREATE VIEW ...<br>
/db/<table-name>_insert.py to create records

# Update the setup.py (i.e.name, version)

# Please create test directory inside the directory of the project i.e. /<project-name>/tests

# Update the serverless.yml in the root directory

provider:
stage: play1

Update the endpoints in serverless.yml
