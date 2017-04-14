import json
f = open('data-1000.json')
data = json.load(f)

class Thread(object):
    def __init__(self, thread_id, title, url, category, op, date, nsfw):
        self.id = thread_id
        self.title = title
        self.url = url
        self.category = category
        self.op = op
        self.date = date
        self.nsfw = nsfw


class QAPair(object):
    def __init__(self, thread_id, op, AId, QId, AText, date, category, nsfw):
        self.op = op
        self.asker = ""
        self.answer_id = AId
        self.question_id = QId
        self.answer_text = AText
        self.question_text = ""
        self.thread_id = thread_id
        self.category = category
        self.nsfw = nsfw
        self.date = date

def fetch_qa(idx):
    thread = data[idx]
    thread_id = thread['id']
    op = thread['author']
    category = thread['category']
    nsfw = thread['nsfw']
    comments = thread["comments"][::-1]
    qa_pairs = {}
    need = {}
    result = []
    for c in comments:
        #Getting Answer
        if c["author"] == op:
            parent = c["parent_id"][3:]
            need[parent] = c["id"]
            qa_pairs[c["id"]] = QAPair(thread_id, c["author"], c["id"], parent, c['body'], c['created'], category, nsfw)
            
        #Getting Question
        elif c["id"] in need.keys():
            answerId = need[c["id"]]
            if answerId in qa_pairs.keys():
                comment_obj = qa_pairs[answerId]
                comment_obj.asker = c['author']
                comment_obj.question_text = c['body']
    
    for r in qa_pairs.values():
        result += [r.__dict__]
                
    return result



def createThread(idx):
    thread = data[idx]
    return Thread(thread['id'], thread['title'], thread['url'], thread['category'], thread['author'], thread['created'], thread['nsfw'])
 
def parseData(qa_fileName, threads_fileName):
	qa_pairs = []
	threads = []

	for i in range(len(data)):
    		qa_pairs += fetch_qa(i)
    		threads += [createThread(i).__dict__]

	with open(qa_fileName, "w") as qa_file:
		qa_file.write(json.dumps(qa_pairs))
		qa_file.close()

	with open(threads_fileName, "w") as threads_file:
		threads_file.write(json.dumps(threads))
		threads_file.close()



    