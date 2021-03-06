import csv
import os
import random
import time
from random import randint

from django.core.files import File
from django.core.files.base import ContentFile

from fake_csv.settings import MEDIA_ROOT
from common.dict.dicts import CeleryStatusTypeDict
from common.models import SchemeColumns, DataSet


def generate_csv_for_schema(obj_id):
    """ Function for create or update schemas """
    try:
        data_set = DataSet.objects.get(id=obj_id)
        schema = data_set.schemas
        file_path_ = f"{MEDIA_ROOT}/file_{data_set.id}.csv"
        with open(file_path_, 'w+', newline="") as csv_file:
            file_writer = csv.writer(csv_file, delimiter=schema.col_separator.value,
                                     quotechar=schema.col_string_char.value, quoting=csv.QUOTE_MINIMAL)
            columns = SchemeColumns.objects.filter(schemas=schema)
            file_writer.writerow(columns.values_list('name', flat=True))
            for row in range(data_set.rows):
                file_writer.writerow([generate_random_value(col) for col in columns])
        with open(file_path_, "rb") as f:
            data_set.file.save(f"file_{data_set.id}.csv", ContentFile(f.read()))
        data_set.status = CeleryStatusTypeDict.objects.get(code='ready')
        data_set.save()
        os.remove(file_path_)
    except (DataSet.DoesNotExist, CeleryStatusTypeDict.DoesNotExist, Exception) as e:
        return False
    return True


def generate_random_value(obj_col: SchemeColumns):
    """ Generate random value """
    if obj_col.type.code == 'integer':
        if obj_col.input_from and obj_col.input_to:
            result = randint(obj_col.input_from, obj_col.input_to)
        else:
            result = randint(0, 10000)
    elif obj_col.type.code == 'date':
        result = random_date("2000-01-01", "2021-01-01", random.random())
    elif obj_col.type.code == 'email':
        result = get_random_text() + '@gmail.com'
    elif obj_col.type.code == 'company':
        result = get_random_text(5)
    elif obj_col.type.code == 'full_name':
        result = f"{get_random_text(5)} {get_random_text(7)}"
    return result


def get_random_text(count=10):
    """ Get random text """
    result = str()
    for char in range(count):
        result += random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
    return result


def random_date(start, end, prop, format='%Y-%m-%d'):
    """ Function random generate date """
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))
