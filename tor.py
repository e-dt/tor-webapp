from flask import Flask, request, render_template, redirect
import praw
app = Flask(__name__)
r = praw.Reddit(client_id='no', client_secret="no", password="no", user_agent='ToR Scraper 0.2.0', username="no")
tor = r.subreddit('TranscribersOfReddit')
already_seen=[] #ok, ok global vars are bad  
def getpost():
    global already_seen 
    for submission in tor.new(limit=1024): #generator, no performance badthing
        if submission.id in already_seen:
            continue
        if not submission.link_flair_text == "Unclaimed":
            continue
        return submission
@app.route("/")
def index():
    submission = getpost()
    reddit_url = submission.url
    iframe_url = praw.models.Submission(r, url=submission.url).url
    return render_template('index.html', iframe_url = iframe_url, id = submission.id, reddit_url= reddit_url)

@app.route("/post/<id>", methods=["POST", "GET"])
def post(id):
    global already_seen
    torsubmission = praw.models.Submission(r, id=id)
    #submission.reply("done")
    submission= praw.models.Submission(r, url=torsubmission.url)
    already_seen.append(id)
    submission.reply(request.form.get("formatText",""))
    torsubmission.reply("done")
    return redirect('/')

@app.route('/claim/<id>')
def claim(id):
    submission = praw.models.Submission(r, id=id)
    submission.reply("claim")
    print("Claimed %s" % id)
    return redirect('/')
@app.route('/skip/<id>')
def skip(id):
    global already_seen
    already_seen.append(id) 
    print("Skipped %s" % id)
    return redirect('/')
