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
    perf_no = Column(Integer, ForeignKey('perf.id'))
    original_price_type_id = Column(Integer)
    
    ## Relationships:
    sli_statuses = relationship('SLIStatuses', back_populates='sub_lineitem')
    price_types = relationship('PriceTypes', 
                               back_populates='sub_lineitem')
    perf = relationship('Perf', 
                        back_populates='sub_lineitem')
    
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
        
class Inventory(Base):
    """
    Inventory holds all the perf, production, and production_season ids and
    their corresponding names. All three of those tables/classes must have an
    id in inventory.
    """
    __tablename__ = 'inventory'
    
    ## id must be included in imports of T_INVENTORY because it is not a 
    ## contiguous value in Tessitura. It maps to inv_no.
    id = Column(Integer, primary_key=True)
    inv_desc = Column(String)
    ## For inv_type: R = Performance, S = Prod Season, P = Production, T = Title
    inv_type = Column(String) 
    
    ## Relationships:
    perf = relationship('Perf', back_populates='inventory')
    prod_season = relationship('ProductionSeason', back_populates='inventory')
    production = relationship('Production', back_populates='inventory')
    
    def __repr__(self):
        return "<Inventory(id='%d')>" % (self.id)
    
class Perf(Base):
    __tablename__ = 'perf'
    
    ## id must be included in imports of T_PERF beacuse it is not a 
    ## contiguous value in Tessitura. It maps to perf_no.
    id = Column(Integer, ForeignKey('inventory.id'), primary_key=True) 
    prod_season_id = Column(Integer, ForeignKey('prod_season.id'))
    perf_dt = Column(DateTime)
    perf_type = Column(Integer, ForeignKey('perf_types.id'))
    
    ## Relationships:
    sub_lineitem = relationship('SubLineitem', back_populates='perf')
    inventory = relationship('Inventory', back_populates='perf')
    prod_season = relationship('ProductionSeason', back_populates='perf')
    perf_types = relationship('PerfTypes', back_populates='perf')
    
    def __repr__(self):
        return "<Perf(id='%d')>" % (self.id)    
    
class PerfTypes(Base):
    __tablename__ = 'perf_types'
    
    id = Column(Integer, primary_key=True)
    perf_type_desc = Column(String)
    
    ## Relationships
    perf = relationship('Perf', back_populates='perf_types')
    
    def __repr__(self):
        return "<PerfType(id='%d', perf_type_desc='%s')>" % (self.id, 
                         self.perf_type_desc)      
    
class ProductionSeason(Base):
    __tablename__ = 'prod_season'
    
    ## id must be included in imports of T_PROD_SEASON beacuse it is not a 
    ## contiguous value in Tessitura. It maps to prod_season_no.    
    id = Column(Integer, ForeignKey('inventory.id'), primary_key=True)
    production_id = Column(Integer, ForeignKey('production.id'))
    
    ## Relationships:
    inventory = relationship('Inventory', back_populates='prod_season')
    perf = relationship('Perf', back_populates='prod_season')
    production = relationship('Production', back_populates='prod_season')
    
    def __repr__(self):
        return "<ProductionSeason(id='%d', prod_season_id='%d')>" % (self.id,
                                 self.prod_season_id)    
    
"""
Not sure if this class is wholly necessary, since all we really need to know is 
the production_id so that we can get the name of the production from 
T_INVENTORY so that we can apply category mapping rules.
"""
class Production(Base):
    __tablename__ = 'production'
    
    ## id must be included in imports of T_PRODUCTION beacuse it is not a 
    ## contiguous value in Tessitura. It maps to prod_no.    
    id = Column(Integer, ForeignKey('inventory.id'), primary_key=True)
    
    ## Relationships:
    inventory = relationship('Inventory', back_populates='production')
    prod_season = relationship('ProductionSeason', back_populates='production')
    
    def __repr__(self):
        return "<Production(id='%d')>" % (self.id)        
        

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
                     
    session.add_all([Inventory(id=143,
                               inv_desc='MHC Admissions FY16',
                               inv_type='R'),
                     Inventory(id=248,
                               inv_desc='MCM Daily Admissions',
                               inv_type='R'),
                    ])
    
    session.add_all([SubLineitem(paid_amt=0.00,
                                 price_type_id=3,
                                 create_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 last_update_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 sli_status_id=1,
                                 perf_no=143,
                                 original_price_type_id=3),
                     SubLineitem(paid_amt=0.00,
                                 price_type_id=2,
                                 create_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 last_update_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 sli_status_id=1,
                                 perf_no=143,
                                 original_price_type_id=2),
                     SubLineitem(paid_amt=12.00,
                                 price_type_id=1,
                                 create_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 last_update_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 sli_status_id=2,
                                 perf_no=248,
                                 original_price_type_id=1),
                     SubLineitem(paid_amt=12.00,
                                 price_type_id=1,
                                 create_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 last_update_dt=dt.strptime('2016-03-10 15:16', '%Y-%m-%d %H:%M'),
                                 sli_status_id=2,
                                 perf_no=248,
                                 original_price_type_id=1),                                     
        ])
        
    session.commit()  
        
if __name__ == '__main__':
    test__objects()