from tff.db import db


article_tag = db.Table(
    'article_tag',
    db.Column('article', db.Integer, db.ForeignKey('article.id')),
    db.Column('tag', db.Integer, db.ForeignKey('tag.id'))
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    articles = db.relationship('Article',
                               secondary=article_tag,
                               back_populates='tags')


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    slug = db.Column(db.Text, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date)
    description = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255))

    tags = db.relationship('Tag',
                           secondary=article_tag,
                           back_populates='articles')

    __mapper_args__ = {
        'polymorphic_identity': 'article',
        'polymorphic_on': type
    }


class FeaturedArticle(Article):
    id = db.Column(db.Integer, db.ForeignKey('article.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'featured_article',
    }
