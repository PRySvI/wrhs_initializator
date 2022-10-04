import csv
from warehouses_checker import extract_wh


def get_type_name_by_id_and_lang(id: int, lang: str):
    types = dict()
    types['7'] = {'fr': 'Magasins Stores', 'es': 'Tiendas'}
    types['10'] = {'fr': 'Secteurs entrepot', 'es': 'Sectores almacén'}
    types['25'] = {'fr': 'Zone logistique', 'es': 'Área de logística'}
    types['43'] = {'fr': 'Groupe logistique', 'es': 'Grupo logistico'}
    types['48'] = {'fr': 'Clients finaux VADA', 'es': 'Cliente final VADA'}
    try:
        res = types.get(id).get(lang)
    except:
        res = 'WRONG_NAME'
    return res


def load_destinations(filename: str, suffix, lang="fr"):
    print(f'converting: {filename}')
    with open(filename, mode='r', encoding='UTF8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        result = "INSERT INTO pickingwavebox.destinations \n" \
                 " (name, type_id, type_name, third_number, third_sub_number, warehouse_id) VALUES \n"

        for row in csv_reader:
            extract_wh(row)
            # print(f'\t {row["name"]}.')
            name = row['name']
            if name == '':
                name = 'NOT_DEFINED_NAME'
            if '---' in name:
                name = 'WRONG_DEFINED_NAME'
            if "'" in name:
                name = name.replace("'", "''")
            if len(name) < 3:
                name = "SHORT_NAME_PREFIX_" + name

            type_id = row['type_id']
            type_name = get_type_name_by_id_and_lang(type_id, lang)
            # if type_id == '7':
            #     type_name = 'Magasins Stores'
            # elif type_id == '10':
            #     type_name = 'Secteurs entrepot'
            # elif type_id == '25':
            #     type_name = 'Zone logistique'
            # elif type_id == '43':
            #     type_name = 'Groupe logistique'
            # elif type_id == '48':
            #     type_name = 'Clients finaux VADA'

            third_number = row['third_number']
            third_sub_number = row['third_sub_number']
            warehouse_id = row['warehouse_id']
            result += f"\t ('{name}', {type_id}, '{type_name}', {third_number}, {third_sub_number}, '{warehouse_id}'),\n"
        result = ''.join(result.rsplit(',', 1))
        result += f"{suffix} \n\n"
        return result
