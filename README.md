# Coverage of DOAJ journals' citations through OpenCitations
[![DOI](https://zenodo.org/badge/486368166.svg)](https://zenodo.org/badge/latestdoi/486368166)

This is the repository for the software of the research "Coverage of DOAJ journals' citations through OpenCitations" made in the context of the Open Science course of 21/22 of University of Bologna held by professor Silvio Peroni.

## Reproduce Our Experiment


### 1. Install

install repo with setup.py tools, launching this command:

```bash
pip install setup.py
```
### 2. Run configuration

Then run the _config_ command for generating the .env file, storing all the information about paths, and
starting the Virtual Environment

```bash
start-venv
```

### 3. Run processing steps

Run the program launch the _run_ command.

```bash
run
```

**If you want to run a specific command** comment out one or more commands script in the _run.bat_ file. Otherwise
you can run a specific command from run directory:

```bash
cd run
```

and then run the command that you prefer:

```bash
python <command>
```

**WARNING**: running a specific command some errors might occur, due to the fact that sometimes the scripts depends on 
each other.

### 4. Output

You can find the output of the running process inside the output repository specified above.

## Hardware Configurations
Our experiment was made on a machine with this hardware configurations:
* CPU: Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz   2.59 GHz
* RAM: 20,0 GB (19,9 GB usable)
* Storage: 200 GB

## Source datasets
* [DOAJ public articles data dump](https://doaj.org/public-data-dump/article) (May 01, 2022)
* [DOAJ public journals data dump](https://doaj.org/public-data-dump/journal) (May 07, 2022)
* [OpenCitations COCI dump](https://opencitations.net/download#coci) (March 2022)

## Other Useful Things

* [The Data Management Plan](https://doi.org/10.5281/zenodo.6417367)
* [The Protocol](https://dx.doi.org/10.17504/protocols.io.n92ldz598v5b/v4)
* [The Article](https://doi.org/10.5281/zenodo.6574741)
* [The Results](https://doi.org/10.5281/zenodo.6573890)
* [The Sister Research](https://github.com/open-sci/2021-2022-la-chouffe-code)
* [The Presentation](https://doi.org/10.5281/zenodo.6579115)
