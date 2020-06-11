# Installation guides

There are two ways to install NL-Baseball on your machine or to deploy it on a sever.

1. Using Docker: Recommended for deploying and experienced developers
2. Using Pip: Recommended for exploring the project and unexperienced developers

## Using Docker
-	The steps in this guide describe the process of installing NL-Baseball using docker.
-	The steps are only tested on a Mac and are guaranteed to work when followed closely and with the given configuration. 
-	After following this guide, you should have a working project without any security mechanisms in place. Meaning, the database is unprotected and the docker-compose only contains the bare minimum of parameters which might be needed for deploying the project.
-   Keep in mind: The Steps in this guid are designed by a docker newbie. There probably is a better way to do this, but time is money, and I dont get paid for this ;)


### Requirements
-	A working docker installation (https://docs.docker.com/get-docker/)
-	A working docker-compose installation

### Step 1
-	Clone or download the repository (https://gitlab.fdmci.hva.nl/ehringh/baseballmd)
-	Open a Terminal in the project folder (baseballmd)
-	Run: `docker-compose up –build`

Now the monogdb container gets build and the data scraper script is executed.
When you see this ouput in the terminal, you know the data scraping has finished:

![finishStep1](img/step1finish.png)

### Step 2
Now the database contains all needed data. We need to make some modifications in the code in order to make the dashboard, database and datas craper run in sync.

Follow these steps closely:

-	Exit the process in the terminal by pressing `control + c`
-	Open "docker-compose.yml" file and remove the comments like shown in the picture:
![beforAfter1](img/beforAfter1.png)
This will make the dashboard start up the next time you will run docker compose

-	Now navigate to the "DataScraper" directory and open "dataJob.py"
-	Edit the file exactly as shown in the picture below:
![beforAfter2](img/beforAfter2.png)
This makes the data scraper run only at night and keep the container up.

### Step 3
-	Make sure all files you have edited are saved
-	Run: `docker-compose up –build` again

The dashboard container should start up now as well and you should see this output in the terminal:
![finishStep3](img/finishStep3.png)

When you see it you can copy http://0.0.0.0:8050/nlbaseball/ to your web browser and you should see the dashboard.

### Step 4
If you want/need to modify anything look here:

For database connections
-	DataScraper > app > config.py 
-	Dashboard > pages > database.py

For start of Dashboard and port modification:
-	Dashboard > index.py
-	Dashboard > Dockerfile
-	docker-compose.yml

## Using Pip

content follows soon