from traitlets.config import Config
import json
import os

import nbformat
from nbconvert import HTMLExporter
from nbparameterise import extract_parameters, parameter_values, replace_definitions

def _convert_config():
    report_config = Config({'ExecutePreprocessor': {
        'enabled': True,
        'timeout': 3600
    },
    'TemplateExporter': {
        'exclude_input_prompt': True,
        'exclude_input': True,
        'exclude_output_prompt': True,
        'template_name': 'classic'}
    })
    return report_config

def convert_notebook(in_file, out_file, parameters=None):
    with open(in_file) as f:
        nb = nbformat.read(f, as_version=4)

    if parameters:
        orig_parameters = extract_parameters(nb)
        params = parameter_values(orig_parameters, NB_PARAMETERS=json.dumps(parameters))
        nb = replace_definitions(nb, params, execute=False)

    exportHtml = HTMLExporter(config=_convert_config())
    output, resources = exportHtml.from_notebook_node(nb)
    print("Generating %s" % out_file)
    open(out_file, mode='w', encoding='utf-8').write(output)
