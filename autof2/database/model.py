from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String,Numeric,DECIMAL
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
'''
class PurchaseHistory(Base):

    __tablename__ = 'purchase_history'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    supplier =  Column(String(6))
    f2_code =  Column(String(10))
    description =  Column(String(50))
    units_sold =  Column(Integer)
    buying_price = Column(Numeric)
    #selling_price = Column(Numeric)
    week =  Column(Integer)
    year =  Column(Integer)
    def __str__(self):
        return f"{self.description} {self.year} - {self.week} x {self.units_sold} "
'''
class Client(Base):
    __tablename__ = 'clients'
    id = Column(String(6), primary_key=True)
    name = Column(String(64))
    address = Column(String(64))
    postal_code = Column(String(64))
    city = Column(String(64))
    salesperson = Column(String(64))

class F2Category(Base):
    __tablename__ = 'sales_f2category'
    f2_category_num = Column(Integer, primary_key=True)
    f2_category_description =  Column(String(255))

    def __str__(self):
        return f"{self.f2_category_description}"
    def __meta__(self):
        ordering= ["f2_category_description","f2_category_num" ]

class F2Assortment(Base):
    __tablename__ = 'sales_f2assortment'
    f2_code = Column(String(10,collation='utf8_bin'), primary_key=True)
    f2_category_id = Column(Integer,ForeignKey(F2Category.f2_category_num))
    f2_category = relationship("F2Category")
    f2_name = Column(String(64))
    f2_grade = Column(String(3))
    f2_colour_code_id = Column(String(3))
    packing = Column(Integer)

    def __str__(self):
        return f"{self.f2_category} {self.f2_code} {self.f2_name} x {self.packing}"
    def __meta__(self):
        ordering= ["f2_category","f2_name" ]


class PurchaseHistoryDays(Base):

    __tablename__ = 'purchase_history'
    id = Column(Integer, primary_key=True)
    client = Column(String(6,collation='utf8_bin'),ForeignKey(Client.id))
    quantity = Column(Integer)
    supplier =  Column(String(6))
    f2_code_id = Column(String(10, collation='utf8_bin'), ForeignKey(F2Assortment.f2_code))
    #f2_code = relationship("F2Assortment", back_populates="f2assortment")
    description =  Column(String(50))
    buying_price = Column(DECIMAL(10,2))
    selling_price = Column(DECIMAL(10,2))
    date =  Column(Date)
    def __str__(self):
        return f"{self.description} {self.date}"

class ClientSales(Base):
    __tablename__ = 'client_sales'
    id = Column(Integer, primary_key=True)
    client = Column(String(6, collation='utf8_bin'), ForeignKey(Client.id))
    buying_price = Column(DECIMAL(10,2))
    advised_price = Column(DECIMAL(10,2))
    invoice_total = Column(DECIMAL(10,2))
    date = Column(Date)




engine = create_engine('mysql+pymysql://po_antoine:$pl4nt3n@mysql.fleurametztoronto.com/fm_app',echo=False, case_sensitive=True)
Base.metadata.create_all(engine)