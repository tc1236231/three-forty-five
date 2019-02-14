from datetime import datetime as dt
from sqlalchemy import (create_engine, ForeignKey, Column, Integer, String, 
                        Numeric, DateTime, Date, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()

## Declare models
class AttendanceReport(Base):
    """
    An attendance count by site, ticket category, and day (as the current 
    smallest unit of measure in time that the organization can accomodate with
    the whole of our data).
    """
    __tablename__ = 'attendance_report'
    
    id = Column(Integer, primary_key=True)
    site_code = Column(String)
    category = Column(String) # Ticket category.
    date = Column(Date)
    count = Column(Integer)
    revenue = Column(Numeric)
    
    def __repr__(self):
        result = """<AttendanceReport(id='%d', 
                                    site_code='%s', 
                                    category='%s',
                                    date='%s',
                                    count='%d',
                                    revenue='%f')>""" % (self.id,
                                                         self.site_code,
                                                         self.category,
                                                         self.date,
                                                         self.count,
                                                         self.revenue)
        return result
    
class TessSubLineitem(Base):
    """
    A log of every event attendance event recorded in T_SUB_LINEITEM in the
    Tessitura database, with appropriate transformations to fit our business
    rules.
    """    
    __tablename__ = 'tess_sub_lineitem'
    
    id = Column(Integer, primary_key=True)
    sli_no = Column(Integer)
    paid_amt = Column(Numeric)
    price_type = Column(Integer, ForeignKey('tess_price_type.id'))
    create_dt = Column(DateTime)
    last_update_dt = Column(DateTime)
    sli_status = Column(Integer, ForeignKey('tess_sli_status.id'))
    perf_no = Column(Integer)
    order_no = Column(Integer)
    original_price_type = Column(Integer)
    
    ## Relationships:
    sli_status_ref = relationship('TessSLIStatus', backref='tess_sli_status')
    price_type_ref = relationship('TessPriceType', backref='tess_price_type')
    
    def __repr__(self):
        result = "<TessSubLineitem(id='%d', sli_no='%d')>" % (self.id, 
                                                              self.sli_no)
        return result
        
class TessSLIStatus(Base):
    __tablename__ = 'tess_sli_status'
    
    id = Column(Integer, primary_key=True)
    status_desc = Column(String)
    indicates_attendance = Column(Boolean)
    
    def __repr__(self):
        result = "<TessSLIStatus(id='%d', status_desc='%s')>" % (self.id, 
                                                                  self.status_desc)
        return result

class TessPriceType(Base):
    __tablename__ = 'tess_price_type'

    id = Column(Integer, primary_key=True)
    price_type_desc = Column(String)
    price_type_category = Column(Integer)
    
    def __repr__(self):
        result = "<TessPriceType(id='%d', price_type_desc='%s')>" % (self.id, 
                                                          self.price_type_desc)
        return result

def test_tess_objects():
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
    session.add_all([TessSLIStatus(status_desc='Seated, Paid',
                                   indicates_attendance=True),
                     TessSLIStatus(status_desc='Ticketed, Paid',
                                   indicates_attendance=True)
        ])
                     
    session.commit()
    
    session.add_all([TessPriceType(price_type_desc='Adult',
                                   price_type_category=1),
                     TessPriceType(price_type_desc='Comp',
                                   price_type_category=2),
                     TessPriceType(price_type_desc='Child (Under 5)',
                                   price_type_category=1)
    ])
    
    session.add_all([TessSubLineitem(sli_no=3109,
                                     paid_amt=0.00,
                                     price_type=3,
                                     create_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                     last_update_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                     sli_status=1,
                                     perf_no=143,
                                     order_no=473819,
                                     original_price_type=17),
                     TessSubLineitem(sli_no=3110,
                                     paid_amt=0.00,
                                     price_type=2,
                                     create_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                     last_update_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                     sli_status=1,
                                     perf_no=143,
                                     order_no=473820,
                                     original_price_type=11),
                     TessSubLineitem(sli_no=3111,
                                     paid_amt=12.00,
                                     price_type=1,
                                     create_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                     last_update_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                     sli_status=2,
                                     perf_no=248,
                                     order_no=473823,
                                     original_price_type=1),
                     TessSubLineitem(sli_no=3112,
                                     paid_amt=12.00,
                                     price_type=1,
                                     create_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                     last_update_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                     sli_status=2,
                                     perf_no=248,
                                     order_no=473823,
                                     original_price_type=1),                                     
        ])
        
    session.commit()  
        
if __name__ == '__main__':
    test_tess_objects()