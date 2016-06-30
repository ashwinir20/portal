from __future__ import unicode_literals
import json

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.util import path_expand
from django.shortcuts import render

from cloudmesh_client.cloud.hpc.BatchProvider import BatchProvider
from cloudmesh_portal.views import dict_table
from cloudmesh_client.cloud.experiment import Experiment
import os
import glob


def workflow_list(request):

    workflows = glob.glob('workflow/*.py')

    print (workflows)
    data = {}
    for filename in workflows:
        data[filename] = {}
        data[filename]['name'] = filename.replace(".py", "")
        data[filename]['filename'] = filename

    context = {
        "data": data,
        "title": "Workflows",
    }
    return render(request, 'cloudmesh_portal/workflow/table.jinja', context)


def workflow_detail(request, script=None):

    script = "workflow/" + script + ".py"

    with open(script) as f:
        content = f.read()

    print (content)
    context = {
        'workflow': content,
        'file': script,
        'title': script.replace(".py", "")
    }

    return render(request,
                  'cloudmesh_portal/workflow/file.jinja',
                  context)


def workflow_graph(request, script=None):

    script = "workflow/" + script + ".py"
    graph = script.replace(".py", ".svg")

    with open(graph) as f:
        svg = f.read()

    context = {
        'graph': svg,
        'file': script,
        'title': script.replace(".py", "")
    }

    return render(request,
                  'cloudmesh_portal/workflow/graph.jinja',
                  context)
