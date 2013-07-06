from distutils.core import setup

setup(
    name = "gtktwitterbox",
    packages = ["gtktwitterbox"],
    version = "1.0.0",
    description = "Python library to inject a GTK Box with the latest tweets from an account.",
    author = "Guillaume Hain",
    author_email = "zedtux@zedroot.org",
    url = "https://github.com/zedtux/gtktwitterbox",
    download_url = "https://github.com/zedtux/gtktwitterbox",
    keywords = ["gtk", "widget", "twitter"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Desktop Environment :: Gnome",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = "Inject a Gtk::Box to show the latest tweets of a given twitter account with auto-refresh"
)
