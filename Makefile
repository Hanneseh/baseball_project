.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = [OPTIONAL] your-bucket-for-syncing-data (do not include 's3://')
PROFILE = default
PROJECT_NAME = baseballmd
PYTHON_INTERPRETER = python3

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Make Dataset
data: requirements
	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw data/processed

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

## Upload Data to S3
sync_data_to_s3:
ifeq (default,$(PROFILE))
	aws s3 sync data/ s3://$(BUCKET)/data/
else
	aws s3 sync data/ s3://$(BUCKET)/data/ --profile $(PROFILE)
endif

## Download Data from S3
sync_data_from_s3:
ifeq (default,$(PROFILE))
	aws s3 sync s3://$(BUCKET)/data/ data/
else
	aws s3 sync s3://$(BUCKET)/data/ data/ --profile $(PROFILE)
endif

## Set up python interpreter environment
create_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda create --name $(PROJECT_NAME) python=3
else
	conda create --name $(PROJECT_NAME) python=2.7
endif
		@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
else
	$(PYTHON_INTERPRETER) -m pip install -q virtualenv virtualenvwrapper
	@echo ">>> Installing virtualenvwrapper if not already installed.\nMake sure the following lines are in shell startup file\n\
	export WORKON_HOME=$$HOME/.virtualenvs\nexport PROJECT_HOME=$$HOME/Devel\nsource /usr/local/bin/virtualenvwrapper.sh\n"
	@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
endif

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')


#################################################################################
# Here are some commands and procedures that you will need to use many times 
# while developing. This file seves as a "Cheat Sheet" for you to look for those 
# commands and procedures. But of course there are many diffrent possible situations
# and I cant provide a standardized procedure for all of them, thats why a I recommend 
# googling or maybe looking at these links for help when you encounter problems:
#
# https://github.com/joshnh/Git-Commands


#################################################################################
# PLEASE ALWAYS BE AWARE OF WHAT YOU ARE DOING. IF YOU DONT KNOW WHAT YOUR ARE DOING,
# ASK ME OR GOOGLE YOURSELF

# Everything that is not a comment in here is a command you can copy to the terminal.
# Squared Brackeds [] mean that you need to replace that part of the command with your
# own information
#################################################################################


#################################################################################
# STARTING DEVELOPMENT:

# 1. Open the folder with the two subfolders: "baseball-env" and "baseballmd" in VSCode

# 2. open a new terminal in VSCode

# 3. activate the virtual environment by typing this: 
. baseball-env/bin/activate
# Windows:      C:\Users\Basit\OneDrive\Desktop\Baseball\baseball-env/Scripts/activate 
# it was a success when the terminal line now starts with "(baseball-env)

# 4. navigate to the project folder "baseballmd" by typing:
cd baseballmd 
# it was a success when the last word in the new terminal line says "baseballmd"

# 5. check what branch you are on by typing:
git branch
# this commands lists all your local branches and marks the one you are on
# NEVER WORK ON MASTER BRANCH!!

# 5.1 in case you are on a wrong branch, switch to the right branch with this command:
git checkout [YOUR BRANCH NAME]

# 5.1.1 in case this is not possible because you have uncomitted changes either commit them 
# or delete them. If you want neither of this you can stash them. Please google what this is
# or ask me

# 6. make sure you have the latest version of that branch by typing:
git pull

# 7. make sure all dependencis are up to date by typing: (*)
pip install --upgrade -r requirements.txt
# ignore possible warnings for now. 

# 8. install all our own python packages in such way that edits are effectiv by typing: (*)
pip install -e .


# now you are ready to start developing. 
# Make sure to follow the the COMMIT Procedure during development
# Make sure to end devolping with the END DEVELOPIG procedure
#################################################################################


#################################################################################
# COMMIT procedure
# Why and then do this?
# -> We do this whenever we were successfull in developing something. This can be as
# little as adding one line of code to a file. So basically whenever your code reaches
# a state that YOU want to safe, in case you ever want to go back to that state.

# An example: The web scrapper works for one specific website perfectly. You commit that 
# state. Now you try to make the scapper work as well for another website. You all the sudden
# need to edit the code you wrote earlier in order to achieve your goal. You fuck something 
# up because you are a noob. You try to fix the error that is now appearing for no reason.
# the error doesnt go away anymore. You start loosing your mind because you messed up 
# a perfectly working code. You become sad. You cant fix the mess. You start crying.
# You start tying the rope. BUT WAIT! There is hope! You remember that you have COMMITED
# the code earlier. With a few simple commands in the terminal, you can go back to that commit
# and you have the working code again! You are happy, you can now start messing everything up agiain.
# But remember: This was only possible because you committed the code! So always commit!

# So how do we commit?

# 1. start by typing:
git add .
# this command adds all changed files to the staging area. 
# the staging area is a virtual space for all the files that need to go in one commit. 

# 2. now commit by typing:
git commit -m "[YOUR COMMIT MESSAGE]"
# this commits all the files that are in the staging area. 
# the message in the "" is visible to all developers and should explain the changes
# that you have made in the commit, but keep it short (10 words max!)

# now you have successfully made a commit. This commit is only on your computer tho.
# you need to push your commit to the remote repository in order to share it with others
# you dont need to push every commit right away, but do at least one push before you stop
# working-

# 3. to push the commit type:
git push

#################################################################################


#################################################################################
# STOPING DEVELOPMENT

# Whenever you are done with devoloping for the day, follow these steps in order 
# to have a clean end

# 1. Make sure all the files you have worked on are saved. (Hit cmd+s or strg+s)
# VScode marks and tells you which files are not safed.
# you can even use the command "git status" to see which files are modified

# 2. open a new terminal and make sure you are in the "baseballmd" folder
# you can see that you are in the folder by checking tha last word in the latest 
# terminal line. If it says "basvallmd" ten you are in the correct folder
# otherwise navigate to it with the "cd" command

# 3. safe all current dependencies by typing this in the terminal: (*)
pip freeze > requirements.txt 

# 4. do a commit and push by doning these commands one by one:
git commit -m "[YOUR COMMIT MESSAGE]"
git push
# see explanation to these commands in COMMIT procedure

# 5. deactivate the virtual environment by typing this in the terminal
deactivate

# you are now done.

#################################################################################


#################################################################################
# CREATING NEW BRANCH: procedure
# You will not use this procedure on a daily bases, but also requalary and its super
# important that use it. But it is even more important that you know why you use it
# and what you are doing. If you have any questions blease ask google or me! 

# short definitions:
# Commit: is a safed. "froozen" state of the project
# Branch: is a copy of the entire project
# master: The master branch is a base branch, never touch it! Only copy it! 

# WHEN do we create a new branch?
# Whenever we start a new development task like developing a feature, fixing a bug etc.

# 1. Make sure the virtual environment is running and that your terminal is in the baseballmd folder
# see STARTING DEVELOPMENT procedure if you dont know how. 

# 2. Checkout on what branch you are on by typing:
git branch

# 3. switch to the master branch by typing:
git checkout master

# 4. make sure you have the latest version of the master branch by pulling. Type:
git pull

# 5. now initiate the new branch. Read NAMING CONVENTIONS first!
# NAMING CONVENTIONS: aways start name so that we know who made tha branch end what it is for
# so start with your name, then type a keyword either "feature" or "bugfix" followed by a shor describtion
# IN GERNAL: [YOUR NAME]_[KEY WORD]_[PURPOSE OF THE BRANCH]
# AN EXAMPLE: hannes_feature_settingUpBasicDashboard
git checkout -b [yourName_KeyWord_Pupose]
# after this command, you have created a new local branch. You are also on that branch
# you can check that by typing "git branch"
# the branch you have created is only on your PC availible and not yet accessible to us

# 6. therefore push that branch to the remote repository with this command:
git push origin [name of the branch you have just created]

# 7. then, use this command to push the current branch and set the remote as upstream
git push --set-upstream origin [NAME OF THE BRANCH]

# the new branch you have just created, is a copy of the master branch
# if you dont like that and you want it to be a copy of some other branch 
# you can use the merge function to copy all changes form that branch to yours.
# be carefull with this tho. This is something you do rather rarly and 
# errors can occure. The basic command is this:
git merge [branch name]
# this command merges the branch you have namend in the command into the brach you are currently on
# so make sure to be on the branch you want to merge in, before you type the command!
# never merge anything into master without asking me!

# You can also use this. 
git merge [source branch] [target branch]

# we will use merge requests on git lab tho to merge into the master. Never merge into master by yourself!
#################################################################################
# (*) I am not completly sure if we need this command everytime, but use it for now,
# because it doesnt mess up anything either. We'll refine our dependency management
# later on when we start deploying

#################################################################################
