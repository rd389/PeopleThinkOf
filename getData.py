import praw
from praw.models import MoreComments
import json

""" One issue I have now is that I seem to only be getting
 400-500 comments per submission, when there are literally
 thousands for the top all time submissions. I think it may
 have to do with the timing out or something. -- Investigate
 the replace_more function as specified in Reddit docs...
 Also try using this http://stackoverflow.com/questions/36366388/get-all-comments-from-a-specific-reddit-thread-in-python

 Another potential issue is that the comments list
 as is is flattened. Can make it a comment tree but is that
 necessary?

 File storage - best way to do it? JSON, CSV, ETC?

 Traffic rates...
 """

FILENAME = 'data.json'
LIMIT = 10

def main():
	file = open(FILENAME, 'w')
	file.write("[")
	reddit = praw.Reddit(client_id='C4P_wOzZQE7gPA',
	                     client_secret='aUitr4qdPNBk0wnJwobh2Y1t_Ms',
	                     user_agent='my user agent')

	subreddit = reddit.subreddit('IAmA')
	count = 0

	for ama in subreddit.top('all', limit = LIMIT):

		if "[AMA Request]" not in ama.title:
			submission = {
			"id" : ama.id,
			"title": ama.title,
			"category": ama.link_flair_css_class,
			"url" : ama.url,
			"author": ama.author.name,
			"comments": [], 
			"score": ama.score,
			"text": ama.selftext,
			"nsfw" : ama.over_18,
			"created": ama.created
			}

			ama.comments.replace_more(limit = 0)

			for comment in ama.comments.list():
				if comment.author is not None:
					submission["comments"] += [{
						"id" : comment.id, 
						"author" : comment.author.name,
						"depth": comment.depth,
						"parent_id": comment.parent_id ,
						"score": comment.score,
						"body": comment.body,
						"nsfw": ama.over_18,
						"created": comment.created,
						"post_title": ama.title,
						"post_url": ama.url,
						"category": ama.link_flair_css_class
					}]
			if count > 0:
				file.write(",")
			file.write(json.dumps(submission))
			count += 1
			print("Processed {}/{}".format(count, LIMIT))

	file.write(']')
	file.close()

if __name__ == '__main__':
	main()
	print("done!")
