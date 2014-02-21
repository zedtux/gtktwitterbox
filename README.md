<p align="center">
  <img src="https://raw.github.com/zedtux/gpair/master/media/developpeur_breton_logo.png" alt="Je suis un developpeyr Breton!"/>
</p>

# GtkTwitterBox [![endorse](http://api.coderwall.com/zedtux/endorsecount.png)](http://coderwall.com/zedtux)

This GTK 3 module written in python 3.3 will show the 5 latest tweets of a given account and refresh X given seconds.

It is a part of the [Douane](https://github.com/zedtux/Douane) project.

#### Python PEP8 and GtkTwitterBox

I'm not a python expert developer, I'm just doing python at home so I didn't spent time to have compliant code with PEP8.

I have plan to do that later on but if an expert is passing here and wants to contribute, he will be the welcome!

## Screenshot

I am using it for my application [Douane configurator](https://github.com/zedtux/douane-configurator) and here it is how it looks like:

![GtkTwitterBox in Douane](http://ubuntuone.com/1ZaFx8nsMX0JKWRSBYzW8Y)

## Installation

### Debian/Ubuntu package

The library is now available in a PPA.

    sudo add-apt-repository http://repository.douaneapp.com/
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 874CAFB5
    sudo apt-get update
    sudo apt-get install gtktwitterbox

### Git

You can import this Git repository as submodule in your project.

To do so open a terminal in the root path of your python project and execute the following:

    git submodule add git://github.com/zedtux/gtktwitterbox.git gtktwitterbox

This command will create a new folder gtktwitterbox in your project.


## Usage

Import it

````python
from gtktwitterbox.twitter import GtkTwitterBox
````

Embed it

````python
GtkTwitterBox(vbox_main, "douaneapp", 15)
````

 - The first argument is the Gtk container where you want to have GtkTwitterBox.
 - The second argument is the twitter account name
 - The third argument is the interval of time to refresh tweets (in seconds)

You can also have a look at the [test.py](https://github.com/zedtux/gtktwitterbox/blob/master/test.py) file

## Contributing

You can contribute to this project by adding support for new [VCS](http://en.wikipedia.org/wiki/Concurrent_Versions_System) or new frameworks.

### Fork

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
