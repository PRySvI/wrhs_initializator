import csv
import os

from extra_field_extractor import get_all_extra_fields_inserts_request

def covertToSQL(filename: str, column, suffix):
    print(f'converting: {filename}')
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
    write_to_result(result)


def write_to_result(result):
    file_object = open('result.sql', 'a', encoding='UTF8')
    file_object.write(result)
    file_object.close()


def convert_destinations(filename: str, suffix, lang: str):
    from destinations import load_destinations
    write_to_result(load_destinations(filename, suffix, lang))


def convert_extra_fields():
    write_to_result(get_all_extra_fields_inserts_request())


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Initilizator information')
    parser.add_argument('--lang', dest='lang', type=str, help='Lang of parsing')
    args = parser.parse_args()
    lang = args.lang
    print(f'started to parse with language {lang} \n')

    try:
        os.remove("result.sql")
    except FileNotFoundError:
        print('result not found, ignore')
    # (id, name, cost_center, ean, timezone)
    covertToSQL('csv/warehouse.csv', 'pickingwavebox.warehouses',
                "ON CONFLICT (id) DO UPDATE SET"
                " name = EXCLUDED.name,"
                " cost_center = EXCLUDED.cost_center,"
                " ean = EXCLUDED.ean;")
    # (id, name, warehouse_id)
    covertToSQL('csv/univers.csv', 'pickingwavebox.universes',
                "ON CONFLICT (id, warehouse_id) DO UPDATE SET name = EXCLUDED.name;")
    # (id, name, warehouse_id)
    covertToSQL('csv/sectors.csv', 'pickingwavebox.sectors',
                "ON CONFLICT (id, warehouse_id) DO UPDATE SET name = EXCLUDED.name;")
    # (id, warehouse_id)
    covertToSQL('csv/stock_zones.csv', 'pickingwavebox.stock_zones',
                "ON CONFLICT (id, warehouse_id) DO NOTHING;")
    # (id, name, warehouse_id)
    covertToSQL('csv/order_types.csv', 'pickingwavebox.order_types',
                "ON CONFLICT (id, warehouse_id) DO UPDATE SET name = EXCLUDED.name;")
    # (name, type_id, type_name, third_number, third_sub_number, warehouse_id)
    convert_destinations('csv/destinations.csv',
                         "ON CONFLICT (type_id, third_number, third_sub_number, warehouse_id) DO UPDATE SET name = EXCLUDED.name, "
                         "warehouse_id = EXCLUDED.warehouse_id;", lang)

    covertToSQL('csv/box_label_printers.csv', 'pickingwavebox.box_label_printers',
                "ON CONFLICT (id, warehouse_id) DO NOTHING;")

    # covertToSQL('csv/item_label_printers.csv', 'pickingwavebox.item_label_printers',
    #             "ON CONFLICT (id, warehouse_id) DO NOTHING;")

    convert_extra_fields()


if __name__ == '__main__':
    main()
    print('\nsuccess ')
