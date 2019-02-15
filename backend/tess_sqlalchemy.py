from datetime import datetime as dt
from sqlalchemy import (create_engine, ForeignKey, Column, Integer, String, 
                        Numeric, DateTime, Date, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()

## Declare models    
class SubLineitem(Base):
    """
    A log of every event attendance event recorded in T_SUB_LINEITEM in the
    itura database, with appropriate transformations to fit our business
    rules.
    """    
    __tablename__ = 'sub_lineitem'
    
    id = Column(Integer, primary_key=True)
    paid_amt = Column(Numeric)
    price_type_id = Column(Integer, ForeignKey('price_types.id'))
    create_dt = Column(DateTime)
    last_update_dt = Column(DateTime)
    sli_status_id = Column(Integer, ForeignKey('sli_statuses.id'))
    perf_no = Column(Integer)
    original_price_type = Column(Integer)
    
    ## Relationships:
    sli_statuses = relationship('SLIStatuses', back_populates='sub_lineitem')
    price_types = relationship('PriceTypes', back_populates='sub_lineitem')
    
    def __repr__(self):
        return "<SubLineitem(id='%d')>" % (self.id)
        
class SLIStatuses(Base):
    __tablename__ = 'sli_statuses'
    
    id = Column(Integer, primary_key=True)
    status_desc = Column(String)
    indicates_attendance = Column(Boolean)
    
    ## Relationships:
    sub_lineitem = relationship('SubLineitem', back_populates='sli_statuses')    
    
    def __repr__(self):
        return "<SLIStatuses(id='%d', status_desc='%s')>" % (self.id, 
                                                           self.status_desc)

class PriceTypes(Base):
    __tablename__ = 'price_types'

    id = Column(Integer, primary_key=True)
    price_type_desc = Column(String)
    price_type_category = Column(Integer)
    
    ## Relationships:
    sub_lineitem = relationship('SubLineitem', back_populates='price_types')
    
    def __repr__(self):
        return "<PriceType(id='%d', price_type_desc='%s')>" % (self.id, 
                                                               self.price_type_desc)

def test__objects():
    """
    ===========================================================================
    Used to test the objects outlined above, in lieu of a formal unit testing
    procedure.
    ===========================================================================
    """    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    ## Test examples:
    session.add_all([SLIStatuses(status_desc='Seated, Paid',
                                   indicates_attendance=True),
                     SLIStatuses(status_desc='Ticketed, Paid',
                                   indicates_attendance=True)
        ])
                     
    session.commit()
    
    session.add_all([PriceTypes(price_type_desc='Adult',
                                   price_type_category=1),
                     PriceTypes(price_type_desc='Comp',
                                   price_type_category=2),
                     PriceTypes(price_type_desc='Child (Under 5)',
                                   price_type_category=1)
    ])
    
    session.add_all([SubLineitem(paid_amt=0.00,
                                 price_type_id=3,
                                 create_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 last_update_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 sli_status_id=1,
                                 perf_no=143,
                                 original_price_type=17),
                     SubLineitem(paid_amt=0.00,
                                 price_type_id=2,
                                 create_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 last_update_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 sli_status_id=1,
                                 perf_no=143,
                                 original_price_type=11),
                     SubLineitem(paid_amt=12.00,
                                 price_type_id=1,
                                 create_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 last_update_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 sli_status_id=2,
                                 perf_no=248,
                                 original_price_type=1),
                     SubLineitem(paid_amt=12.00,
                                 price_type_id=1,
                                 create_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 last_update_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 sli_status_id=2,
                                 perf_no=248,
                                 original_price_type=1),                                     
        ])
        
    session.commit()  
        
if __name__ == '__main__':
    test__objects()