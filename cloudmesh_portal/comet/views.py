from __future__ import unicode_literals
from pprint import pprint
import json

from django.shortcuts import render
from cloudmesh_client.comet.cluster import Cluster
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.cloud.hpc.hpc import Hpc
from cloudmesh_base.hostlist import Parameter

from ..charts import Chart
from ..views import dict_table


def comet_dict_table(request, **kwargs):
    context = kwargs
    pprint(context)
    return render(request, 'cloudmesh_portal/comet_dict_table.jinja', context)


def comet_logon(request):
    c = None
    try:
        c = Comet.logon()
        print("LOGON OK")
        return render(request,
                      'cloudmesh_portal/logon_error.jinja')
    except:
        return c


def comet_status(request):
    c = comet_logon(request)
    data = json.loads(Cluster.simple_list(format="json"))
    # pprint(data)
    # print (type(data))

    clusters = []
    for key in data:
        total = data[key]["nodes"]
        name = data[key]["name"]
        if name == "comet-fe1":
            name = "free"
        cluster = {
            "name": name,
            "total": total,
            "status": {
                'active': 0,
                'nostate': 0,
                'down': 0,
                'pending': 0,
                'unkown': total
            }
        }
        clusters.append(cluster)

    details = json.loads(Cluster.list(format="json"))

    counter = {}
    for node in details.values():
        clustername = node["cluster"]
        if clustername is not None:
            if clustername not in counter:
                counter[clustername] = {
                    'name': None,
                    'total': 0,
                    'status': {
                        'unkown': 0,
                        'active': 0,
                        'down': 0,
                        'pending': 0,
                        'nostate': 0,
                        'nostate-error': 0
                    }
                }

    # print (counter)
    for key, node in details.items():

        if node['kind'] == 'compute':

            name = node['cluster']
            state = node['state']

            if state in [None, 'None']:
                state = 'unkown'

            # print ("SSSSSSS", state, name, node['kind'])
            counter[name]['status'][state] += 1
            counter[name]['total'] += 1
            counter[name]['name'] = name
    pprint (counter)
    #
    # delete the free nodes for now
    #

    for count in counter:
        if count != "comet-fe1":
            counter['comet-fe1']['total'] = counter['comet-fe1']['total'] - \
                                            counter[count]['total']

    counter['comet-fe1']['name'] = 'free'
    counter_list = []
    for key, cluster in counter.items():
        counter_list.append(cluster)

    # context["clusters"] = counter_list

    Chart.cluster_overview_pie(counter_list, filename='pie.svg')

    #
    # delete the overall count
    #
    del counter['comet-fe1']
    counter_list = []
    for key, cluster in counter.items():
        counter_list.append(cluster)

    Chart.cluster_overview_pie_vector(counter_list, filename='pie_vector.svg')
    Chart.cluster_overview_radar(counter_list, filename='radar.svg')

    context = {
        'pid': str(Comet.find_tunnel()),
        'tunnel': str(Comet.is_tunnel())
    }

    return render(request,
                  'cloudmesh_portal/status.jinja',
                  context)


def comet_ll(request):
    c = comet_logon(request)
    data = json.loads(Cluster.simple_list(format="json"))
    pprint (data)
    #data["terminal"] = Parameter.expand(data.keys())
    for entry in data:
        data[entry]["terminal"] = ', '.join (Parameter.expand(data[entry]["computes"]))
    # pprint(type(data), data)
    order = [
        "name",
        "project",
        "nodes",
        "computes",
        "terminal",
        "frontend name",
        "frontend state",
        "frontend type",
        "description",
    ]
    header = [
        "Name",
        "Project",
        "Count",
        "Nodes",
        "Terminal",
        "Frontend (Fe)",
        "State (Fe)",
        "Type (Fe)",
        "Description",
    ]

    return comet_dict_table(request, title="Comet List", data=data, header=header, order=order)


def comet_list(request):
    c = comet_logon(request)
    data = json.loads(Cluster.list(format="json"))

    dictionary = {}

    for item in data.values():
        dictionary[item["name"]] = item

    order = [
        "name",
        "state",
        "kind",
        "type",
        "mac",
        "ip",
        "cpus",
        "cluster",
        "memory",
    ]

    return comet_dict_table(request, title="Comet List", data=dictionary, order=order)


def comet_list_queue(request):
    cluster = "comet"
    output_format = "json"
    order = [
        "jobid",
        "nodelist",
        "name",
        "partition",
        "st",
        "user",
        "time",
        "nodes",
    ]

    data = json.loads(Hpc.queue(cluster, format=output_format))
    print (data)

    return dict_table(request, title="Comet Queue", data=data, order=order)


def comet_info(request):
    cluster = "comet"
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
    data = json.loads(Hpc.info(cluster, format=output_format))
    print (data)

    return dict_table(request, title="Comet Queue", data=data, order=order)
