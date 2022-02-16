# Project Title

CS50's Web Programming with Python and JavaScript Project 4 - Networks

## Project Description

This project is the 4th assignment for a CS50 course mentioned in the title. The details of the assignment can be found here - [https://cs50.harvard.edu/web/2020/projects/4/network/](https://cs50.harvard.edu/web/2020/projects/4/network/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The following are the prerequisite for installing and running the project.



1. The project was built and tested on Macbook running MacOS Monterey 12.1.
2. You need to have a Git installed on your machine. You can follow instruction here to install Git- [https://github.com/git-guides/install-git](https://github.com/git-guides/install-git)
3. You will need a GitHub account which will enable you to clone the project from Github. sign up for a Github account here [https://github.com/](https://github.com/)
4. Python 3.10. You can download and install the latest Python from here - [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)
5. Install virtualenv. You can follow the instruction here [https://sourabhbajaj.com/mac-setup/Python/virtualenv.html](https://sourabhbajaj.com/mac-setup/Python/virtualenv.html)
6.	You will need PostgreSQL database. You can follow the instructions here - [https://www.postgresql.org/download/macosx/](https://www.postgresql.org/download/macosx/). Please setup a database called "project4_networks" and if you can set it up running on port 5432, that will be great.
7. Chrome Version 98.0.4758.102 (Official Build) (arm64)
8. ChromeDriver Version 98.0.4758.102. The ChromeDriver is required if you intend to run the test suits



### Installing


Once you have the above pre-requisites, you can follow the instructions here to setup and get the project running. You need to open a terminal session. Sample commands are in bold like **```$this```**, the '$' sign being the bash prompt.



1.	Create a new folder for the project - **```$mkdir myproject```**. 
2.	CD to the folder - **```$cd myproject/```**.
3.	Setup up a virtual environment - **```$virtualenv venv```**. 
4.	Activate virtual environment - **```$source venv/bin/activate```**.
5.	Clone the project from GitHub - **```git clone https://github.com/sekarnagappan/CS50_project4_network.git```**.
6. CD to the project folder as - **```cd CS50_project4_network```**.
7. Ensure you have the lastest version os pip. **```python -m pip install --upgrade pip```**.
8. Install all the require Python libaries - **```pip install -r requirements.txt```**
9. Setup .env file, with the following 3 environment variable.
	*	Create a file .env in the folder project4 - **```touch project4/.env```**
	* 	Open the file in a text editor - **```nano project4/.env```**
	*  you need to setup up values for the following environment variables.
		*  DEBUG=on
		*  SECRET_KEY=your-secret-key
		*  DATABASE_URL=psql://user:password@127.0.0.1:port/database
	*	Save the file. 
	* You can set DEBOG oN or OFF.
	* You can generate secret key using this command - **```python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'```**
	* For the databaseURL, you need to replace 'user', 'password' and port with your database user id, password and port that you have setup during database setup.
10. Run makemigrations  - **```$python manage.py makemigrations```**
11. Run migrations - **```$python manage.py migrate```**.
12. Start the application **```$python manage.py runserver 8000```**.
13. Create a superuser. **```$python manage.py createsuperuser```**
14. You will be prompted for the user ID and password. Please provide as a ID and password of your choice.
14. Go to your Web browser, and connect to localhost:8000.
15. Go will get the log in screen. 
16. Please this demo video at this link on how to use the application.


## Running the tests

The project contais a set of test cases. From the folder "CS50_project4_network", you can run this command to execute the test cases,

```
$python manage.py test
```

You should see an output like this,

```
$python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....................
----------------------------------------------------------------------
Ran 20 tests in 103.701s

OK
Destroying test database for alias 'default'...
```
The test run in slicence mode. A database will be created, 20 test will be run, and then the database destoryed.

Please the project has Github workflow file, will will execute the full set of test cases whenever a change is pushed to Github.

The Github workflow file is 

~~~
.github/workflows/project4-network-test.yaml
~~~

### Break down into end to end tests

The following are the test cases in the set of test above.

|Test Case                   	|Description                       |
|-----------------------------|----------------------------------|
|          									|                        |
|test_followings              			|Test views.py functionality for follow, unfollows, and followings count|
|test_likes                   			|Test views.py functionality for likes, unlikes and likes counts.|
|test_paging                  			|Test views.py functionality for pagination.|
|test_postings                			|Test views.py functionality for recording a new post.|
|test\_empty_postings        				|Test views.py functionality for test of an empty post|
|test\_view_profile         			 	|Test views.py functionality for profile views|
|test\_get\_index\_and\_paging_count		|Test views.py functionality for PAging and index counts|
|test\_likes_dislikes                	|Test views.py functionality for flipping between like and dislikes|
|test\_user_counts 							|Test views.py functionality for |
|test\_valid_login 							|Test views.py functionality for testing login|
|test\_invalid_login 						|Test views.py functionality for testing login failures|
|test\_create_post 							|Test views.py functionality for create new post|
|test\_create\_empty_post 					|Test views.py functionality for create an empty post|
|test\_edit_post 							|Test views.py functionality for edit your own post|
|test\_edit\_others_post 					|Test views.py functionality for editing somelese post|
|test\_view_profile 						|Test views.py functionality for view a profile|


## Deployment

This project is an assigment for a programming couse. The project is not to be deployed in any production server. 

For testing purposes the code can be downloaded and installed using the above installation and testing instructions.

A docker compose file is also provided to deploy the project in Docker and run the application. 

## Built With

* Django
* Javascript
* Python
* HTML
* JSON

## Usage

The application is a fairly simple application to use. The couse required a 5 minutes demo video of the project. This video will show you how to use the application. The video is [here]().

## Versioning and Change Log

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This project is version 1.0.0


## Authors

* **Sekar Nagappan** - *Initial Submission*


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

* I have used the function getCookie from https://docs.djangoproject.com/en/dev/ref/csrf/#ajax in network.js.

