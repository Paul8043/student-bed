# student-bed

# Preamble

Why does this repository exist? My son has declared some demand for an additional bed for his student digs. I have got an order to run a project. The entire project is organized as a sequence of mile-stones. After each mile-stone I will add an entry in this Readme.md. Stay curious, I will take you along for a longer, and hopeful interesting, journey. Let us start, the adventure begins ...

# Mile-Stone #1: Model Specification

Before a journey starts, it always good to know, which destination we want to reach. A clear view of the goal is always helpful. In our case this is a bed, and this beds needs a specification. It comes in two flavors. The External-Model-Specification, for short EMS, describes the requirements for the view of the customer (my son). Here, he describes what he wants to get.  The most important topics are related to measures. All these details can be found here XXX. The Internal-Model-Specification, for short IMS, covers the aspects of the design and implementation. It holds all the details from the view of a cabinetmaker (that's my role). This document can be found here YYY. See HERE for some additional information.

# Mile-Stone #2: Software-Tools 

This project requires some resources for its execution. Some tools are need for the design of the bed, and some others for the wood-working. We try to use the up-to-date tools. We make a CAD-model first, then we can see how it will look like. The tool for this purpose is "CadQuery", a CAD-library written in Python. The hidden agenda is to give some stimulus to learn new tools, this applies for us both, my son and me. We make a new approach, the model is not "drawn", but programmed. This strategy has some advantages, the python-program, that represents the model is very compact and easy to maintain. Changes measures are only a few clicks. How does this work? How to convert a python-program to a visual 3D-object? This is task of a 3D-viewer, in our case this done by CQ-editor. "CadQuery" and "CQ-Editor" are close campanions. In most cases they are used together. As the naming might indicate, the "CQ-editor" can do more than visualizing the model, it has also some possibilities to change the python-code. It is a small IDE (Integrated Development Environment). For our purposes fully sufficient. As always running a project is never a straight forward going. It is more an explorations of various alternatives. Going back and forth is quite normal. What is the best solution, will crystallize out during our journey. Because of that it makes a lot of sense to have good revision-control-system, which can store all intermediate revisions. The top-candidate is "git". And because now-a-days everything can go to a cloud, we set up the infrastructure for this, too. Here we choose GitHub. So far, the tool-box for the software-side is almost complete. What is needed for wood-working will be discussed later. To make this mile-sone complete, perform the installations, which described here and here.


1. GitHub-Account
2. Software-Tools
   1) git           revision control system
   2) mambaforge    virtual environments for python
   3) python        programming language
   4) cadquery      CAD-library
   5) VS Code       IDE 
   6) cq-editor     model editor & viewer
