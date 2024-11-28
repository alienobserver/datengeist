# Datengeist
## Application for easy understanding of unstructured data

Datengeist is a streamlit built application which is made to understand unstructured data through visualization 
of its components. Datengeist is working with **.csv** files. Datengeist has this key functionalities:

1. Categorization of features
2. Visualization of distributions
3. Convenient handling of missing data
4. Tools for feature comparison

To run datengeist you can install via pip

```
$ pip install datengeist
$ datengeist start
```

Or you can create a virtual environment and then run it (recommended)

```
$ python3 -m venv datengeist_env
$ source datengeist_env/bin/activate

$ pip install datengeist
```

### 1. Sample the Dataset
Sample the Dataset is where you can sample data, load it and have your first overview of the data
<img src="https://raw.githubusercontent.com/alienobserver/geist/refs/heads/main/datengeist/assets/git_images/Screenshot%20from%202024-11-13%2013-02-23.png" alt="screenshot" width="600" />

### 2. General Info
General Info is where you can divide your features into corresponding categories and view your
missing values in each feature

<img src="https://raw.githubusercontent.com/alienobserver/geist/refs/heads/main/datengeist/assets/git_images/Screenshot%20from%202024-11-13%2013-02-35.png" alt="screenshot" width="600" />

### 3. Feature Info
Feature Info is where you can view your features more closely, the distributions and missing value percentage
<img src="https://raw.githubusercontent.com/alienobserver/geist/refs/heads/main/datengeist/assets/git_images/Screenshot%20from%202024-11-13%2013-02-46.png" alt="screenshot" width="600" />
<img src="https://raw.githubusercontent.com/alienobserver/geist/refs/heads/main/datengeist/assets/git_images/Screenshot%20from%202024-11-13%2013-03-58.png" alt="screenshot" width="600" />

### 4. Relate Features
Relate Features is where you can view the correlation between your features and relate them via box plotting
<img src="https://raw.githubusercontent.com/alienobserver/geist/refs/heads/main/datengeist/assets/git_images/Screenshot%20from%202024-11-13%2013-04-22.png" alt="screenshot" width="600" />

### License 

Apache 2.0
