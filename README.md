# PeaTMOSS-Demos
A repository that holds demos on interactions with the PeaTMOSS Dataset, submitted to the MSR 2024 Mining Challenge.

Link to Globus Share containing all zipped repos and full metadata dataset: https://transfer.rcac.purdue.edu/file-manager?origin_id=c4ec6812-3315-11ee-b543-e72de9e39f95&origin_path=%2F


# include note about unzipping tar files


## Table of Contents

- [PeaTMOSS-Demos](#PeaTMOSS-Demos)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [Captured Model Hubs](#captured-model-hubs)
  - [Dependencies](#dependencies)
  - [How To Install](#how-to-install)
    - [From GitHub Releases](#from-github-releases)
    - [From Source](#from-source)
  - [How to Run](#how-to-run)
    - [As Individual Scripts](#as-individual-scripts)
  - [Data Representation](#data-representation)
  - [Pre-Packaged Dataset](#pre-packaged-dataset)
  - [Example Usage of Dataset](#example-usage-of-dataset)
  - [How to Cite](#how-to-cite)
  - [References](#references)

## About

This repository contains a sample of the *PeaTMOSS* dataset,
as well as scripts that demonstrate possible interactions with the SQLite database used to store the metadata dataset.
The *PeaTMOSS* dataset dataset contains snapshots of **P**re-**T**rained machine learning **M**odel (PTM) repositories and the downstream Open-Source GitHub repositories that reuse the PTMs,
metadata about the PTMs,
the pull requests and issues of the GitHub Repositories,
and links between the downstream GitHub repositories and the PTM models.
The schema of the SQLite database is specified by [PeaTMOSS.py](PeaTMOSS.py) and [PeatMOSS.sql](PeatMOSS.sql).
The sample of the database is [PeaTMOSS_sample.db](PeaTMOSS_sample.db).
The full database, as well as all captured repository snapshots are available here: https://transfer.rcac.purdue.edu/file-manager?origin_id=c4ec6812-3315-11ee-b543-e72de9e39f95&origin_path=%2F

### Captured Model Hubs

The following model hubs are captured in our database:

- [Hugging Face](https://huggingface.co/)
- [PyTorch Hub](https://pytorch.org/hub/)

## Dependencies

The scripts in the project depend upon the following software:

- [`Python 3.11`](https://www.python.org/downloads/release/python-3110/)
- [`SQLAlchemy 2.0`](https://www.sqlalchemy.org)

> Package dependencies are given in [`environment.yml`](environment.yml) and
> handled by [`anaconda`](https://anaconda.org/)

## How To Install

To run the scripts in this project, you must install python 3.11 and SQLAlchemy v2.0 or greater.

These package can be installed using the `anaconda` environment manager
1. Install the latest version of anaconda from [here](https://www.anaconda.com/download)
1. run `conda env create -f environment.yml` to create the anaconda environment `PeaTMOSS`
1. Activate the environment using `conda activate PeaTMOSS`

Alternatively, you can navigate to each packages respective pages and install them.

## How to Run

After [installing the anaconda environment](#how-to-install), each demo script can be run using `python3 script_name.py`

## Data Representation

Each model hub script generates the following directory structure **per model
hub**:

```shell
📦data
 ┗ 📂MODELHUB
 ┃ ┣ 📂html
 ┃ ┃ ┗ 📂metadata
 ┃ ┃ ┃ ┃ ┗ 📂models
 ┃ ┃ ┣ 📂json
 ┃ ┃ ┃ ┗ 📂metadata
 ┃ ┃ ┃ ┃ ┗ 📂models
 ┃ ┃ ┗ 📂repos
 ┃ ┃ ┃ ┗ 📂AUTHOR
 ┃ ┃ ┃ ┃ ┗ 📂MODEL
```


Where:

- data/`MODELHUB` is the same name as the `Python` module directory that
  contained the script.
- data/MODELHUB/repos/`AUTHOR` is the author name of the repository that was
  cloned.
- data/MODELHUB/repos/AUTHOR/`MODEL` is the name of the repository that was
  cloned.

Model hub scripts do not overwrite the directory. In other words, it is a safe
operation to run multiple model hub scripts from the same directory sequentially
or concurrently.

Specifics about the types of metadata files and content that are produced by the
scripts can be found in each model hub's script directory's `README.md` file.

## Full Dataset

An existing dataset is available on
[this Purdue University Globus share](https://app.globus.org/file-manager?origin_id=55e17a6e-9d8f-11ed-a2a2-8383522b48d9&origin_path=%2F%7E%2F).

If you are unfamiliar with Globus, we prepared a guide in the [globus-docs/](globus-docs/) directory.

## Example Usage of Dataset

An example usage of the dataset is described within the
[`example`](example/README.md) directory.

## How to Cite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7570357.svg)](https://doi.org/10.5281/zenodo.7570357)

This project has a DOI on [Zenodo](https://doi.org/10.5281/zenodo.7570357).
Please visit our Zenodo page for the latest citation information.

## References

> References are sorted by alphabetical order and not how they appear in this
> document.

\[1\] “Git.” <https://git-scm.com/> (accessed Jan. 25, 2023).

\[2\] “Git Large File Storage,” Git Large File Storage. <https://git-lfs.com/>
(accessed Jan. 25, 2023).

\[3\] “Hugging Face – The AI community building the future.,” Jan. 03, 2023.
<https://huggingface.co/> (accessed Jan. 25, 2023).

\[4\] “Model Zoo - Deep learning code and pretrained models for transfer
learning, educational purposes, and more.” <https://modelzoo.co/> (accessed Jan.
25, 2023).

\[5\] “Modelhub.” <https://modelhub.ai/> (accessed Jan. 25, 2023).

\[6\] “MSR 2023 - Data and Tool Showcase Track - MSR 2023.”
<https://conf.researchr.org/track/msr-2023/msr-2023-data-showcase> (accessed
Jan. 25, 2023).

\[7\] “ONNX Model Zoo.” Open Neural Network Exchange, Jan. 25, 2023. Accessed:
Jan. 25, 2023. \[Online\]. Available: <https://github.com/onnx/models>

\[8\] “pip documentation v22.3.1.” <https://pip.pypa.io/en/stable/> (accessed
Jan. 25, 2023).

\[9\] “Poetry - Python dependency management and packaging made easy.”
<https://python-poetry.org/> (accessed Jan. 25, 2023).

\[10\] “Python Release Python 3.10.9,” Python.org.
<https://www.python.org/downloads/release/python-3109/> (accessed Jan. 25,
2023).

\[11\] “PyTorch Hub.” <https://www.pytorch.org/hub> (accessed Jan. 25, 2023).

\[12\] W. Jiang et al., “SoftwareSystemsLaboratory/PTMTorrent.” Zenodo, Jan. 25,
2023\. doi: 10.5281/zenodo.7570357.



# Introduction

The PTMTorrent dataset is available for download from Purdue University via a Globus share.

[Globus](https://www.globus.org) is a data management and transfer service designed for working with large-scale data.

If you have not used Globus before, this document describes the setup steps necessary to get access to the data.
After finishing this guide, you will have downloaded the smallest piece of PTMTorrent onto your computer (less than 1GB of data).
You can follow similar steps to get the rest.

If your institution has large compute resources, the IT staff may already have a large storage system with a Globus front-end, and you can download PTMTorrent directly onto that storage system.

# Steps

1. Visit the PTMTorrent URL from the paper, and you'll get to a Globus login page.

![GLobus login page](images/1-globus-landing.jpg)

2. Sign in through your organization, Google, or ORCID. I used ORCID in this example.

![ORCID sign-in](images/2-globus-orcid.jpg)

3. Successful login through ORCID.

![ORCID success](images/3-globus-loggedin.jpg)

4. Globus asks for some more permissions.

![Globus permissions request](images/4-globus-orcidperms.jpg)

5. We have reached the PTMTorrent share within Purdue's Globus service.

![PTMTorrent share](images/5-ptmtorrentLanding.jpg)

6. *(This is a side note)*. If your institution has a Globus instance, you might be able to right-click on the item of interest, get the link, and access it from your destination Globus. This link cannot be used via `wget` or similar.

![One download approach](images/6-ptmtorrent-download1.jpg)

7. Let's download something onto our workstation. You will need to install the Globus client on your machine. Visit https://www.globus.org/globus-connect-personal and follow the instructions.

8. Now we can see two shares in the Globus view: "My Laptop" (your workstation) and "PTMTorrent" (Purdue's Globus share) side by side in two panels. On your local share, pick the folder you want the data to land in. Then, on the PTMTorrent side, select the data you want and press the "Start" button. That button has a left-arrow pointing towards the destination share.

![Local share preparing to transfer from Purdue](images/7-ptmtorrent-DownloadViaClient-1.jpg)

9. In the "Activity" tab we can see that the task has queued.

![Task queued in the Activity tab](images/8-ptmtorrent-downloadViaClient-TaskQueued.jpg)

10. An email success notification.

![Email success notification](images/9-ptmtorrent-downloadViaClient-success.jpg)

11. I went to my Downloads/ folder and ran `tar -xzvf modelhub.tar.gz` and then `cd data/modelhub`. Let's see what is in the `repos` folder:

![The repos folder lists all models from this hub, in directories corresponding to their owner](images/10-downloadSuccess-allModels.jpg)

12. Within the `data/modelhub/repos/modelhub-ai/yolo-v3` PTM package, we see a git repository with 8 commits.

![YOLO-v3](images/11-downloadsuccess-yolov3Commits.jpg)

13. Happy mining!
