# FlaskABF
FlaskABF is a Python-based web application designed to browse and analyze electrophysiology data stored as Axon Binary Format (ABF) files. 

This project reads ABF files using [pyABF](https://github.com/swharden/pyABF) (and [pyABFauto](https://github.com/swharden/pyABFauto)) and displays them using a Flask server. Web interfaces are inspired by abandonware like [SWHLab](https://github.com/swharden/SWHLab) and [SWHLabPHP](https://github.com/swharden/SWHLabPHP). FlaskABF is built on the [Flask microframework](http://flask.pocoo.org) and is intended to be easier to maintain and develop for than complex systems based on custom configurations of Apache and PHP.

The path of the root folder served is hard-coded in [server.py](src/server.py) but referred to in URLs as /X/ regardless of its actual path on the server.

## Usage

Activate different views by calling different URLs with a directory-like structure.

### ABFviewer
Creates a frameset and loads the ABFmenu and ABFfolder for the given path. Most people will only type this in their browser.
```
http://192.168.1.225:8080/ABFviewer/X/Data/path/to/project
```

### ABFmenu
Displays the menu with colors/comments/groups from cells.txt
```
http://192.168.1.225:8080/ABFmenu/X/Data/path/to/project
```

### ABFfolder
Displays folder-level (project-level) information.
This includes an experiments.txt editor
and an origin command generator.
* _Accepts POST to update experiments.txt_
```
http://192.168.1.225:8080/ABFfolder/X/Data/path/to/project
```

### ABFparent
Displays information about a parent ABF (shows all the child ABFs, images, and provides an interface to edit parent comment and color).

* _Accepts POST to update a cells.txt line (comment and color)_
* _Accepts POST to mark an ABF as ignored_

```
http://192.168.1.225:8080/ABFparent/X/Data/path/to/project/19702020
```
