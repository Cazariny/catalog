This is the my Item catalog project

#Function
This is a Catalog of sports products made with python flask and sqlalchemy using a database and some templates for the products.
This project have the CRUD functionality (Create, Read, Update and Delete) which means you can create new articles , edit it and delete it
in order to create, edit and delete you need to be logged in in the project so, this project have the option of be a registered user and modify the catalog or be an unregister user and just see the catalog
The only way to login in the application is by having a google acount, so take that in mind.

##Requirements
**Use of the terminal If you are using a Mac or Linux system, your regular terminal program will do just fine. On Windows, we recommend using the Git Bash terminal that comes with the Git software. If you don't already have Git installed, download Git from https://git-scm.com/downloads**

###Install a Virtual Machine
The Virtual Machine is basically a computer inside an other computer (not literally) you don´t need to install the virtual machine for run the program but, you can do it if you want

You need to install virtual box, Virtual box is a software that runs virtual machines you can download it from here **https://www.virtualbox.org/wiki/Download_Old_Builds_5_1**

and click in the version for your operating system

###Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. You can download it from **https://www.vagrantup.com/downloads.html**

If you are a windows user the installer may ask you yo grant network permissions to Vagrant, be sure to allow this

If you install vagrant correctly in your terminal you will be able to run the command

```
vagrant --version
```

and it will give you the version of the installed vagrant

The virtual machine configuration you can download it from **https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip**

Extract the content and you will have a new directory in your terminal change to that directory with the command *cd* inside of that directory there are an other directory called vagrant (you can check it with the command *ls*)

####Start the Virtual Machine
From the vagrant folder run the command **vagrant up** with this Vagrant will download the Linux operating system and install it. don´t worry this will take a while, depending on how fast is your internet

When vagrant up is finished you will get the shell prompt back (in git bash *$*) now you can run **vagrant sh** and you will be logged in your new Linux virtual machine

##Run
For use the app you need to download the project and save it in your vagrant folder, then initialize your vagrant environment and write in your terminal

```
cd /vagrant
```

This command will go to your computer vagrant folder (where you save the project) and now you can run the files.
The next thing you need to do in order to run de project is go to the project folder so, you need to run

 ```
 cd catalog
 ```

Now you can start the catalog just by writing:

```
python aplication.py
```
When you do this in your terminal will appear something like this
```
vagrant@vagrant:~$ python aplication.py
 * Serving Flask app "aplication" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 325-904-188

```
If this appear it means that the application is Running.
Now it's time to start your favorite browser and type the following **http://localhost:5000/**
And that's it you are using the catalog

