import csv
from sqlalchemy import (create_engine, Column, Integer, String, Float, text)
from sqlalchemy.sql.expression import (func, select)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()

class attendance(Base):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True)
    sli_no = Column(Integer)
    paid_amt = Column(Float)
    order_no = Column(Integer)
    price_type_desc = Column(String)
    price_type_short_desc = Column(String)
    sli_status_desc = Column(String)
    perf_dt = Column(String)
    order_dt = Column(String)
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

class att_aggregate(Base):
    __tablename__ = 'att_aggregate'
    
    id = Column(Integer, primary_key=True)
    group_on = Column(String)
    ticket_ct = Column(Integer)
    revenue = Column(Float)
    
    def __repr__(self):
        return "<att_aggregate(id='%d', group_on='%s', ticket_ct='%d', revenue='%f')>" % (
                self.id, self.group_on, self.ticket_ct, self.revenue)
        
    def cat_price_aggregate(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        connection = engine.connect()
    
        query = select([attendance.perf_type_desc,
                        attendance.price_type_desc,
                        func.count(attendance.sli_no), 
                        func.sum(attendance.paid_amt)]
                        ).group_by('perf_type_desc','price_type_desc')
        
        results = connection.execute(query)
        
        for result in results:
            group_on_str = ''
            for group_val in result[:-2]:
                group_on_str = group_on_str + str(group_val) + '&'
            group_on_str = group_on_str[:-1]
            row = att_aggregate(group_on=group_on_str, ticket_ct=result[-2], revenue=result[-1])
            session.add(row)
            
        session.commit()

Base.metadata.create_all(engine)

def main():
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
    
    some_rows = to_db[0:12]
    
        
    Session = sessionmaker(bind=engine)
    session = Session()
    
    for data in some_rows:  
        session.add(attendance(sli_no=data[0],
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
                               gl_account_no=data[17]
                               )    
        )   
    
    session.commit()
    
    test = att_aggregate()
    test.cat_price_aggregate()
    
    print(session.query(select([att_aggregate.group_on, att_aggregate.ticket_ct, att_aggregate.revenue])).all())
        
    #session.query().all()
    
#    session.add(attendance(sli_no=1))    
#    
#    for instance in session.query(attendance).order_by(attendance.id).filter_by(id<6):
#        print(instance.name, instance.sli_no)
#    
#    for id, in session.query(attendance.id).filter_by(text("id<6")):
#        print(id)
    
    return to_db, some_rows
        
if __name__ == '__main__':
    raw_data, raw_rows = main()