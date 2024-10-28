from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///database.db')  # Replace with your actual DB connection
Session = sessionmaker(bind=engine)
session = Session()

# Opportunity Table
class Opportunity(Base):
    __tablename__ = 'opportunities'
    opportunity_id = Column(Integer, primary_key=True)
    keyword = Column(String)

# User-Opportunity mapping
class UserOpportunity(Base):
    __tablename__ = 'user_opportunities'
    user_id = Column(Integer)
    opportunity_id = Column(Integer, ForeignKey('opportunities.opportunity_id'))
    rating = Column(Integer)

Base.metadata.create_all(engine)

# Function to search for opportunities
def search_opportunities(keywords):
    opportunity_ids = []
    for keyword in keywords:
        results = session.query(Opportunity).filter_by(keyword=keyword).all()
        for result in results:
            opportunity_ids.append(result.opportunity_id)
    
    # If results are insufficient, derive new keywords and retry search
    if len(opportunity_ids) < 3:  # Example threshold
        broader_keywords = broaden_keywords(keywords)
        for keyword in broader_keywords:
            results = session.query(Opportunity).filter_by(keyword=keyword).all()
            for result in results:
                opportunity_ids.append(result.opportunity_id)
    
    return opportunity_ids

# Function to insert found opportunities into UserOpportunity table
def insert_user_opportunities(user_id, opportunity_ids):
    for opp_id in opportunity_ids:
        rating = opportunity_ids.count(opp_id)  # Calculate the rating
        user_opp = UserOpportunity(user_id=user_id, opportunity_id=opp_id, rating=rating)
        session.add(user_opp)
    session.commit()
