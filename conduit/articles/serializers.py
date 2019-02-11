# coding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump

from conduit.profile.serializers import ProfileSchema


class TagSchema(Schema):
    name = fields.Str()
    featured = fields.Boolean()

    @post_dump()
    def dump_tag(self, data):
        return {'tag': data}

    class Meta:
        strict = True


class TagsSchema(TagSchema):

    @post_dump
    def dump_tag(self, data):
        return data

    @post_dump(pass_many=True)
    def dump_tags(self, data, many):
        return {'tags': data, 'tagsCount': len(data)}


class ArticleSchema(Schema):
    slug = fields.Str()
    title = fields.Str()
    description = fields.Str()
    createdAt = fields.DateTime()
    body = fields.Str()
    filePath = fields.Str()
    updatedAt = fields.DateTime(dump_only=True)
    author = fields.Str()
    article = fields.Nested('self', exclude=('article',), default=True, load_only=True)
    tagList = fields.List(fields.Str())
    favoritesCount = fields.Int(dump_only=True)
    favorited = fields.Bool(dump_only=True)
    featured = fields.Boolean()

    @pre_load
    def make_article(self, data):
        return data['article']

    @post_dump
    def dump_article(self, data):
        return {'article': data}

    class Meta:
        strict = True


class ArticleSchemas(ArticleSchema):

    @post_dump
    def dump_article(self, data):
        return data

    @post_dump(pass_many=True)
    def dump_articles(self, data, many):
        return {'articles': data, 'articlesCount': len(data)}


class CommentSchema(Schema):
    createdAt = fields.DateTime()
    body = fields.Str()
    updatedAt = fields.DateTime(dump_only=True)
    author = fields.Nested(ProfileSchema)
    id = fields.Int()

    # for the envelope
    comment = fields.Nested('self', exclude=('comment',), default=True, load_only=True)

    @pre_load
    def make_comment(self, data):
        return data['comment']

    @post_dump
    def dump_comment(self, data):
        data['author'] = data['author']['profile']
        return {'comment': data}

    class Meta:
        strict = True


class CommentsSchema(CommentSchema):

    @post_dump
    def dump_comment(self, data):
        data['author'] = data['author']['profile']
        return data

    @post_dump(pass_many=True)
    def make_comment(self, data, many):
        return {'comments': data}


article_schema = ArticleSchema()
articles_schema = ArticleSchemas(many=True)
comment_schema = CommentSchema()
comments_schema = CommentsSchema(many=True)
tag_schema = TagSchema()
tags_schema = TagsSchema(many=True)
