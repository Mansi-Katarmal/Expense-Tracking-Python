import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_cursor_db(commit = False):
    connection = mysql.connector.connect(host = "localhost",
        user = "root",
        password = "root",
        database = "expense_manager")
      
    try:
        cursor = connection.cursor(dictionary=True)
        logger.info('Connection Opened')
        yield cursor
        if commit:
            connection.commit()
    finally:
        cursor.close()
        connection.close()
        logger.info('Connection Closed')


def fetch_expenses_for_date(expense_date):
    logger.info(f'Executed fetch_expenses_for_date {expense_date}')
    with get_cursor_db() as cursor:
        cursor.execute('SELECT * FROM expense_manager.expenses where expense_date = %s',(expense_date,))
        data = cursor.fetchall()
        return data

def insert_expense(expense_date, amount, category, notes):
    logger.info(f'Executed insert_expense({expense_date}, {amount},{category},{ notes})')
    query = ''' 
    insert into expense_manager.expenses (expense_date, amount, category, notes) values ( %s, %s, %s, %s)
    '''
    params = (expense_date, amount, category, notes)
    with get_cursor_db(commit=True) as cursor:
        cursor.execute(query,params)
        

def delete_expense_for_date(expense_date):
    logger.info(f'Executed delete_expense_for_date({expense_date})')
    query = '''
    delete from expense_manager.expenses where expense_date = %s
    '''
    params = (expense_date,)
    with get_cursor_db(commit=True) as cursor:
        cursor.execute(query,params)
        

def expense_summary(start_date,end_date):
    logger.info(f'Executed expense_summary({start_date},{end_date})')
    query = '''
    SELECT category,sum(amount) total_amount FROM expense_manager.expenses 
    where expense_date between %s and %s
    group by category
    '''
    params = (start_date,end_date)

    with get_cursor_db() as cursor :
        cursor.execute(query,params)
        summary = cursor.fetchall()
        

    return summary

def total_records():
    with get_cursor_db() as cursor:
        cursor.execute('select count(*) total_records from expenses')
        total_count = cursor.fetchall()
        return total_count

def monthly_expense_summary():
    logger.info(f'Executed monthly_expense_summary()')
    with get_cursor_db() as cursor:
        cursor.execute('select month(expense_date) month_number, ' \
        'monthname(expense_date) month_name,sum(amount) monthly_expense from ' \
        'expenses group by month(expense_date), monthname(expense_date)')
        monthly_summary = cursor.fetchall()
        return monthly_summary


if __name__ == "__main__":
    # data = fetch_expenses_for_date('2024-08-24')
    # for record in data:
    #     print(record)
    # insert_expense('2024-08-15',1500,'Entertainment','Games')
    # print('Before delete')
    # data = fetch_expenses_for_date('2024-08-15')
    # for record in data:
    #     print(record)
    # delete_expense_for_date('2024-08-15')
    # print('After Delete')
    # data = fetch_expenses_for_date('2024-08-15')
    # for record in data:
    #     print(record)

    # data = expense_summary('2024-08-01','2024-08-05')
    # print(data)
    # for record in data:
    #     print(record)
    # data = total_records()
    # print(data[0]['total_records'])
    print(monthly_expense_summary())