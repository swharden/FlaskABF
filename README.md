# FlaskABF
**FlaskABF is a Python-based web application designed to browse and analyze electrophysiology data stored as Axon Binary Format (ABF) files.** A [Flask web server](http://flask.pocoo.org) allows simple experiment folder browsing and display of ABF information (with [pyABF](https://github.com/swharden/pyABF)). Creation of analysis graphs is achieved by [pyABFauto](https://github.com/swharden/pyABFauto) which analyzes new ABF files as they appear (ideal for use on multi-user network drives). Experiment notes and cell notes can also be edited from the web interface.

![](dev/screenshot.png)


This project replaces abandonware like [SWHLab](https://github.com/swharden/SWHLab) (for auto-analysis) and [SWHLabPHP](https://github.com/swharden/SWHLabPHP) (for web browser navigation).