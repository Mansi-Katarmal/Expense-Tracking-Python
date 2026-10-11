from pydantic import BaseModel
from fastapi import FastAPI,HTTPException
from datetime import date
import db_helper
from typing import List

app = FastAPI()

class Expense(BaseModel):
    amount : int
    category : str
    notes : str

class DateRange(BaseModel):
    start_date : date
    end_date : date


@app.get('/expenses/{expense_date}',response_model=List[Expense])
def get_expenses(expense_date : date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500,details = 'Data Fetch Failed')
    return expenses



@app.post('/expenses/{expense_date}')
def update_or_insert_expense_for_date(expense_date : date, expenses : List[Expense]):
    db_helper.delete_expense_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date,expense.amount,expense.category,expense.notes)
    return {'message':'Expense inserted'}

@app.post('/analytics_by_category/')
def get_analytics(dateRange : DateRange):
    summary = db_helper.expense_summary(dateRange.start_date,dateRange.end_date)
    if summary is None:
        raise HTTPException(status_code=500,details = 'Data Fetch Failed')
    total_expense = sum([record['total_amount'] for record in summary])
    final_response = {}
    for record in summary:
        percentage = (record['total_amount']/total_expense) * 100 if total_expense != 0 else 0
        final_response[record['category']] = {
            'total' : record['total_amount'],
            'percentage' : round(percentage,2)
        }
    return final_response

@app.get('/analytics_by_month/')
def get_monthly_analytics():
    monthly_summary = db_helper.monthly_expense_summary()
    if monthly_summary is None:
        raise HTTPException(status_code=500,detail='Data Fetch Failed')
    # monthly_summary_breakdown = {rec['month_name'] : rec['monthly_expense'] for rec in monthly_summary}
    return monthly_summary
# _breakdown
    