from typing import Dict


class ExtraFieldData:
    def __init__(self, id: str, default_value: str, values: Dict[str, int]):
        self.id: str = id
        self.default_value: str = default_value
        self.values: Dict[str, int] = values


class ExtraField:
    def __init__(self, id: str, default_value: str, warehouse_id: str):
        self.id: str = id
        self.warehouse_id: str = warehouse_id
        self.default_value: str = default_value

    @staticmethod
    def get_extra_fields_from_extra_field_data(data: list[ExtraFieldData], warehouse_id: str) -> []:
        return list(map(lambda x: ExtraField(x.id, warehouse_id, x.default_value), data))


class ExtraFieldValue:
    def __init__(self, id: str, value: str, order: int):
        self.id: str = id
        self.value: str = value
        self.order: int = order

    @staticmethod
    def get_values_from_extra_field_data(data: list[ExtraFieldData]) -> []:
        res: list[ExtraFieldValue] = []
        for extra_field_data in data:
            if extra_field_data.default_value not in extra_field_data.values.keys():
                raise Exception(
                    f"Extra field {extra_field_data.id} default_value {extra_field_data.default_value} not in values {extra_field_data.values}")
            for key in extra_field_data.values:
                res.append(ExtraFieldValue(extra_field_data.id, key, extra_field_data.values.get(key)))
        return res
