# ECSE211 Project: Team N - TEAM_NAME

:triangular_flag_on_post:

_Read this entire document before doing anything._

**You need to modify this README file as part of your project using these steps:**

1. Read this entire document to fully understand what you need to do.
2. Replace "N" and "TEAM_NAME" above with your team number and the name of your team.
3. Provide a **Project Software Overview** and complete the missing parts of the
**Project Organization**. Both of these sections can be found below.
4. **Delete** everything in this document between the two flags,
including the flags themselves.
The content between the two flags is student instructions that are not needed
by the Executives (Profs) or Senior Engineers (TAs), so remove it to make this
document suitable for them once you are done.

___

In this project you will build an item sorter that can sort solid objects
based on their properties.
For project objectives, requirements, submission instructions, and
deadlines, see detailed instructions on MyCourses.

If you need help, please post on the discussion board or contact your
mentor TA.

## Updates and corrections

We will post any updates, corrections, and
clarifications to the starter code or these instructions on
[this page](https://mcgill-dpm.github.io/website/Corrections).
Please check it regularly.

## Software requirements

- The software implementation must be done in Python 3.9 or higher
- You are allowed to create extra files, classes, and functions,
  but you must not alter the project structure
- The use of any external software libraries not included with the BrickPi or
  the lab or project materials requires prior approval from the course staff

## Setup

As with the previous labs, you will have two options for developing code for the robot:

- **Option 1: Simple Setup.** With this option, you will work on the robot directly,
using NoMachine and Thonny.
This is the recommended approach for beginners since the setup is simpler.
  
  Setup instructions for using NoMachine are provided in the
  [Getting Started Guide](https://mcgill-dpm.github.io/website/GettingStarted-F21#connecting-to-the-brick).
  Once you have connected to the robot, use a private browsing window to download
  the zip file containing the starter code to the `ecse211` folder.
  Right-click on the zip file and select "Extract Here".

  When you are ready to submit your code, right-click on the folder
  that contains the project (including this file),
  select "Compress" and pick a location to save the zip file.
  Add the zip file to your project submission folder on MS Teams.

- **Option 2: Flexible Setup.** With this option, you develop your code in an advanced
IDE such as VS Code on your computers and send it to the robot.
This is recommended for more experienced students as it offers greater flexibility,
since all members can work on the project in parallel.
Setup details for this option are provided [here](flexible-setup.md).

  You still need to submit a zip file of your code to the MS Teams submission folder.
  You can create the zip file on the robot as described in
  "Option 1" above, or simply download the zip file from GitHub (make sure
  you committed and pushed all your changes first!). 

If you are unsure which option to choose, discuss this with your teammates or mentor TA.
If you have technical issues, contact your mentor TA for assistance.

___

**In both cases, also do the following:**

**On the brick:** Double-click `robot_setup.sh` and select "Run in terminal"
to install the necessary libraries.

**On your computer:** Run `pipenv install` to install the dependencies you
need on your computer, eg, to make plots. If `pipenv` is not already installed
you can install it using `python3 -m pip install pipenv`.

___

:triangular_flag_on_post:

## Project Software Overview

_Provide a short overview of your software implementation here, including how to run your software and how to run the tests. Do not duplicate large quantities of information from your software design documents, instead mention relevant implementation details._

___

## Project Organization

In this section, we go over the files and folders included in this project,
listed in alphabetical order.
The files we modified are shown in **bold**.

- `lib`: contains libraries used by the robot such as
  the simpleaudio sound library.
- `project`: all Python files in this folder run on the robot.
  - [`doc`](project/doc): documentation for the brick API
  (Application Programming Interface), ie, the classes and functions
  you can use to work with the robot.
  - [`utils`](project/utils): brick-related utilities for this project.
  See the other project files to see examples of how to use these modules.
    - `brick.py`: the main module for interacting with the brick hardware.
    - `sound.py`: module that allows you to play sounds.
    It depends on the simpleaudio library.
  - [**`logic.py`**](project/logic.py): computations that can run on both
  the brick and the computer. Placing these in a separate file allows
  for testing on a computer, which can be faster than running on the brick.
  - [**`retriever.py`**](project/retriever.py):
  _Describe your sorter implementation here. If you used other files, describe them as well._
  - [**`test_logic.py`**](project/test_logic.py): a script to test the correctness of controller logic.
  It is meant to be run from a computer using the `pytest` command.
- `scripts`:
  - `reset_brick.py`: If the program does not exit correctly, eg,
  if it is stuck in an infinite loop, this script can be run on the brick to reset it.
- `deploy_to_robot.py`: a script to deploy the code to the robot from a computer.
  It offers the following options:
  - Deploy DPM Project on Robot without running:
  copy the `project` folder to the robot.
  - Deploy and run DPM Project on Robot:
  copy the `project` folder to the robot and run the file specified
  in `project_info.json`.
  - Reset Robot: reset the robot.
- **`project_info.json`**: a file containing information about the project.
- `robot_setup.sh`: a script to install the required libraries on
the brick as described in the project instructions.
