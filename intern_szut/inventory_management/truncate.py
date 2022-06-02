class Truncate:
    @classmethod
    def truncate_data(cls, data_set, field_to_truncate,  max_length: int):
        for data in data_set:
            if len(data[field_to_truncate]) > max_length:
                data[field_to_truncate] = data[field_to_truncate][:max_length - 3] + '...'

        return data_set
