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
    
class ArtifaxAttendance(Base):
    """
    ===========================================================================
    A log of every daily attendance event in Artifax. 
    This model should be reconfigured for BI-51 to ensure that it actually
    expects the output that Artifax spits out.
    ===========================================================================
    """    
    __tablename__ = 'artifax_attendance'
    
    id = Column(Integer, primary_key=True)
    revenue = Column(Float)
    attendance = Column(Integer)
    price_type_desc = Column(String)
    attendance_dt = Column(DateTime)
    price_type_category_desc = Column(String)
    program_attended = Column(String)
    perf_type_desc = Column(String) ## Presumably GA or Program?
    season_fy = Column(Integer)
    site_code = Column(String)
    
    def __repr__(self):
        result = """<ArtifaxAttendance(id='%d',
                                revenue='%f', 
                                attendance='%d',
                                price_type_desc='%s', 
                                attendance_dt='%s',
                                price_type_category_desc='%s',
                                program_attended='%s',
                                perf_type_desc='%s',
                                season_fy='%d',
                                site_code='%s')>""" % (self.id,
                                                           self.revenue, 
                                                           self.attendance,
                                                           self.price_type_desc, 
                                                           self.attendance_dt,
                                                           self.price_type_category_desc,
                                                           self.program_attended,
                                                           self.perf_type_desc,
                                                           self.season_fy,
                                                           self.site_code)
        return result
    
    @classmethod
    def import_csv(cls, session, file_name):
        """
        =======================================================================
        Imports a properly formatted csv file into ArtifaxAttendance.
        
        Currently this is configured to match the artifax_orders100.csv in this
        feature branch. It will need to be re-jiggered once we know what 
        the Artifax CSV files are going to look like going forward.
        =======================================================================
        """        

        with open(file_name, 'r') as o:
            dr = csv.DictReader(o)
            to_db = [(i['revenue'],
                      i['attendance'],
                      i['price_type_desc'],
                      i['attendance_dt'],
                      i['price_type_category_desc'],
                      i['program_attended'],
                      i['perf_type_desc'],
                      i['season_fy'],
                      i['site_code']) for i in dr]

        for data in to_db:
            session.add(ArtifaxAttendance(revenue=data[0],
                                   attendance=data[1],
                                   price_type_desc=data[2],
                                   attendance_dt=datetime.datetime.strptime(data[3],
                                        '%m/%d/%Y'),
                                   price_type_category_desc=data[4],
                                   program_attended=data[5],
                                   perf_type_desc=data[6],
                                   season_fy=data[7],
                                   site_code=data[8],
                                   )    
            )   

        session.commit()
    
    @classmethod
    def daily_attendance_report(cls, session, date):
        """
        =======================================================================
        Return an attendance report for a given day. 
        =======================================================================
        """
        ## BI-54: Update this so it can handle date inputs better.
        date_obj = datetime.datetime.strptime(date, '%m/%d/%Y')

        date_param = date_obj.strftime('%Y-%m-%d')
        result = (
                session
                .query(cls.site_code,
                       cls.attendance_dt,                           
                       cls.price_type_category_desc,
                       func.sum(cls.attendance),
                       func.sum(cls.revenue))
                .filter(func.date(cls.attendance_dt) == date_param)
                .group_by(cls.site_code, 
                          func.date(cls.attendance_dt),
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

def test_artifax_objects():
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
    ArtifaxAttendance.import_csv(session, 'artifax_orders100.csv')

    ## Test daily_attendance_report against a picked day.
    session.add_all(ArtifaxAttendance.daily_attendance_report(session, 
                                                           '4/21/2016'))
    
    session.commit()
    
    results = session.query(AttendanceReport).all()
    
    ## Check the results of ArtifaxAttendance.daily_attendance_report for 4/21/2016.
    ## There should be 2 row results (1 for each price type on that day), with
    ## the following breakdown of count and revenue:
    expected_agg_result = [[11, 0.0], [28, 244.0]]
    
    ## Compare expectation with results:
    test_result = [False, False]
    
    for i, agg_result in enumerate(expected_agg_result):
        if (expected_agg_result[i][0] == results[i].count and
            expected_agg_result[i][1] == results[i].revenue):
                test_result[i] = True
                
    return test_result
        
    
if __name__ == '__main__':
    print(test_artifax_objects())

