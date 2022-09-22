import json
import os

import csv
from extra_field import ExtraFieldData, ExtraFieldValue, ExtraField
from warehouses_checker import extract_wh

# def get_inserts():

current_path = os.path.dirname(os.path.realpath(__file__))


def get_wh_id_and_extra_fields_id_from_csv() -> dict[str, list[str]]:
    key_extra_field_id: str = 'id'
    key_warehouse_id: str = 'warehouse_id'

    warehouse_id: str
    extra_field_ids_to_init: list[str] = []
    with open(current_path + '/csv/extra_fields.csv', mode='r', encoding='UTF8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            extract_wh(row)
            ef_id = row.get(key_extra_field_id)
            warehouse_id = row.get(key_warehouse_id)
            if not ef_id:
                raise AttributeError("extra_field (id) not found")
            extra_field_ids_to_init.append(ef_id)

    return {'warehouse_id': warehouse_id, 'extra_fields_ids': extra_field_ids_to_init}


def get_all_extra_fields() -> list[ExtraFieldData]:
    with open(current_path + '/json_data/extra_fields.json', mode='r', encoding='UTF8') as json_file:
        extra_fields = list(map(lambda ef: ExtraFieldData(**ef), json.load(json_file)))
        # extra_fields = json.load(json_file, object_hook=lambda arr: map(lambda ef: ExtraFieldData(**ef), arr))
        return extra_fields


def covertToSQL(filename: str, column, suffix):
    result = ''
    with open(filename, mode='r', encoding='UTF8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                result += f'INSERT INTO {column}\n\t({", ".join(row)})\n VALUES\n'
                line_count += 1
            line = '\t('
            values = list(row.values())
            for i, value in enumerate(values):
                if not value.isnumeric():
                    line += f"'{value}'"
                else:
                    line += f"{value}"
                if i != len(values) - 1:
                    line += ','
            line += '),'
            result += f"{line} \n"
        result = ''.join(result.rsplit(',', 1))
        result += f"{suffix}\n\n"
        # print(f'{result}')


def get_extra_field_id_insert_request(extrafield_ids: list[str]) -> str:
    request = 'INSERT INTO pickingwavebox.extra_field_id (id) \nVALUES'
    request += ", ".join(list(map(lambda x: f"\n\t('{x}')", extrafield_ids)))
    request += "\nON CONFLICT DO NOTHING;\n"
    return request


def get_extra_field_values_insert_request(extrafield_values: list[ExtraFieldValue]) -> str:
    request = 'INSERT INTO pickingwavebox.extra_field_values (extra_field_id, field_value, order_value) \nVALUES'
    request += ", ".join(list(map(lambda x: f"\n\t('{x.id}','{x.value}','{x.order}')", extrafield_values)))
    request += "\nON CONFLICT DO NOTHING;\n"
    return request


def get_extra_field_insert_request(extrafield_values: list[ExtraField]) -> str:
    request = 'INSERT INTO pickingwavebox.extra_fields(extra_field_id, default_value, warehouse_id) \nVALUES'
    request += ", ".join(
        list(map(lambda x: f"\n\t('{x.id}','{x.warehouse_id}','{x.default_value}')", extrafield_values)))
    request += "\nON CONFLICT (extra_field_id, warehouse_id) DO UPDATE SET default_value = EXCLUDED.default_value;\n"
    return request


def get_all_extra_fields_inserts_request() -> str:
    print(f'converting: csv/extra_fields.csv')
    from_csv = get_wh_id_and_extra_fields_id_from_csv()
    extra_fields_ids = from_csv.get('extra_fields_ids')
    warehouse_id = from_csv.get('warehouse_id')
    required_extra_fields_datas = list(filter(lambda field: field.id in extra_fields_ids, get_all_extra_fields()))
    request = get_extra_field_id_insert_request(extra_fields_ids)
    request += '\n' + get_extra_field_values_insert_request(
        ExtraFieldValue.get_values_from_extra_field_data(required_extra_fields_datas))
    extra_field_data = ExtraField.get_extra_fields_from_extra_field_data(required_extra_fields_datas, warehouse_id)
    if len(extra_fields_ids) != len(extra_field_data):
        data_ids = list(map(lambda ef: ef.id , extra_field_data))
        raise Exception(f"{list(set(extra_fields_ids).symmetric_difference(set(data_ids)))} in extra_field.csv not exist in extra_fields.json")
    request += '\n' + get_extra_field_insert_request(
        extra_field_data)
    request += '\n'
    return request
