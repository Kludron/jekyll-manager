# jekyll-manager

## What is jekyll-manager?

Jekyll-Manager is a command-line tool that acts as an interface to manage your jekyll blog.

Currently, the extent of the tool covers managing posts (listing, viewing, editing, creating and deleting),
but plans to cover more. Your suggestions are always welcome!

## QuickStart

Jekyll-Manager is available for download via pip (page [here](https://pypi.org/project/jekyll-manager/)).

To download, you simply need to run:
```
pip install jekyll-manager
```

### How to run (with pip install)

To run jekyll-manager, first navigate to the root directory of your jekyll blog, then type `jekyll-manager` to run.

It's that simple!

## Build it yourself

With the current build being in Python3, this needs to be installed.

Installation guide for Python3 can be found [here](https://www.python.org/downloads/). *https://www.python.org/downloads/*

After installing Python3, we need to install all of the required packages. To do this, `pip` needs to be
installed. If this is not already installed, installation steps can be found
[here](https://pip.pypa.io/en/stable/installation/). *https://pip.pypa.io/en/stable/installation/*

To install the required packages, first you will need to clone the repository. To do this, open your
terminal (or command prompt on windows) and type in:

```
git clone https://github.com/Kludron/jekyll-manager
```

The next step is to install the required pip packages. To do this, type in:

```
cd jekyll-manager
pip install -r requirements.txt
```

### How to run

Now that the requirements are installed, jekyll-manager can be run directly

*NOTE: This is tool is currently not yet configured to be run directly for Windows Machines.*
```
./jekyll-manager <jekyll-blog-directory>
```

or with python 

```
python jekyll-manager <jekyll-blog-directory>

```

There is also the ability to run this program from anywhere.

#### Linux / MacOS

For Linux and MacOS users, this can be done by symlinking the file to your local bin folder.

*NOTE: For this to work, your $HOME/.local/bin file needs to be in your PATH.*
```
ln -s $(pwd)/jekyll-manager $HOME/.local/bin/
```

#### Windows

For Windows users, this can be done by adding the jekyll-manager folder to your path. To do this:

*NOTE: Currently, this is unsupported and not available on Windows machines yet.*

1. Open up Control Panel.
2. Type in `env` in the search bar.
3. Click on 'Edit environment variable for you account'.
4. Select the 'Variable' named 'PATH'.
5. Click on 'Edit...'
6. Click on 'New'
7. Type in the Path to the jekyll-manager folder (that was cloned from github).
8. Click OK
9. Click OK (again)
10. Restart your device (for changes to take effect)

## FAQ

#### My Jekyll Configuration is different to the default, can I still use this tool?

Not at the moment. 

This tool is still very much in progress, but will cater towards all configurations for jekyll in the 
near future. Stay tuned!



