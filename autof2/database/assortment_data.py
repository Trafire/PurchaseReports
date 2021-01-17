from sqlalchemy.orm import sessionmaker
from autof2.database.model import engine, F2Category, F2Assortment


def get_session():
    session = sessionmaker(bind=engine)
    return session()


def get_f2_code(category, product, grade, colour,packing):
    session = get_session()
    category = session.query(F2Category).filter_by(f2_category_description=category).first()
    return session.query(F2Assortment).filter_by(f2_name=product,
                                                 f2_category=category,
                                                 packing=packing,
                                                 f2_grade=grade,
                                                 f2_colour_code_id=colour).first()

def get_f2_code_no_colour(category, product, grade,packing):
    session = get_session()
    category = session.query(F2Category).filter_by(f2_category_description=category).first()
    return session.query(F2Assortment).filter_by(f2_name=product,
                                                 f2_category=category,
                                                 packing=packing,
                                                 f2_grade=grade
                                                ).first()


def one_session_get_f2_code(session,category, product, grade, colour,packing):
    category = session.query(F2Category).filter_by(f2_category_description=category).first()
    return session.query(F2Assortment).filter_by(f2_name=product,
                                                 f2_category=category,
                                                 packing=packing,
                                                 f2_grade=grade,
                                                 f2_colour_code_id=colour).first()

def one_session_get_f2_code_no_colour(session,category, product, grade, packing):
    category = session.query(F2Category).filter_by(f2_category_description=category).first()
    return session.query(F2Assortment).filter_by(f2_name=product,
                                                 f2_category=category,
                                                 packing=packing,
                                                 f2_grade=grade).first()


