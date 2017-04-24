# Notes

## Virtual Env

Everytime you code you should use a virtual environment so that this better replicates how the app will behave on heroku (unaffected by all the stuff already installed on your computer).

1. Install virtualev
```
$ conda install virtualenv
```

2. Create a virtual environment (only have to do this once)
```
$ virtualenv <project-name>
```
This will create a folder `<project-name>` in your current directory.

3. Activate your virtual environment
```
$ source <project-name>/bin/activate
```

4. Install requirements
```
$ pip install -r requirements.txt
```

5. Include your `<project-name>` folder in `.gitignore`
```
# In .gitignore
...
<project-name>/
```

## Data Structures

- dictionary of AMA objects
    - key: id
    - value: object with fields:
      - id
      - title
      - url
      - category
      - op_name
      - date

- dictionary of QA pairs objects
    - key: (thread_id, answer_id)
    - value: object with fields:
      - answer_id
      - question_id
      - thread_id
      - date
      - answer_text
      - question_text
      - asker (name)
      - op_name

- tf-idf matrix for threads
- index (in tf-idf) to id

- tf-idf matrix for QA pairs
- index (in tf-idf) to id

- matrix of thread vectors
- QA pair to index


## To Do

- add titles to scores
- add empath
-
