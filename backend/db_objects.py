import csv
import datetime
from sqlalchemy import (create_engine, Column, Integer, String, Float, 
                        DateTime, Date)
from sqlalchemy.sql.expression import (func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()

## Declare models
class AttendanceReport(Base):
    """
    ===========================================================================
    An attendance count by site, ticket category, and day (as the current 
    smallest unit of measure in time that the organization can accomodate with
    the whole of our data).
    ===========================================================================
    """
    __tablename__ = 'attendance_report'
    
    id = Column(Integer, primary_key=True)
    site_code = Column(String)
    category = Column(String) # Ticket category.
    date = Column(Date)
    count = Column(Integer)
    revenue = Column(Float)
    
    def __repr__(self):
        try:
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
        except TypeError:
            result = 'No results'
        return result
    
class TessAttendance(Base):
    """
    ===========================================================================
    A log of every event attendance event recorded in T_SUB_LINEITEM in the
    Tessitura database, with appropriate transformations to fit our business
    rules.
    ===========================================================================
    """    
    __tablename__ = 'tess_attendance'
    
    id = Column(Integer, primary_key=True)
    sli_no = Column(Integer)
    paid_amt = Column(Float)
    order_no = Column(Integer)
    price_type_desc = Column(String)
    price_type_short_desc = Column(String)
    sli_status_desc = Column(String)
    perf_dt = Column(DateTime)
    order_dt = Column(DateTime)
    price_type_category_desc = Column(String)
    price_type_category_short_desc = Column(String)
    perf_desc = Column(String)
    prod_desc = Column(String)
    perf_type_desc = Column(String)
    season_desc = Column(String)
    season_fy = Column(Integer)
    mos_desc = Column(String)
    site_code = Column(String)
    gl_account_no = Column(String)
    
    def __repr__(self):
        result = """<TessAttendance(id='%d',
                                sli_no='%d',
                                paid_amt='%f', 
                                order_no='%d', 
                                price_type_desc='%s', 
                                price_type_short_desc='%s',
                                sli_status_desc='%s',
                                perf_dt='%s',
                                order_dt='%s',
                                price_type_category_desc='%s',
                                price_type_category_short_desc='%s',
                                perf_desc='%s',
                                prod_desc='%s',
                                perf_type_desc='%s',
                                season_desc='%s',
                                season_fy='%d',
                                mos_desc='%s',
                                site_code='%s',
                                gl_account_no='%s')>""" % (self.id,
                                                           self.sli_no,
                                                           self.paid_amt, 
                                                           self.order_no, 
                                                           self.price_type_desc, 
                                                           self.price_type_short_desc,
                                                           self.sli_status_desc,
                                                           self.perf_dt,
                                                           self.order_dt,
                                                           self.price_type_category_desc,
                                                           self.price_type_category_short_desc,
                                                           self.perf_desc,
                                                           self.prod_desc,
                                                           self.perf_type_desc,
                                                           self.season_desc,
                                                           self.season_fy,
                                                           self.mos_desc,
                                                           self.site_code, 
                                                           self.gl_account_no)
        return result
    
    @classmethod
    def daily_attendance_report(cls, session, date):
        """
        =======================================================================
        Return an attendance report for a given day. 
        =======================================================================
        """
        try: ## BI-54: Update this so it can handle date inputs better.
            date_obj = datetime.datetime.strptime(date, '%m/%d/%Y')
        except ValueError:
            print('Improperly formatted date, date must be MM/DD/YYYY')
            return
        else:
            date_param = date_obj.strftime('%Y-%m-%d')
        result = (
                session
                .query(cls.site_code,
                       cls.perf_dt,                           
                       cls.price_type_category_desc,
                       func.count(cls.sli_no),
                       func.sum(cls.paid_amt))
                .filter(func.date(cls.perf_dt) == date_param)
                .group_by(cls.site_code, 
                          func.date(cls.perf_dt),
                          cls.price_type_category_desc)
                .all()
                )
        return [
                AttendanceReport(
                        site_code=site_code,
                        category=category,
                        date=date,
                        count=count,
                        revenue=total)
                for site_code, date, category, count, total in result
                ]

def test_db_objects():
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
    
    # Load the static dataset for testing.
    with open('tess_orders.csv', 'r') as o:
        dr = csv.DictReader(o)
        to_db = [(i['sli_no'],
                  i['paid_amt'],
                  i['order_no'],
                  i['price_type_desc'],
                  i['price_type_short_desc'],
                  i['sli_status_desc'],
                  i['perf_dt'],
                  i['order_dt'],
                  i['price_type_category_desc'],
                  i['price_type_category_short_desc'],
                  i['perf_desc'],
                  i['prod_desc'],
                  i['perf_type_desc'],
                  i['season_desc'],
                  i['season_fy'],
                  i['mos_desc'],
                  i['site_code'],
                  i['gl_account_no']) for i in dr]
    
    # Get only the first 100 rows, for the sake of speed.
    some_rows = to_db[0:100]
    
    # Add 100 rows to TessAttendance.
    for data in some_rows:
        session.add(TessAttendance(sli_no=data[0],
                               paid_amt=data[1],
                               order_no=data[2],
                               price_type_desc=data[3],
                               price_type_short_desc=data[4],
                               sli_status_desc=data[5],
                               perf_dt=datetime.datetime.strptime(data[6],
                                    '%m/%d/%Y %H:%M'),
                               order_dt=datetime.datetime.strptime(data[7],
                                    '%m/%d/%Y %H:%M'),
                               price_type_category_desc=data[8],
                               price_type_category_short_desc=data[9],
                               perf_desc=data[10],
                               prod_desc=data[11],
                               perf_type_desc=data[12],
                               season_desc=data[13],
                               season_fy=data[14],
                               mos_desc=data[15],
                               site_code=data[16],
                               gl_account_no=data[17]
                               )    
        )   
    
    session.commit()

    ## Test daily_attendance_report against a picked day.
    session.add_all(TessAttendance.daily_attendance_report(session, 
                                                           '3/19/2016'))
    
    session.commit()
    
    results = session.query(AttendanceReport).all()
    
    ## Check the results of TessAttendance.daily_attendance_report for 3/19/2016.
    ## There should be 3 row results (1 for each price type on that day), with
    ## the following breakdown of count and revenue:
    expected_agg_result = [[2, 0.0], [3, 12.0], [46, 276.0]]
    
    ## Compare expectation with results:
    test_result = [False, False, False]
    
    for i, agg_result in enumerate(expected_agg_result):
        if (expected_agg_result[i][0] == results[i].count and
            expected_agg_result[i][1] == results[i].revenue):
                test_result[i] = True
                
    return test_result
        
    
if __name__ == '__main__':
    print(test_db_objects())

