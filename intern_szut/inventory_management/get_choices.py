from django.utils.translation import gettext_lazy as _


class GetChoices:
    @classmethod
    def get_enum_choices(cls, enum_data, append_unknown=False):
        unknown = {'id': 'unknown', 'label': _('Unbekannter Status')}
        enum_choices = []

        for status in enum_data:
            devices_statuses_dict = {'id': enum_data(status).value, 'label': enum_data(status).label}
            enum_choices.append(devices_statuses_dict)

        if append_unknown:
            enum_choices.append(unknown)

        return enum_choices

    @classmethod
    def make_labels_readable(cls, enum_data, status_options, label_key: str):
        label_name = label_key + '_label'
        for data_set in enum_data:
            if data_set[label_key] is not None:
                data_set[label_name] = status_options(data_set[label_key]).label
            else:
                data_set[label_key] = 'unknown'
                data_set[label_name] = _('Unbekannt')

        return enum_data
