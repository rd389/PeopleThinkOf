#Notes

##Data Structures

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
 - 
