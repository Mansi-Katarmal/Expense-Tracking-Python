from backend import db_helper
import pytest
from mysql.connector.errors import ProgrammingError

def test_fetch_expenses_for_date():
    data = db_helper.fetch_expenses_for_date('2024-08-31')
    assert len(data) == 1
    assert data[0]['amount'] == 100
    assert data[0]['category'] == 'Food'
    assert data[0]['notes'] == 'Gola'

def test_fetch_expenses_for_invalid_date():
    data = db_helper.fetch_expenses_for_date('2024-08-23')
    assert len(data) == 0

def test_connection():
    with db_helper.get_cursor_db() as cursor:
        cursor.execute('select count(*) counts from expenses')
        total_count = cursor.fetchall()
        assert total_count[0]['counts'] == 56
    with pytest.raises(ProgrammingError):
        cursor.execute('select 1')