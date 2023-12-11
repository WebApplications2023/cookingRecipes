# Cooking Recipes
_Authors:_ Sophia Weiler & Oscar Benedek

_Project Description:_ Using Python, JavaScript, HTML, and SQLAlchemy, we created a social media-style cooking recipes flask app. Users are able to create accounts, add their recipes, and see other recipes that other uses have created. Additionally, collaboration is encouraged as other users are able to upload photos of their versions of recipes. Created locally using a sqlite database, people who are interesting in running our project should first create a python virtual environment using the following commands:  

    python3 -m venv venv
    . venv/bin/activate
From there, install the requirements.txt file with the command  

    pip install -r requirements.txt 
after pulling the code. Finally, activate a python interpreter by typing **python** in your terminal, and then create the sqlite db using the following commands:  

    from cookingRecipes import db, create_app
    app=create_app()
    with app.app_context():
        db.create_all()
There! Your database and environment should be properly set up. As a last step, exit your python interpreter and (within your virtual environment) type this command to run the cooking recipes app:  

    flask --debug --app=cookingRecipes run

_Purpose:_ Final project for UC3M Web Applications class developing an interactive Cooking Recipies website.

_Project specifications listed here: https://www.it.uc3m.es/jaf/wa/labs/project/_
