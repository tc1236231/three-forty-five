# coding: utf-8

import datetime as dt

from flask import Blueprint, jsonify
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user, jwt_required, jwt_optional
from marshmallow import fields

from conduit.database import db
from conduit.exceptions import InvalidUsage
from conduit.user.models import User
from .models import Article, Tags, Comment
from .serializers import (article_schema, articles_schema, comment_schema,
                          comments_schema, tag_schema, tags_schema)

blueprint = Blueprint('articles', __name__)


##########
# Articles
##########

@blueprint.route('/api/articles', methods=('GET',))
@jwt_optional
@use_kwargs({'tag': fields.Str(), 'author': fields.Str(),
             'favorited': fields.Str(), 'featured': fields.Boolean(), 'latest': fields.Boolean(), 'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(articles_schema)
def get_articles(tag=None, author=None, favorited=None, featured=None, latest=None, limit=20, offset=0):
    res = Article.query
    if tag:
        res = res.filter(Article.tagList.any(Tags.name == tag))
    if author:
        res = res.join(Article.author).join(User).filter(User.username == author)
    if favorited:
        res = res.join(Article.favoriters).filter(User.username == favorited)
    if featured:
        res = res.filter(Article.featured == featured)
    if latest:
        res = res.order_by(Article.createdAt.desc())
    return res.offset(offset).limit(limit).all()


@blueprint.route('/api/articles', methods=('POST',))
@jwt_optional
@use_kwargs(article_schema)
@marshal_with(article_schema)
def make_article(filePath, title, description, author, tagList=None, featured=False):
    article = Article(title=title, description=description, filePath=filePath,
                      author=author, featured=featured)
    existing_article = Article.query.filter_by(slug=article.slug).first()
    if existing_article is not None:
        raise InvalidUsage.article_already_exist()
    if tagList is not None:
        for tag in tagList:
            mtag = Tags.query.filter_by(name=tag).first()
            if not mtag:
                mtag = Tags(tag)
                mtag.save()
            article.add_tag(mtag)
    article.save()
    return article


@blueprint.route('/api/articles/<slug>', methods=('PUT',))
@jwt_optional
@use_kwargs(article_schema)
@marshal_with(article_schema)
def update_article(slug, **kwargs):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    article.update(updatedAt=dt.datetime.utcnow(), **kwargs)
    article.save()
    return article


@blueprint.route('/api/articles/<slug>', methods=('DELETE',))
@jwt_optional
def delete_article(slug):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    article.delete()
    return '', 200


@blueprint.route('/api/articles/all/<key>', methods=('DELETE',))
@jwt_optional
def delete_all_articles(key):
    if key != 'k2h6o1':
        return '', 422

    num_rows_deleted = 0
    articles = db.session.query(Article).all()
    for article in articles:
        article.delete()
        num_rows_deleted += 1
    return str(num_rows_deleted), 200


@blueprint.route('/api/articles/<slug>', methods=('GET',))
@jwt_optional
@marshal_with(article_schema)
def get_article(slug):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    return article


@blueprint.route('/api/articles/<slug>/favorite', methods=('POST',))
@jwt_required
@marshal_with(article_schema)
def favorite_an_article(slug):
    profile = current_user.profile
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    article.favourite(profile)
    article.save()
    return article


@blueprint.route('/api/articles/<slug>/favorite', methods=('DELETE',))
@jwt_required
@marshal_with(article_schema)
def unfavorite_an_article(slug):
    profile = current_user.profile
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    article.unfavourite(profile)
    article.save()
    return article


@blueprint.route('/api/articles/feed', methods=('GET',))
@jwt_required
@use_kwargs({'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(articles_schema)
def articles_feed(limit=20, offset=0):
    return Article.query.join(current_user.profile.follows). \
        order_by(Article.createdAt.desc()).offset(offset).limit(limit).all()


######
# Tags
######

@blueprint.route('/api/tags', methods=('GET',))
@use_kwargs({'featuredOnly': fields.Boolean(), 'limit': fields.Int()})
@marshal_with(tags_schema)
def get_tags(featuredOnly=False, limit=None):
    res = Tags.query
    if featuredOnly:
        res = res.filter(Tags.featured)
    if limit:
        res = res.limit(limit)
    return res.all()


@blueprint.route('/api/tags/feature', methods=('POST',))
@use_kwargs({'name': fields.Str()})
@marshal_with(tag_schema)
def feature_a_tag(name):
    tag = Tags.query.filter(Tags.name == name).first()
    if not tag:
        raise InvalidUsage.tag_not_found()
    tag.update(featured=True)
    tag.save()
    return tag


##########
# Comments
##########


@blueprint.route('/api/articles/<slug>/comments', methods=('GET',))
@marshal_with(comments_schema)
def get_comments(slug):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    return article.comments


@blueprint.route('/api/articles/<slug>/comments', methods=('POST',))
@jwt_required
@use_kwargs(comment_schema)
@marshal_with(comment_schema)
def make_comment_on_article(slug, body, **kwargs):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    comment = Comment(article, current_user.profile, body, **kwargs)
    comment.save()
    return comment


@blueprint.route('/api/articles/<slug>/comments/<cid>', methods=('DELETE',))
@jwt_required
def delete_comment_on_article(slug, cid):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()

    comment = article.comments.filter_by(id=cid, author=current_user.profile).first()
    comment.delete()
    return '', 200
