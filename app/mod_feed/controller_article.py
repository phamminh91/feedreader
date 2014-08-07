from app import db
from app.mod_feed import mod_feed
from app.models import FeedArticle,		\
					   FeedVote

from flask import render_template,		\
				  abort,				\
				  redirect,				\
				  jsonify,				\
				  request,				\
				  url_for
from flask.ext.login import login_required,		\
							current_user

"""
Upvote
Downvote
Remove Vote
Upview
"""

@mod_feed.route('/article/')
def read_article():
	article_id = request.args.get('article_id')
	if not article_id:
		return render_template(url_for('mod_feed.index'))

	article = FeedArticle.query.get(article_id)

	if not article:
		abort(404)

	a = {
		'link': article.link,
		'readable': article.readable_content
	}

	return render_template('read.html', article = a)


@mod_feed.route('/upvote')
@login_required
def upvote():
	article_id = request.args.get('article_id')

	if not article_id:
		return redirect(url_for('mod_main.all_feeds'))

	article = FeedArticle.query.get(article_id)

	# Article does not exist
	if not article:
		abort(404)

	vote = FeedVote.query.filter_by(user_id = current_user.id, article_id = article_id).first()

	# No vote from the user yet, add one
	if not vote:
		vote = FeedVote(user_id = current_user.id, article_id = article_id, is_upvote = True)
		article.upvote += 1
		article.update_wilson_score()
		db.session.add(vote)
	else:
		if not vote.is_upvote:
			vote.is_upvote = True
			article.upvote += 1
			article.downvote -= 1
			article.update_wilson_score()

	return redirect(url_for('mod_feed.index'))


@mod_feed.route('/downvote')
@login_required
def downvote():
	article_id = request.args.get('article_id')

	if not article_id:
		return redirect(url_for('mod_main.all_feeds'))

	article = FeedArticle.query.get(article_id)

	# Article does not exist
	if not article:
		abort(404)

	vote = FeedVote.query.filter_by(user_id = current_user.id, article_id = article_id).first()

	# No vote from the user yet, add one
	if not vote:
		vote = FeedVote(user_id = current_user.id, article_id = article_id, is_upvote = False)
		article.downvote += 1
		article.update_wilson_score()
		db.session.add(vote)
	else:
		if vote.is_upvote:
			vote.is_upvote = False
			article.upvote -= 1
			article.downvote += 1
			article.update_wilson_score()

	return redirect(url_for('mod_feed.index'))


@mod_feed.route('/remove_vote')
@login_required
def remove_vote():
	article_id = request.args.get('article_id')

	if not article_id:
		return redirect(url_for('mod_main.all_feeds'))

	article = FeedArticle.query.get(article_id)

	# Article does not exist
	if not article:
		abort(404)

	if article:
		vote = FeedVote.query.filter_by(user_id = current_user.id, article_id = article_id).first()
		if vote:
			if vote.is_upvote:
				article.upvote -= 1
			else:
				article.downvote -= 1
			article.update_wilson_score()
			db.session.delete(vote)

	return redirect(url_for('mod_feed.index'))


@mod_feed.route('/upview/')
def upviews():

	article_id = request.args.get('article_id')


	if not article_id:
		return jsonify({'error': 'invalid parameter', 'message': 'article_id not provided'})

	article = FeedArticle.query.get(article_id)

	if not article:
		return jsonify({'error': 'resource not found', 'message': 'no article with that id'})

	article.views += 1

	return jsonify({'article_id': article_id, 'article_views': article.views})