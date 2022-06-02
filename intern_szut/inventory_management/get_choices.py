from django.utils.translation import gettext_lazy as _


class GetChoices:
    @classmethod
    def get_enum_choices(cls, data_set, append_unknown=False):
        unknown = {'id': 'unknown', 'label': _('Unbekannter Status')}
        enum_choices = []

        for data in data_set:
            devices_statuses_dict = {'id': data_set(data).value, 'label': data_set(data).label}
            enum_choices.append(devices_statuses_dict)

        if append_unknown:
            enum_choices.append(unknown)

        return enum_choices

    @classmethod
    def make_labels_readable(cls, data_set, enum_options, label_key: str):
        label_name = label_key + '_label'
        for data in data_set:
            if data[label_key] is not None:
                data[label_name] = enum_options(data[label_key]).label
            else:
                data[label_key] = 'unknown'
                data[label_name] = _('Unbekannt')

        return data_set
