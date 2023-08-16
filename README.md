# PeaTMOSS-Demos
A repository that holds demos on interactions with the PeaTMOSS Dataset, submitted to the MSR 2024 Mining Challenge.


## Globus Share

All zipped repos and the full metadata dataset are available through Globus Share: https://transfer.rcac.purdue.edu/file-manager?origin_id=c4ec6812-3315-11ee-b543-e72de9e39f95&origin_path=%2F

If you do not have an account, follow the Globus docs on how to sign up: https://docs.globus.org/how-to/get-started/. You may create an account through a partnered organization if you are a part of that organization, or through Google or ORCID accounts.

# include note about unzipping tar files



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

## Table of Contents
The content for each specific model hub is listed in the table below:

|   Model hub  |  #PTMs  | #Snapshotted Repos | #Discussions (PRs, issues) | #Links | Size of Zipped Snapshots |
|:------------:|:-------:|:------------------:|:--------------------------:|:------:|:------------------------:|
| Hugging Face | 281,276 |       14,899       |           19,436           | 30,514 |           44TB           |
|  PyTorch Hub |   362   |         361        |           54,064           | 13,823 |           1.3GB          |

We also offer two different formats of our datasets to facilitate the mining challenge for participants. An overview of these two formats can be found in the table below:
|  Formats |                                                                    Description                                                                   |  Size  |
|:--------:|:------------------------------------------------------------------------------------------------------------------------------------------------:|:------:|
| Metadata |                          It contains only the metadata of the PTM packagesr and a subset of the GitHub project metadata.                         |  6.7GB |
|   Full   | It contains all metadata, adding the PTM package contents in each published version, and git history of the main branhes of the GitHub projects. | 48.2TB |

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

## Tutorial
This section will explain how to use SQL and SQLAlchemy to interact with the database to answer the research questions outlined in the proposal. 

### Using SQL to query the database
The metadata dataset is stored in a SQLite database file called PeaTMOSS.db, which can be found in the Globus Share: https://transfer.rcac.purdue.edu/file-manager?origin_id=c4ec6812-3315-11ee-b543-e72de9e39f95&origin_path=%2F. This file can be queried through standard SQL queries, and this can be done from a terminal using sqlite3: https://sqlite.org/cli.html. Single queries can be executed like ```sqlite3 PeaTMOSS.db '{query statement}'```. Alternatively, you can start an SQLite instance by simply executing ```sqlite3 PeaTMOSS.db```, which can be terminated by CTRL + D. To output queries to files, the .output command can be used as such: ```sqlite> .output {filename}.txt```. The following example has to do with research question GH2: "What do developers on GitHub discuss related to PTM use, e.g., in issues, and pull requests? What are developers’ sentiments regarding PTM use? Do the people do pull requests of PTMs have the right expertise?" 

If someone wants to observe what developers on GitHub are currently discussing related to PTM usage, they can look at discussions in GitHub issues and pull requests. The following SQLite example shows queries that would help accomplish this task.

First, we will create an sqlite3 instance:
```$ sqlite3 PeaTMOSS.db```

Then, we will create an output file for our issues query, then execute that query:
```
sqlite> .output issues.txt
sqlite> SELECT id, title FROM github_issue WHERE state = 'OPEN' ORDER BY updated_at DESC LIMIT 100;
```
Output:
<img width="614" alt="6c66d24cac7cf9542f91d4a875bb1abe" src="https://github.com/PurdueDualityLab/PeaTMOSS-Demos/assets/70859381/3f6d9508-76de-4386-808b-0d9157a8392b">

The above query selects the ID and Title fields from the github_issue table, and chooses the 100 most recent issues that are still open.

Next, we will create an output file for our pull requests query, then execute that query:
```
sqlite> .output pull_requests.txt
sqlite> SELECT id, title FROM github_pull_request WHERE state = 'OPEN' OR state = 'MERGED' ORDER BY updated_at DESC LIMIT 100;
```
Output:
![Alt text](image-1.png)
Notice that the query is very similar to the issues query, as we are looking for similar information. The above query selects the ID and Title fields from the github_pull_request table, and chooses the 100 most recent pull requests that are either open or merged.

Querying this data can assist when beginning to observe current/recent discussions in GitHub about PTMs. From here, you may adjust these queries to include more/less entries by changing the LIMIT value, or you may adjust which fields the queries return. For example, if you want more detailed information you could select the "body" field in either table.


## How to Run

After [installing the anaconda environment](#how-to-install), each demo script can be run using `python3 script_name.py`
