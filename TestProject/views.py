from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseGone
import operator
import logging
import json
import csv
import os

current_dir = os.getcwd()
database_dir = os.path.join(current_dir, 'TestProject\Databases\\base.csv')

# HTML input names
getID = 'getID'
deleteID = 'deleteID'
page = 'page'
limit = 'limit'


def index(request):
    return render(request, 'index.html')


# Вывод определённого количества записей
def show(request):
    database_list = _get_database(database_dir)
    pageLimit = request.GET['page']
    limit = request.GET['limit']
    row_limit = len(database_list)
    if limit != '':
        row_limit = int(limit)

    database_list.sort(key=operator.itemgetter('Station'))
    database_json = json.dumps({'data': database_list[:row_limit]})
    _log('SHOW', f'Shown {row_limit} rows', '', f'{request.environ["HTTP_HOST"]}/?{request.environ["QUERY_STRING"]}')
    return HttpResponse(database_json)


# Обработка добавления записи
def add(request):
    database_list = _get_database(database_dir)
    database_list.append({
        'Station': request.POST['station'],
        'Line': request.POST['line'],
        'AdmArea': request.POST['admArea'],
        'District': request.POST['district'],
        'Status': request.POST['status'],
        'ID': str(int(database_list[-1]['ID']) + 1)
    })
    _rewrite_database_file(database_dir, database_list)
    _log('ADD', 'Added new row to database', '',
         f'{request.environ["HTTP_HOST"]}/?{request.environ["QUERY_STRING"]}')
    return HttpResponse(json.dumps(database_list[-1]))


def get_delete(request):
    database_list = _get_database(database_dir)

    # Обработка получения записи по ID
    if getID in request.GET:
        row = _find_row_by_id(request, database_list, getID)
        json_row = json.dumps(row)
        _log('GET', 'Got row from database', '', f'{request.environ["HTTP_HOST"]}/?{request.environ["QUERY_STRING"]}')
        return HttpResponse(json_row)

    # Обработка удаления записи по ID
    elif deleteID in request.GET:
        row = _find_row_by_id(request, database_list, deleteID)
        if row is None:
            _log('DELETE', '"ID" not found', '404', f'{request.environ["HTTP_HOST"]}/?{request.environ["QUERY_STRING"]}')
            return HttpResponseNotFound()
        else:
            database_list.remove(row)
            _rewrite_database_file(database_dir, database_list)
            _log('DELETE', f'Deleted row with id={row["ID"]}', '', f'{request.environ["HTTP_HOST"]}/?{request.environ["QUERY_STRING"]}')
            return HttpResponse(f"Row {row} deleted!", status=200)


def _log(service, message, error, endpoint):
    logger = logging.getLogger(__name__)
    log_message = {'service': service, 'message': message, 'error': error, 'endpoint': endpoint}
    logger.error(log_message)


def _rewrite_database_file(filename, database):
    with open(filename, "w", newline='') as file:
        fieldnames = database[0].keys()
        writer = csv.DictWriter(file, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        for row in database:
            writer.writerow(row)


def _get_database(directory_name):
    headers = ''
    database = []
    with open(directory_name, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            database.append(row)
    return database


def _find_row_by_id(request, database, rowid):
    for row in database:
        if row['ID'] == request.GET[rowid]:
            return row
