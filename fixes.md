## Fixes
   - createReactApp now downloads the configs for CRA on first use, then uses this config for subsequent use while it updates itself whenever there is an update to CRA config
   - handled the case where a user tries to install and configure a django project without initially installing an app
   - fixed the DRF module error for runserver, sqlmigrate commanda
   - handled moduleNotFound error in migrate command
   - minor bug fixes to: djshell, makemigrations, mkandmigrate, static4django
   - removed unnecessary display from py3venv command
   - changed the help text from using apt package manager to using pip to install mysqlclient
   - gitignore - the command now create/update with the root paths starting with root repository
   - minor bug fixes made to setScript, cloneRepo and createRepo commands
   - every prompt that require single character as response are now auto executing soon as the character is provided
   - you don't have to enter your information twice anymore when running createRepo and/or cloneRepo anymore in the same session
   - "Next" and "Previous" choices no longer reinstall the previous command and clears off the screen, any information belonging to the previous command
   - Resolve issue of invalid path in ctemp command
   - Fixed bugs in createRepo command
   - Fixed scripts repetition for PCs and Phones
   - Fixed bugs in cloneRepo command
   - Fixed bugs preventing pycodemore command from working due to pycodestyle
   - Fixed bugs in "[n] option display and selection"
   - Fixed bugs in ctemp command
   - Fixed exec: format errors caused by variation in operating system architectures for both phones and computers
   - Commands creation now runs contineously until you quit the process
   - Source files and compilations has been removed from the operations for optimization
   - The authorID, create and clone repo commands now automatically configures local author during operation
   - You now have to provide your Username, token and email when creating create/clone repo commads
   - Repetition of codes in setscript has been removed to enhance robost performance 
   - Fixed and removed answer display before the start of the guessing game
   - Added execute permission for all user to the files.
   - Fixed response to wrong input entered by users during installation and command execution
   - Fixed option display to be limited to alphabets and not numbers
   - Removed repeated lines of codes that need not be



   ###### *We Rise by Lifting Others.*