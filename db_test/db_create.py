from db_test.db_model import Base, session, engine, Author, Review, Reviewer, Publet, Publet_status, Category, Reviewer_verdict, Reviewer_verdict_type
from datetime import datetime


###################
## Dummy data
###################


def add_author():
    author_1 = Author(fullname='Gopikrishnan Chandrasekharan', email='ezgopi@gmail.com', username='gopi', password='111222', affiliation='City, University of London',
                      position='PhD student', city='London', country='United Kingdom')
    author_2 = Author(fullname='Hywel Curtis', email='hywel@gmail.com', username='hywel', password='111222', affiliation='OpenClinical.net', position='Knowledge engineer',
                      city='Manchester', country='United Kingdom')
    author_3 = Author(fullname='John Fox', email='john@gmail.com', username='john', password='111222', affiliation='Oxford University', position='Professor', city='Oxford',
                      country='United Kingdom')
    session.add(author_1)
    session.add(author_2)
    session.add(author_3)
    session.commit()


def add_category():
    category_1 = Category(category_name='Dentistry')
    category_2 = Category(category_name='Ophthalmology')
    category_3 = Category(category_name='Cardiology')
    session.add(category_1)
    session.add(category_2)
    session.add(category_3)
    session.commit()


def add_reviewer():
    a1 = session.query(Author.author_id).filter(Author.username == 'gopi').scalar()
    c1 = session.query(Category.category_id).filter(Category.category_name == 'Dentistry').scalar()
    r1 = Reviewer(author_id=a1, alias_nickname='gopi', field_of_interest=c1)
    r1.date_of_first_review = datetime.now()
    r1.date_of_latest_review = datetime.now()

    a2 = session.query(Author.author_id).filter(Author.username == 'hywel').scalar()
    c2 = session.query(Category.category_id).filter(Category.category_name == 'Ophthalmology').scalar()
    r2 = Reviewer(author_id=a2, alias_nickname='hywel', field_of_interest=c2)
    r2.date_of_first_review = datetime.now()
    r2.date_of_latest_review = datetime.now()

    a3 = session.query(Author.author_id).filter(Author.username == 'john').scalar()
    c3 = session.query(Category.category_id).filter(Category.category_name == 'Cardiology').scalar()
    r3 = Reviewer(author_id=a3, alias_nickname='JohnFox', field_of_interest=c3)
    r3.date_of_first_review = datetime.now()
    r3.date_of_latest_review = datetime.now()

    session.add(r1)
    session.add(r2)
    session.add(r3)
    session.commit()


def add_publet_status():
    ps1 = Publet_status(publet_status_name='Currently submitted for review')
    ps2 = Publet_status(publet_status_name='Submitted for review')
    ps3 = Publet_status(publet_status_name='Submitted and undergoing review')
    ps4 = Publet_status(publet_status_name='Review process completed and accepted for publication')
    ps5 = Publet_status(publet_status_name='Published')
    ps6 = Publet_status(publet_status_name='Rejected')
    session.bulk_save_objects([ps1, ps2, ps3, ps4, ps5, ps6])
    session.commit()


def add_publet():
    p1 = Publet(publet_title='Dentistry', publet_description='Publet for dentistry', repository_user='gopi', path_to_application='public/CAMBRA-V2',
                guideline_objectives='Diagnose dental pain', target_setting='Dental primary care', target_users='Dentists')
    p1.author_id = session.query(Author.author_id).filter(Author.username == 'gopi').scalar()
    p1.publet_status = session.query(Publet_status.publet_status_id).filter(Publet_status.publet_status_id == 1).scalar()
    p1.category_id = session.query(Category.category_id).filter(Category.category_id == 1).scalar()

    session.add(p1)
    session.commit()


def add_reviewer_verdict_type():
    r1 = Reviewer_verdict_type(reviewer_verdict_type_name='Accepted')
    r2 = Reviewer_verdict_type(reviewer_verdict_type_name='Rejected')
    session.bulk_save_objects([r1, r2])
    session.commit()


def add_review():
    a1 = session.query(Author.author_id).filter(Author.username == 'gopi').scalar()
    p1 = session.query(Publet.publet_id).filter(Publet.publet_id == 1).scalar()
    reviewer_1 = session.query(Reviewer.reviewer_id).filter(Reviewer.reviewer_id == 2).scalar()
    reviewer_2 = session.query(Reviewer.reviewer_id).filter(Reviewer.reviewer_id == 3).scalar()
    review_1 = Review(review_desc='First review', author_id=a1, publet_id=p1, reviewer_1_id=reviewer_1, reviewer_2_id=reviewer_2)
    session.add(review_1)
    session.commit()


def add_reviewer_verdict():
    review_id = session.query(Review.review_id).filter(Review.review_id == 1).scalar()
    qry = session.query(Reviewer.reviewer_id)
    qry = qry.filter(Reviewer.author_id == Author.author_id)
    reviewer_1 = qry.filter(Author.username == 'hywel').scalar()
    reviewer_2 = qry.filter(Author.username == 'john').scalar()

    reviewer_1_verdict_type = session.query(Reviewer_verdict_type.reviewer_verdict_type_id).filter(Reviewer_verdict_type.reviewer_verdict_type_name == 'Accepted').scalar()
    reviewer_2_verdict_type = session.query(Reviewer_verdict_type.reviewer_verdict_type_id).filter(Reviewer_verdict_type.reviewer_verdict_type_name == 'Accepted').scalar()

    reviewer_verdict_1 = Reviewer_verdict(review_id=review_id, reviewer_id=reviewer_1, reviewer_verdict_type=reviewer_1_verdict_type,
                                          reviewer_verdict_comment='This is a good publet')
    reviewer_verdict_2 = Reviewer_verdict(review_id=review_id, reviewer_id=reviewer_2, reviewer_verdict_type=reviewer_2_verdict_type,
                                          reviewer_verdict_comment='This is a very good publet')

    session.add(reviewer_verdict_1)
    session.add(reviewer_verdict_2)
    session.commit()


def update_review():
    qry1 = session.query(Reviewer_verdict.reviewer_verdict_id)
    qry1 = qry1.filter(Review.review_id == Reviewer_verdict.review_id).filter(Review.reviewer_1_id == Reviewer_verdict.reviewer_id)
    qry1 = qry1.filter(Review.reviewer_1_id == 2).scalar()
    print(qry1)

    qry2 = session.query(Reviewer_verdict.reviewer_verdict_id)
    qry2 = qry2.filter(Review.review_id == Reviewer_verdict.review_id).filter(Review.reviewer_2_id == Reviewer_verdict.reviewer_id)
    qry2 = qry2.filter(Review.reviewer_2_id == 3).scalar()
    print(qry2)

    rev1 = session.query(Review).filter(Review.review_id == 1).first()
    rev1.reviewer_1_verdict = qry1

    rev2 = session.query(Review).filter(Review.review_id == 1).first()
    rev2.reviewer_2_verdict = qry2

    session.commit()
    print(rev1.reviewer_1_verdict)
    print(rev2.reviewer_2_verdict)


def drop_all_tables():
    session.close()
    Base.metadata.drop_all(engine)


# drop_all_tables()

Base.metadata.create_all(engine)

# add_author()
# add_category()
#
# add_reviewer()
#
# add_publet_status()
# add_publet()
# add_reviewer_verdict_type()
# add_review()

# add_reviewer_verdict()
update_review()
