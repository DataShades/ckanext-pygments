from ckan.plugins import toolkit as tk

import ckanext.pygments.utils as pygment_utils


@tk.side_effect_free
def pygments_formats_list(context, data_dict):
    result = []

    for formats, _ in pygment_utils.LEXERS.items():
        for res_format in formats:
            result.append({"value": res_format, "text": res_format})

    return result
