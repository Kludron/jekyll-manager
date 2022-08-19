# jekyll-manager

## What is jekyll-manager?

Jekyll-Manager is a command-line tool that acts as an interface to manage your jekyll blog.

Currently, the extent of the tool covers managing posts (listing, viewing, editing, creating and deleting),
but plans to cover more. Your suggestions are always welcome!

## QuickStart (Method One: with pip)

Jekyll-Manager is available for download via pip (page [here](https://pypi.org/project/jekyll-manager/)).

To download, you simply need to run:
```
pip install jekyll-manager
```

### How to run

If you installed it via pip, then it's quite easy to run.

There are 3 ways (currently) to run the program:

1. Type in `jekyll-manager </relative/path/to/jekyll-blog>` to manage your blog.
2. Traverse to the root of your jekyll blog directory, then type in `jekyll-manager` to manage your blog.
3. Set the environement variable `JEKYLL_ROOT` to point to your jekyll blog directory, and run 
`jekyll-manager` from anywhere.

Jekyll-Manager will find your blog in the order above, so even if you're in a jekyll-blog directory, and 
type in the path to another directory, it'll check that other directory.

## Method Two: setup.py

Alternatively, if you don't want to download via pip, clone the repository by typing in
```
user@computer:~/Downloads/$ git clone https://github.com/kludron/jekyll-manager
```

Then traverse into the directory and run the `python setup.py install`

```
user@computer:~/Downloads/$ cd jekyll-manager
user@computer:~/Downloads/jekyll-manager/$ python setup.py install
```

You should now be able to follow the same instructions as in the 'How to run' section!

## Build it yourself

With the current build being in Python3, this needs to be installed.

Installation guide for Python3 can be found [here](https://www.python.org/downloads/). *https://www.python.org/downloads/*

After installing Python3, we need to install all of the required packages. To do this, `pip` needs to be
installed. If this is not already installed, installation steps can be found
[here](https://pip.pypa.io/en/stable/installation/). *https://pip.pypa.io/en/stable/installation/*

To install the required packages, first you will need to clone the repository. To do this, open your
terminal (or command prompt on windows) and type in:

```
user@computer:~/Downloads/$ git clone https://github.com/kludron/jekyll-manager
```

The next step is to install the required pip packages. To do this, type in:

```
user@computer:~/Downloads/$ cd jekyll-manager
user@computer:~/Downloads/jekyll-manager/$ pip install -r requirements.txt
```

### How to run (build it yourself)

Now that the requirements are installed, jekyll-manager can be run directly

*NOTE: This is tool is currently not yet configured to be run directly for Windows Machines. The `python` prefix is needed*
```
./jekyll-manager <jekyll-blog-directory>
```

or with python 

```
python jekyll-manager <jekyll-blog-directory>

```

There is also the ability to run this program from anywhere (by setting environment variables).

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


After adding it to your path, you can follow the guide in the (first) 'How to run' section.

## FAQ

#### My Jekyll Configuration is different to the default, can I still use this tool?

Not at the moment. 

This tool is still very much in progress, but will cater towards all configurations for jekyll in the 
near future. Stay tuned!



