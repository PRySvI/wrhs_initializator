warehouses_ids = list()


def extract_wh(row: dict):
    try:
        warehouses_ids.append(row['warehouse_id'])
    except KeyError as e:
        pass


def check_wh_ids():
    if len(warehouses_ids) != 0 and not all(el == warehouses_ids[0] for el in warehouses_ids):
        raise Exception('warehouse_ids not matched verify your csv files')
