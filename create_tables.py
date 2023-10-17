# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 14:15:13 2023

@author: joema
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base


load_dotenv()

fullstring = os.getenv('DATABASE_URL')
engine = create_engine(fullstring)

# Define the declarative base
Base = declarative_base()

#Define the Transactions class
class Transactions(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    text_id = Column(String(200), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    booking_date = Column(DateTime, nullable=False)
    description_text = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    subcategory_id = Column(Integer, ForeignKey('subcategories.subcategory_id'), nullable=True)

#Define the Banks class
class Banks(Base):
    __tablename__ = 'banks'
    bank_id = Column(Integer, primary_key=True, autoincrement=True)
    bank = Column(String(200), nullable=False)
    
#Define the Accounts class
class Accounts(Base):
    __tablename__ = 'accounts'
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(200), nullable=False)
    bank_id = Column(Integer, ForeignKey('banks.account_id'), nullable=False)
    
# Define the Category class
class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(200), nullable=False)

# Define the Subcategory class
class Subcategory(Base):
    __tablename__ = 'subcategories'
    subcategory_id = Column(Integer, primary_key=True, autoincrement=True)
    subcategory_name = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    
# Define the Budget class
class Budgets(Base):
    __tablename__ = 'budgets'
    budget_id      = Column(Integer, primary_key=True, autoincrement=True)
    subcategory_id = Column(Integer, ForeignKey('subcategories.subcategory_id'), nullable=True)
    budget_amount  = Column(Float, nullable=False)
    start_date     = Column(DateTime, nullable=False)
    end_date       = Column(DateTime, nullable=False)
    
# Define the Mapping class
class Mapping(Base):
    __tablename__ = '#mapping'
    mapping_id = Column(Integer, primary_key=True, autoincrement=True)
    description_text = Column(String(500), nullable=False)
    subcategory_id = Column(Integer, ForeignKey('subcategories.subcategory_id'), nullable=False)
    

# Create the tables in the database
Base.metadata.create_all(engine)
