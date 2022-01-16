import json
import os
import pickle
from enum import Enum
from io import StringIO

from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile


def get_path_for_noderun(flow_id, flowrun_id, node_id):
    return os.path.join(
        settings.FLUXIS_STORAGE_DIRECTORY, str(flow_id)[-12:], str(flowrun_id)[-12:], str(node_id)
    )


# Handles data formatting and writing
def write_output_for_node(flow_id, flowrun, data, node_id, node_run_db):
    cache.set(node_run_db.id, data)

    path = get_path_for_noderun(flow_id, flowrun.id, node_id)
    file_content = pickle.dumps(data)
    node_run_db.output.save(f"{path}.pkl", ContentFile(file_content))
    """
    # We convert all the np arrays to series
    for output_key, output_data in data.items():
        if isinstance(output_data, np.ndarray):
            data[output_key] = pd.Series(output_data)

    # We split all the dataframes and series off to go into their own file
    for output_key, output_data in data.items():
        if isinstance(output_data, pd.DataFrame) or isinstance(output_data, pd.Series):
            csv_names[output_key] = f"{node_dir}_{output_key}.csv"
            csv_files[output_key] = output_data

    for output_key, output_data in csv_files.items():
        del data[output_key]

    write_data = {
        'serial': data,
        'csv': csv_names,
    }

    file_content = json.dumps(write_data)
    node_run_db.output.save(f"{node_dir}.txt",
                            ContentFile(file_content.encode('utf-8')))

    # Now write csvs
    for extrafile_output_key, extrafile_output_data in csv_files.items():
        file = StringIO()
        extrafile_output_data.to_csv(file, header=True, index=False)
        node_run_db_eo = core.models.NodeRunExtraOutput.objects.create(
            noderun=node_run_db, port_key=extrafile_output_key)
        node_run_db_eo.output.save(
            csv_names[extrafile_output_key], ContentFile(file.getvalue().encode('utf-8')))
    """


def read_output_for_noderun(noderun):
    data = cache.get(noderun.id)
    if not data:
        # Cache doesn't have data
        # Might be because value is too old, check db:
        if not noderun.output:
            # Also no data referenced in db
            # this node run failed
            return None
        # Found data
        try:
            raw_data = noderun.output.read()
        except FileNotFoundError as e:
            # File was not found
            print(e)
            return None
        data = pickle.loads(raw_data)
    cache.set(noderun.id, data)
    return data
    """
    raw_file_content = ""
    raw_file_content = noderun.output.read()
    raw_data = json.loads(raw_file_content)

    final = {}

    for (key, val) in raw_data['serial'].items():
        final[key] = {"type": "infer",
                      "data": val}

    extra_outputs = core.models.NodeRunExtraOutput.objects.filter(
        noderun__exact=noderun)

    for eo in extra_outputs:
        # We need to fill na values with blanks, so that they can be serialized
        final[eo.port_key] = {"type": "tabular",
                              "data": pd.read_csv(eo.output).fillna(value="")}

    return final
    """
