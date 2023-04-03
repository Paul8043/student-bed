# !!! under construction !!!

# Student-Bed

# Preamble

Why does this repository exist? My son has declared some demand for an additional bed for his student digs. I have got an order to run a project. That's clear, I take this challenge. This is a perfect candidate to learn Python, Cadquery and some aspects of Woodworking. The entire project is organized as a sequence of mile-stones. After each mile-stone I will add an entry in this Readme.md. Stay curious, I will take you along for a longer, and hopeful, interesting journey. Let us start, the adventure begins ...

# Mile-Stone #1: Model Specification

Before a journey starts, it is always good to know, which destination we want to reach. A clear view of the goal is always helpful. In our case this is a bed, and this bed needs a specification. It comes in two flavors.

The External-Model-Specification, for short EMS, describes the requirements from the view of the customer (my son). Here, he describes what he wants to get. The most important topics are related to measures. All these details can be found in [EMS](docs/EMS.txt). 
 
The Internal-Model-Specification, for short IMS, covers the aspects of the design and implementation. It holds all the details from the view of a cabinetmaker (that's my role). This document can be found here [IMS](docs/IMS.txt).

# Mile-Stone #2: Software-Tools 

This project requires some resources for its execution. Some tools are need for the design of the bed, and some others for the wood-working. Because is a tutoroal, we try to use the up-to-date tools. Before we do any woodworking, we create a CAD-model first, then we are able to see how it will look like. The tool for this purpose is "CadQuery", a CAD-library written in Python. 

The hidden agenda is to give some stimulus to learn new tools, this applies for us both, my son and me. We make a new approach, the model is not "drawn", but programmed. This strategy has some advantages, the python-program, that represents the model is very compact and easy to maintain. Changing measures are only a few clicks away.

How does this work? How to convert a python-program to a visual 3D-object? This is task of a 3D-viewer, in our case this done by CQ-editor. "CadQuery" and "CQ-Editor" are close campanions. In most cases they are used together. As the naming might indicate, the "CQ-editor" can do more than visualizing the model, it has also somecapabilties to change the python-code. It is a small IDE (Integrated Development Environment). For our purposes fully sufficient.
 
As always running a project is never a straight forward going. It is more an explorations of various alternatives. Going back and forth is quite normal. What might be the best solution, that will crystallize out later during our journey. Because of that it makes a lot of sense to have good revision-control-system, which can store all intermediate revisions. The top-candidate is "git".

And because now-a-days everything can go to a cloud, we establish the infrastructure for this, too. Here we choose GitHub. Git and GitHub are also close companions. All code for this project is kept in a folder on the local machine. With some git-commands this folder can be transfered to GitHub and vice versa. In the name-space of GitHub this folder is called "repository".

There is one thing left over. What kind of editor we will use, for modifying our source-files? We choose VS-Code. This has many benefits (will become clearer soon).
 
So far, the tool-box for the software-side is almost complete. What is needed for wood-working will be discussed later.

# Mile-Stone #3: Software Installation

This is a complicated step, a high risk enterprise. It can be accomplished in a few minutes, if have good and proven recipe (good luck). If you don't have one, calculate more time, it can consume hours, days, weeks or even more (bad luck).

To reduce the fear, it took me a few days.

What is the reason for this? The big question is: In which order should we perform the installations? Some dependency-checks are built-in, and each package should solve this issues for its own. But this does not work very well and not across different of kinds  of applications. The likehood, that some trials are necessary, are quite high. An installation should always be an all-or-nothing operation, which means an application should succeed or leave the computer untouched. On the windows-platform installations are something in between. The de-installer is not the inverse of the installer, and this the root-cause for almost any kind of trouble. What typically happens, the de-installer leaves something over, in your home-directory, in AppData-area or even inthe registry. That means, if you have to de-install an application, and this need comes up very often, then your are forced to play the loser-role.

Before doing installations it is always good practice to create an immage-backup first, then you can recover with less effort to a previous working state. But this needs also some know-how. We skip this topic, because it would lead us too far away from our CadQuery-project.

A good advice in advance, never install more that is really needed, otherwise the probabiltity to fail be increased significantly.

Make sure that your windows is up-to-date (windows-update).

We install "git" first. Follow the instructions given [here](docs/HowTo-Git.txt). The video there, is highly recommeded. Don't forget to specify user.name and user.email at the end of the procedure. Without that "git" will reject to perfom any work. If it succeeds, you will have a Git-Bash. This is like a CMD-window, but is offers much more capabilities. You get full access to "git" and some famous linux tools like "find" and "grep". Always use the Git-Bash, if you plan to talk to "git" on command-line level. The Command-Windows like CMD or Power-Shell do have the right context. Keep that in mind.

Next we take care for GitHub. To use GitHub you don't need any installations, you need just an account. Then define your first "repository" which consists initially of 3 files: a "Readme.md", "LICENSE" and a ".gitignore". For ".gitignore" select the template for python. The "LICENSE" is up to you. There is one subtlety here: "git" had asked you to specify your email-address and "GitHub" has asked you for a login-name which is likewise also an email-address. Both work only work smoothly together, if the email-address is same for both.

The next application is Visual Studio Code, sometimes simply called VS-Code. Originally it has been designed as an editor. But in the meantime it has reached the level of a comfortable IDE (integrated develop environment). There exist extensions for almost everything. Besides this, it offers built-in git-support. By using VS-Code you can do all needed git-tasks thru the graphical interface which is really simple to use. You should install the following extension:

* Your language Pack
* Git Graph
* Python (by Microsoft)

Resist the temptation to install more.







1. GitHub-Account
2. Software-Tools
   1) git           revision control system
   2) mambaforge    virtual environments for python
   3) python        programming language
   4) cadquery      CAD-library
   5) VS Code       IDE 
   6) cq-editor     model editor & viewer
