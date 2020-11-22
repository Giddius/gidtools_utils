import pytest
import os


def test_startup(simple_db):
    simple_db.startup_db()
    assert os.path.exists(simple_db.path) is True


def test_write_read(simple_db):
    simple_db.startup_db()
    simple_db.writer.write('INSERT INTO "main_tbl" ("name", "info") VALUES (?,?)', ("first_name", "first_info"))
    assert simple_db.reader.query('SELECT * FROM "main_tbl"') == [(1, "first_name", "first_info")]


def test_scripts(simple_db):
    simple_db.startup_db()
    simple_db.writer.write(simple_db.scripter['insert_script'], ("first_name", "first_info"))
    assert simple_db.reader.query(simple_db.scripter['query_script']) == [('first_name', 'first_info')]
    tup_list = []
    for i in range(10):
        tup_list.append((f"{str(i)}_name", f"{str(i)}_info"))
    simple_db.writer.write(simple_db.scripter['insert_script'], tup_list)
    tup_list.append(('first_name', 'first_info'))
    assert set(simple_db.reader.query(simple_db.scripter['query_script'])) == set(tup_list)
