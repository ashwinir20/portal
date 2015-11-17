# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pprint import pprint
import json

from django.shortcuts import render
from django.http import HttpResponse
from cloudmesh_client.comet.cluster import Cluster
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.cloud.hpc.hpc import Hpc
from django.template.defaulttags import register
from cloudmesh_client.common.ConfigDict import ConfigDict
from sqlalchemy.orm import sessionmaker

from charts import Chart


def Session():
    from aldjemy.core import get_engine
    engine = get_engine()
    _Session = sessionmaker(bind=engine)
    return _Session()


session = Session()


def message(msg):
    return HttpResponse("Message: %s." % msg)


def cloudmesh_vclusters(request):
    return message("Not yet Implemented")


@register.filter
def get_item(dictionary, key):
    value = dictionary.get(key)
    if value is None:
        value = "-"
    return value


def dict_table(request, **kwargs):
    context = kwargs
    pprint(context)
    return render(request, 'cloudmesh_portal/dict_table.jinja', context)


def comet_logon(request):
    c = None
    try:
        c= Comet.logon(request)
        return render(request,
                      'cloudmesh_portal/logon_error.jinja')
    except:
        return c

def comet_status(request):
    context = {}
    c = comet_logon(request)
    data = json.loads(Cluster.simple_list(format="json"))
    pprint(data)
    print (type(data))

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
    for id in data.keys():
        counter[id] = {
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

    print (counter)
    for key, node in details.items():

        if node['kind'] == 'compute':

            name = node['cluster']
            state = node['state']

            if state in [None, 'None']:
                state = 'unkown'

            print ("SSSSSSS", state, name, node['kind'])

            element = counter[name]
            counter[name]['status'][state] += 1
            counter[name]['total'] += 1
            counter[name]['name'] = name

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

    # pprint(type(data), data)
    order = [
        "name",
        "project",
        "nodes",
        "computes",
        "frontend name",
        "frontend state",
        "frontend type",
        "frontend rocks_name",
        "description",
    ]
    header = [
        "Name",
        "Project",
        "Count",
        "Nodes",
        "Frontend (Fe)",
        "State (Fe)",
        "Type (Fe)",
        "Rocks name (Fe)",
        "Description",
    ]

    return (dict_table(request, title="Comet List", data=data, order=order))



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
        "ip",
        "rocks_name",
        "cpus",
        "cluster",
        "host",
        "memory",
    ]

    return (dict_table(request, title="Comet List", data=dictionary, order=order))


def cloudmesh_clouds(request):
    config = ConfigDict(filename="cloudmesh.yaml")
    clouds = config["cloudmesh.clouds"]
    data = {}
    attributes = ['cm_host',
                  'cm_label',
                  'cm_heading',
                  'cm_type',
                  'cm_type_version']
    for cloud in clouds:
        data[cloud] = {}
        for attribute in attributes:
            data[cloud][attribute] = clouds[cloud][attribute]
        print clouds[cloud]['cm_type']
        if clouds[cloud]['cm_type'] == "ec2":
            data[cloud]['username'] = clouds[cloud]['credentials']['userid']
        elif clouds[cloud]['cm_type'] == "azure":
            data[cloud]['username'] = 'not implemented'
        elif clouds[cloud]['cm_type'] == "openstack":
            data[cloud]['username'] = clouds[cloud]['credentials'][
                'OS_PASSWORD']

    headers = ['username']
    headers.extend(attributes)

    pprint(data)

    context = {
        'data': data,
        'title': "Cloud List",
        'order': headers,
    }
    return render(request,
                  'cloudmesh_portal/dict_table.jinja',
                  context)


def comet_list_queue(request):
    cluster = "comet"
    format = "json"
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

    data = json.loads(Hpc.queue(cluster, format=format))
    print (data)

    return (dict_table(request, title="Comet Queue", data=data, order=order))


def comet_info(request):
    cluster = "comet"
    format = "json"
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
    data = json.loads(Hpc.info(cluster, format=format))
    print (data)

    return (dict_table(request, title="Comet Queue", data=data, order=order))


def homepage(request):
    return render(request,
                  'cloudmesh_portal/home.jinja')
