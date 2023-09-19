# facer
My school project face-recognition thing. Using cv2 and face_recognition libraries

# Get started
To make it work you have to install cv2 and face_recognition libraries.

Install using requirements.txt:
   1. Open your terminal
   2. use one of those commands: pip install -r [path to the requirements.txt] or pip3 install -r [path to requirements.txt]

Install all by yourself:
  1. Open your terminal
  2. pip3 install opencv-python && pip3 install face_recognition

# How to use

We'll start with the face data creation and saving (or deleting):
  1. To use the panel, you will need to know some commands. You can see them by calling the help function:
     python3 controlPanel.py -h

     You will see something like this:
       usage: controlPanel.py [-h] [-a] [-d] [-n NAME] [-i IMAGE]

        Control panel for face recognition
        
        options:
          -h, --help            show this help message and exit
          -a, --add             Add a new face to the JSON file
          -d, --delete          Delete an existing face from the JSON file
          -n NAME, --name NAME  The name of the person to add or delete
          -i IMAGE, --image IMAGE
                                The path of the image of the person to add

     the syntax is pretty self-explanatory here, so you'll adapt to it pretty fast

     Here's the example of adding a new facedata from a photo: python controlPanel.py -a -n John -i images/John.jpg
     Here's its deletion: python controlPanel.py -d -n John

# Good luck using it and be free to file any bugs to my email: lvumbapipin@gmail.com
