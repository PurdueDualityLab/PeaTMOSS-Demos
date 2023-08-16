# PeaTMOSS-Demos
A repository that holds demos on interactions with the PeaTMOSS Dataset, submitted to the MSR 2024 Mining Challenge.


## Globus

### Globus Share
All zipped repos and the full metadata dataset are available through Globus Share: https://transfer.rcac.purdue.edu/file-manager?origin_id=c4ec6812-3315-11ee-b543-e72de9e39f95&origin_path=%2F

If you do not have an account, follow the Globus docs on how to sign up: https://docs.globus.org/how-to/get-started/. You may create an account through a partnered organization if you are a part of that organization, or through Google or ORCID accounts.

### Globus Connect Personal
To access the metadata dataset using the globus.py script provided in the repository, follow the instructions to download Globus Connect Personal to create your own private Globus collection: https://docs.globus.org/how-to/globus-connect-personal-windows/. Once this is created, ensure the application is running before running globus.py. In some cases, you may run into permission issues on Globus when running the script. If this is the case, look for the line: ```local_endpoint_id = local_endpoint.endpoint_id```, as you will need to change "local_endpoint.endpoint_id" to your private collection's UUID. To locate this, right click on your Globus icon on your taskbar, and select "Web: Collection Details". Once this page opens, scroll down to the bottom where the UUID field for your collection should be visible. Terminate the existing transfer, replace the variable with your collection's UUID as a string, and rerun globus.py.

 
## Table of Contents
- [PeaTMOSS Demos](#peatmoss-demos)
  - [Metadata Description](#metadata-description)
  - [About](#about)
    - [Captured Model Hubs](#captured-model-hubs)
  - [Dependencies](#dependencies)
  - [How To Install](#how-to-install)
  - [Tutorial](#tutorial)
  - [How to Run](#how-to-run)


## Metadata Description
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
#### Note: When unzipping .tar.gz snapshots, include the --strip-components=4 flag in the tar statement, ex: tar --strip-components=4 -xvzf {name}.tar.gz. If you do not do this, you will have 4 extraneous parent directories that encase the repository.

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
One option users have to interact with the metadata dataset is to use plain SQL. The metadata dataset is stored in a SQLite database file called PeaTMOSS.db, which can be found in the Globus Share: https://transfer.rcac.purdue.edu/file-manager?origin_id=c4ec6812-3315-11ee-b543-e72de9e39f95&origin_path=%2F. This file can be queried through standard SQL queries, and this can be done from a terminal using sqlite3: https://sqlite.org/cli.html. Single queries can be executed like ```sqlite3 PeaTMOSS.db '{query statement}'```. Alternatively, you can start an SQLite instance by simply executing ```sqlite3 PeaTMOSS.db```, which can be terminated by CTRL + D. To output queries to files, the .output command can be used as such: ```sqlite> .output {filename}.txt```. The following example has to do with research question GH2: "What do developers on GitHub discuss related to PTM use, e.g., in issues, and pull requests? What are developers’ sentiments regarding PTM use? Do the people do pull requests of PTMs have the right expertise?" 

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

<img width="611" alt="b128657ee024e2441110090f3bc19ea6" src="https://github.com/PurdueDualityLab/PeaTMOSS-Demos/assets/70859381/b3773972-9dd0-43e6-8244-3ab1ac94d4dc">

Notice that the query is very similar to the issues query, as we are looking for similar information. The above query selects the ID and Title fields from the github_pull_request table, and chooses the 100 most recent pull requests that are either open or merged.

Querying this data can assist when beginning to observe current/recent discussions in GitHub about PTMs. From here, you may adjust these queries to include more/less entries by changing the LIMIT value, or you may adjust which fields the queries return. For example, if you want more detailed information you could select the "body" field in either table.


### Using ORMs to query the database

This section will include more details about the demo provided in the repository, PeaTMOSS_demo.py. Once again, this method requires the PeaTMOSS.db file, which can be found in the Globus Share: https://transfer.rcac.purdue.edu/file-manager?origin_id=c4ec6812-3315-11ee-b543-e72de9e39f95&origin_path=%2F. Prior to running this demo, ensure that the conda environment has been created and activated, or you may run into errors. 

The purpose of the demo, as described at by the comment at the top of its file, is to demonstrate how one may use SQLAlchemy to address one of the research questions. The question being addressed in the demo is I1: "It can be difficult to interpret model popularity numbers by download rates. To what extent does a PTM’s download rates correlate with the number of GitHub projects that rely on it, or the popularity of the GitHub projects?". The demo accomplishes this by looking at two main fields: the number of times a model is downloaded from its model hub, and the number of times a model is reused in a GitHub repository. The demo finds the 100 most downloaded models, and finds how many times each of those models are reused. Users can take this information and attempt to find a correlation.

PeaTMOSS_demo.py utilizes PeaTMOSS.py, which is used to describe the structure of the database so that we may interact with it using SQLAlchemy. To begin, you must create and SQLAlchemy engine using the database file: ```engine = sqlalchemy.create_engine(f"sqlite:///{absolute_path}")```, where absolute_path is a string that describes the filepath of the database file. Relative paths are also acceptable. 

To find the 100 most downloaded models, we will query the model table
```
query_name_downloads = sqlalchemy.select(PeaTMOSS.Model.id, PeaTMOSS.Model.context_id, PeaTMOSS.Model.downloads) \
            .limit(100).order_by(sqlalchemy.desc(PeaTMOSS.Model.downloads))
```
and execute the query
```
models = session.execute(query_name_downloads).all()
```

For each of these models, we want to know how many times they are being reused. The model_to_reuse_repository contains fields for model IDs and reuse repository IDs, effectively linking them together. If a model is reused in multiple repository its ID will show up multiple times in the model_to_reuse_repository table. Therefore, we want to see if these highly downloaded models are also highly reused. We can do this querying the model_to_reuse_repository table and only select entries where the model_id field is equivalent to the current model's ID:

```
for model in models:
    ...
    query_num_reuses = sqlalchemy.select(PeaTMOSS.model_to_reuse_repository.columns.model_id) \
                .where(PeaTMOSS.model_to_reuse_repository.columns.model_id == model.id)

```
This query will select all the instances of the current model's ID appears in the model_to_reuse_repository table. If we execute this query and count the number of elements in the result, we have the number of times that model has been reused:
```num_reuses = len(session.execute(query_num_reuses).all())```

In each iteration of the loop we can store this information in dictionaries, where the keys can be the names of the models:
```
for model in models:
    highly_downloaded[model.context_id] = model.downloads
    ...
    ...
    reused_rates[model.context_id] = num_reuses
```
And then at the end, we can simply print the results. From there, users may observe a level of correlation using a method they see fit. 

Download Results:

<img width="649" alt="5349fd8861432ed693ca27429f569eb3" src="https://github.com/PurdueDualityLab/PeaTMOSS-Demos/assets/70859381/f5d6ee38-adf1-4978-9ae4-6eedb4f5e9be">

Reuse Results:

<img width="656" alt="003113aa18d146f9babc7e9ae1c6c3e0" src="https://github.com/PurdueDualityLab/PeaTMOSS-Demos/assets/70859381/6b835260-8afa-4f1b-9104-9d6a54c9ed44">

## How to Run

After [installing the anaconda environment](#how-to-install), each demo script can be run using `python3 script_name.py`
