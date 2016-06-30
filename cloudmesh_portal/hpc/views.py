from __future__ import print_function
from __future__ import unicode_literals
import json

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.util import path_expand
from django.shortcuts import render

from cloudmesh_client.cloud.hpc.BatchProvider import BatchProvider
from cloudmesh_portal.views import dict_table
from cloudmesh_client.cloud.experiment import Experiment


def hpc_run_list(request, count=None, cluster=None):
    cluster = "india"
    result = {}
    ids = Experiment.list(cluster, format="list")
    print (ids)
    for count in ids:
        result[count] = {
            "list": Experiment.list(cluster, id=count, format="list")
        }

    print (result)
    print (json.dumps(result, indent=4))

    order = ["list"]
    context = {
        "data": result,
        "title": "HPC Experiments on {}".format(cluster),
        "order": ["list"]
    }

    return render(request, 'cloudmesh_portal/hpc/run_table.jinja', context)


def hpc_list(request):
    clusters = ConfigDict(path_expand("~/.cloudmesh/cloudmesh.yaml"))["cloudmesh.hpc.clusters"]
    print (clusters)
    data = {}
    for cluster in clusters:
        data[cluster] = {
            "cluster": cluster,
            "test": "test"}
    order = ["cluster"]
    context = {
        "data": data,
        "title": "Clusters",
        "order": order,
    }
    return render(request, 'cloudmesh_portal/hpc/hpc_table.jinja', context)


def hpc_queue(request, cluster=None):
    output_format = "json"
    order = [
        "jobid",
        "user",
        "partition",
        "nodes",
        "st",
        "name",
        "nodelist",
        "time",
    ]
    provider = BatchProvider(cluster)
    data = json.loads(provider.queue(cluster, format=output_format))
    print (data)

    return dict_table(request,
                      title="Queues for {}".format(cluster),
                      data=data,
                      order=order)


def hpc_info(request, cluster=None):
    output_format = "json"
    order = [
        'partition',
        'nodes',
        'state',
        'avail',
        'timelimit',
        'cluster',
        'nodelist',
        # 'updated',
    ]
    provider = BatchProvider(cluster)

    data = json.loads(provider.info(cluster, format=output_format))
    print (data)

    return dict_table(request,
                      title="Info for {}".format(cluster),
                      data=data, order=order)
