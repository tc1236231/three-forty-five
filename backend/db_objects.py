import csv
from sqlalchemy import (create_engine, Column, Integer, String, Float, text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def main():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base = declarative_base()

    class attendance(Base):
        __tablename__ = 'attendance'
        
        id = Column(Integer, primary_key=True)
        sli_no = Column(Integer) #
        paid_amt = Column(Float) #
        order_no = Column(Integer)
        price_type_desc = Column(String)
        price_type_short_desc = Column(String)
        sli_status_desc = Column(String)
        perf_dt = Column(String)
        order_dt = Column(String)
        price_type_category_desc = Column(String) #
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
            result = """<attendance(id='%d',
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
    
    Base.metadata.create_all(engine)
    
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
    
    some_rows = to_db[0:6]
    
        
    Session = sessionmaker(bind=engine)
    session = Session()
    
    for data in some_rows:  
        session.add(attendance(
                sli_no=data[0],
                paid_amt=data[1],
                order_no=data[2],
                price_type_desc=data[3],
                price_type_short_desc=data[4],
                sli_status_desc=data[5],
                perf_dt=data[6],
                order_dt=data[7],
                price_type_category_desc=data[8],
                price_type_category_short_desc=data[9],
                perf_desc=data[10],
                prod_desc=data[11],
                perf_type_desc=data[12],
                season_desc=data[13],
                season_fy=data[14],
                mos_desc=data[15],
                site_code=data[16],
                gl_account_no=data[17])    
                )
    
    test = session.query(attendance).all()
    print(sum(test.paid_amt))
    
#    session.add(attendance(sli_no=1))    
#    
#    for instance in session.query(attendance).order_by(attendance.id).filter_by(id<6):
#        print(instance.name, instance.sli_no)
#    
#    for id, in session.query(attendance.id).filter_by(text("id<6")):
#        print(id)
    
    return to_db
        
if __name__ == '__main__':
    raw_data = main()