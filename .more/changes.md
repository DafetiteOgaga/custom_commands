# Changelog
This file contains the notable changes made to the Custom Commands project.

## Changes
   - fixed pushfile command to now execute without argument, parsing through all the directories and subdirectories in the given repository and listing the modified, changed, new, deleted, etc files in-turns for staging and commiting before pushing only the committed changes to remote
   - createReactApp - changed the default tags within the head tag of index.html in /public/ to accomodate setup for seo, preview cards for social media, etc
   - merged mysqlstart, mysqlstop, mysqlrestart and mysql_status commands
   into mysqlOp command
   - changed rollback to revert2commit command, which is preferred because
   it reverts to any earlier commit state and still keeps the commit history by undoing all the changes made upto the selected commit and
   creating a new commit for this revert. Hence, history is not lost or
   discarded
   - added distributeApk command, it helps to update the versioning and
   distribution of my altaviz mobile app for update and download to the
   latest version.
   - Added (New) createExpoApp - uses backed up app config setup to create apps after the initial (first downloaded) setup and spins up the local server automatically.
   - Added (New) setEnv command - creates environmental variables automatically.
   - Added collectstatic command - collects static files in django for production.
   - Added support for urls display to startproject command when creating a new django project. install and run djangoUrls command to see the list and details of all configured urls.
   - Added the list of endpoints created by drf, jwtDjango and djoser to the the displayed text after installation
   - changed showDiffs command to showDiff command
   - django config commands now display the specific changes made to the settings and urls files
   - added support for DRF-xml rednderer configuration, separated DRF-auth configuration from DRF config in DRF command
   - implemented app-level urls.py auto creation and urls configuration were added in startapp command
   - gitignore now auto add all \_\_pychache\_\_ files and venv dirs if you choose to
   - djoser command now configures its default routes in project's urls file along with the settings.py file
   - drf command now configures its authentication token functionality along with its installation
   - startapp command will now install the app name under INSTALLED_APPS in settings.py automatically
   - changed compare command to showDiffs command
   - gitignore now adds itself as a file to the .gitigore file to prevent commiting and pushing it to your repository
   - currfol now works on ubuntu and wsl-ubuntu
   - you can now skip files from being committed when using pushfile
   - majority of the display/output now commes with text coloring
   - deleting your repo is now much flexible as all you have to is select the number corresponding to the repo from the display me listing all of your repos
   - error of "... divergent branches ... reconcile divergent branches" has been fixed for all pull processes
   - massive improvements made to cloneRepo command. All you now need to clone your repo is just to run the command. It displays all your private and public repositories, giving you the option of cloning any of them with the selection menu. To clone another person's public repo, you only need the username. Collaboration has never been more interesting, you can now do so easily using this command
   - you can now observe the progress of setting up auto commit message for README.md files via a progress bar
   - added the ability to set "Update README.md" as your default commit message to all README.md files
   - new updates and general improvements to the the program
   - pull and push commands has been updated for robust perfomances
   - Improved user experience with a little bit of animated display
   - Minor changes made to the script and display for effectiveness
   - pyxecute also appends the python3 shebang line to the first line of the script
   - pyxecute command now checks for the presence of py scripts and responds accordingly
   - Readme file was updated
   - "from" word was removed from the parting message after installation
   - Change to multiple display in pages and its navigation
   - Minor changes made to guessing game, rot13, rot47 and my ascii codes to enhance performance
   - clone and create repo commands now collect users information during installation
   - Changed the process of users having to open the clone and create repo scripts to manually input their details
   - Added the last choice of command and the command it created to the display
   - Changed the simple ASCII table display
   - Changed default C template description
   - Removed emoji from Guessing game
   - Removed emoji from Rot47
   - Removed emoji from Rot13
   - Removed emoji from simple ASCII table
   - Added support for multiple arguments for pycode, pycodemore and pycompile commands
   - Added installations of betty linter and pycodestyle(PEP 8)
   - Added Support for 64-bit operating system computers
   - Added Support for AARCH64/ARM64 operating system for phones
   - Added Support for PC and Phone and device detection
   - Added Support for root user password request for PC
   - Added sample screenshot of the menu when the script is executed
   - Added Support to configure git username and email locally to the create and clone repository commands (specific to the current working repository)
   - Added reminder to users not to create a repository within an existing repository
   - Added reminder to users not to clone into an existing repository
   - Added quit option to push command
   - Moved the project to remote repository



###### *We Rise by Lifting Others.*
