from sqlalchemy import Table, Column, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy import ForeignKey, DateTime, Boolean, create_engine
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///OC_data.db')
Session = sessionmaker(bind=engine)
session = Session()


class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer(), primary_key=True)
    fullname = Column(String(80), index=True)
    email = Column(String(35), unique=True)
    username = Column(String(80), unique=True)
    password = Column(String(80))
    affiliation = Column(String(80))
    position = Column(String(80))
    city = Column(String(80))
    country = Column(String(80))
    is_author = Column(Boolean(), default=True)
    is_reviewer = Column(Boolean(), default=False)
    is_editor = Column(Boolean(), default=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __init__(self, fullname, email, username, password, affiliation, position, city, country):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.affiliation = affiliation
        self.position = position
        self.city = city
        self.country = country

    def __repr__(self):
        return "Author(fullname='{self.fullname}', " \
               "email = '{self.email}', " \
               "username = '{self.username}' " \
               ")".format(self=self)


class Reviewer(Base):
    __tablename__ = 'reviewers'

    reviewer_id = Column(Integer(), primary_key=True)
    author_id = Column(Integer(), ForeignKey('authors.author_id'), unique=True)
    date_of_first_review = Column(DateTime())
    date_of_latest_review = Column(DateTime())
    alias_nickname = Column(String(80))
    field_of_interest = Column(Integer(), ForeignKey('categories.category_id'))

    author = relationship("Author", backref=backref('reviewers', uselist=False))
    category = relationship("Category", backref=backref('reviewers', order_by=reviewer_id))

    def __init__(self, author_id, alias_nickname, field_of_interest):
        self.author_id = author_id
        self.alias_nickname = alias_nickname
        self.field_of_interest = field_of_interest


class Publet(Base):
    __tablename__ = 'publets'

    publet_id = Column(Integer(), primary_key=True)
    publet_title = Column(String(80), nullable=False)
    publet_description = Column(String(255))
    repository_user = Column(String(80))
    path_to_application = Column(String(80))
    guideline_objectives = Column(String(80))
    target_setting = Column(String(80))
    target_users = Column(String(80))
    publet_submitted_date_folios = Column(DateTime(), default=datetime.now)
    publet_submitted_date_review = Column(DateTime(), nullable=True)
    publet_published_date_repertoire = Column(DateTime(), nullable=True)
    publet_image = Column(String(255))
    author_id = Column(Integer(), ForeignKey('authors.author_id'))
    publet_status = Column(Integer(), ForeignKey('publet_status.publet_status_id'))
    category_id = Column(Integer(), ForeignKey('categories.category_id'))

    def __init__(self, publet_title, publet_description, repository_user, path_to_application, guideline_objectives, target_setting, target_users):
        self.publet_title = publet_title
        self.publet_description = publet_description
        self.repository_user = repository_user
        self.path_to_application = path_to_application
        self.guideline_objectives = guideline_objectives
        self.target_setting = target_setting
        self.target_users = target_users


class Publet_status(Base):
    __tablename__ = 'publet_status'

    publet_status_id = Column(Integer(), primary_key=True)
    publet_status_name = Column(String(50))

    def __init__(self, publet_status_name):
        self.publet_status_name = publet_status_name


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer(), primary_key=True)
    category_name = Column(String(50))

    def __init__(self, category_name):
        self.category_name = category_name


class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer(), primary_key=True)
    review_start_date = Column(DateTime(), default=datetime.now)
    review_desc = Column(String(255))
    review_public = Column(Boolean(), default=True)
    author_id = Column(Integer(), ForeignKey('authors.author_id'))
    publet_id = Column(Integer(), ForeignKey('publets.publet_id'))
    reviewer_1_id = Column(Integer(), ForeignKey('reviewers.reviewer_id'))
    reviewer_2_id = Column(Integer(), ForeignKey('reviewers.reviewer_id'))
    editor_first_verdict = Column(Integer(), ForeignKey('reviewer_verdict.reviewer_verdict_id'))
    reviewer_1_verdict = Column(Integer(), ForeignKey('reviewer_verdict.reviewer_verdict_id'))
    reviewer_2_verdict = Column(Integer(), ForeignKey('reviewer_verdict.reviewer_verdict_id'))
    editor_second_verdict = Column(Integer(), ForeignKey('reviewer_verdict.reviewer_verdict_id'))

    def __init__(self, review_desc, author_id, publet_id, reviewer_1_id, reviewer_2_id):
        self.review_desc = review_desc
        self.author_id = author_id
        self.publet_id = publet_id
        self.reviewer_1_id = reviewer_1_id
        self.reviewer_2_id = reviewer_2_id


class Reviewer_verdict(Base):
    __tablename__ = 'reviewer_verdict'

    reviewer_verdict_id = Column(Integer(), primary_key=True)
    review_id = Column(Integer(), ForeignKey('reviews.review_id'))
    reviewer_id = Column(Integer(), ForeignKey('reviewers.reviewer_id'))
    reviewer_verdict_date = Column(DateTime(), default=datetime.now)
    reviewer_verdict_type = Column(Integer(), ForeignKey('reviewer_verdict_type.reviewer_verdict_type_id'))
    reviewer_verdict_comment = Column(String(255))

    def __init__(self, review_id, reviewer_id, reviewer_verdict_type, reviewer_verdict_comment):
        self.review_id = review_id
        self.reviewer_id = reviewer_id
        self.reviewer_verdict_type = reviewer_verdict_type
        self.reviewer_verdict_comment = reviewer_verdict_comment


class Reviewer_verdict_type(Base):
    __tablename__ = 'reviewer_verdict_type'

    reviewer_verdict_type_id = Column(Integer(), primary_key=True)
    reviewer_verdict_type_name = Column(String(80))

    def __init__(self, reviewer_verdict_type_name):
        self.reviewer_verdict_type_name = reviewer_verdict_type_name
