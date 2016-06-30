from __future__ import unicode_literals
from __future__ import print_function
from pprint import pprint
import json

from django.shortcuts import render
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.image import Image
from cloudmesh_client.cloud.flavor import Flavor
from cloudmesh_client.cloud.attributes import Attributes
from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.cloud.launcher import Launcher
from cloudmesh_client.common.util import banner, path_expand

from ..views import dict_table


def cloudmesh_launcher_table(request):
    launcher_config = ConfigDict(path_expand("~/.cloudmesh/cloudmesh_launcher.yaml"))

    context = {
        'recipies': launcher_config["cloudmesh.launcher.recipes"],
        'title': '<div><i class="fa fa-rocket"></i> Cloudmesh Launcher List </div>'
    }

    return render(request,
                  'cloudmesh_portal/launcher/mesh_launch_table.jinja',
                  context)


def cloudmesh_launcher(request):
    if request.method == 'POST':
        print ("HHHHHH", request.form.keys())
        for key in request.form.keys():
            print (key, ":", request.form[key])
    else:
        print ("HEY JUDE")

    launcher_config = ConfigDict(path_expand("~/.cloudmesh/cloudmesh_launcher.yaml"))

    context = {
        'recipies': launcher_config["cloudmesh.launcher.recipes"],
        'title': '<div><i class="fa fa-rocket"></i> Cloudmesh Launcher </div>'
    }

    pprint(context)

    return render(request,
                  'cloudmesh_portal/launcher/mesh_launch.jinja',
                  context)


def cloudmesh_launcher_start(request):
    parameters = dict(request.POST)
    for key in parameters:
        try:
            parameters[key] = parameters[key][0]
        except:
            pass
    if 'csrfmiddlewaretoken' in parameters:
        del parameters['csrfmiddlewaretoken']

    response = 'error'
    if parameters["name"]:
        name = parameters["name"]

        launcher_config = ConfigDict(path_expand("~/.cloudmesh/cloudmesh_launcher.yaml"))
        recipe = dict(launcher_config["cloudmesh.launcher.recipes"])[name]

        print(json.dumps(recipe, indent=4))

        response = "error"

        if recipe["script"]["type"] in ["sh", "shell"]:
            script = recipe["script"]["value"].format(**parameters)
            print (script)
            launcher = Launcher("shell")
            print (type(launcher))
            response = launcher.run(script=script)
            parameters["script"] = script

    else:
        parameters = "error"

    context = {
        'title': '<div><i class="fa fa-rocket"></i> Cloudmesh Launcher</div>',
        "response": response,
        "parameters": parameters,
    }

    return render(request,
                  'cloudmesh_portal/launcher/mesh_launch_response.jinja',
                  context)

def badge(msg):
    return '<span class="label label-pill label-info">{}</span>'.format(msg)

def url(msg, link):
    print (locals())
    data = {
        'msg': msg,
        'link': link
    }
    return '<a href="{link}"> {msg} </a>'.format(**data)


def cloudmesh_clouds(request):
    config = ConfigDict(filename="cloudmesh.yaml")
    clouds = config["cloudmesh.clouds"]
    active = config["cloudmesh.active"]
    default = Default.get_cloud()
    data = {}
    attributes = ['cm_label',
                  'cm_host',
                  'cm_heading',
                  'cm_type',
                  'cm_type_version']
    for cloud in clouds:
        name = {'cloud': cloud}
        data[cloud] = {}
        for attribute in attributes:
            data[cloud][attribute] = clouds[cloud][attribute]
        print (clouds[cloud]['cm_type'])
        if clouds[cloud]['cm_type'] == "ec2":
            data[cloud]['username'] = clouds[cloud]['credentials']['userid']
        elif clouds[cloud]['cm_type'] == "azure":
            data[cloud]['username'] = 'not implemented'
        elif clouds[cloud]['cm_type'] == "openstack":
            data[cloud]['username'] = clouds[cloud]['credentials'][
                'OS_USERNAME']
        if cloud in active:
            data[cloud]['active'] = 'yes'
        else:
            data[cloud]['active'] = 'no'
        if cloud in [default]:
            data[cloud]['default'] = True
        else:
            data[cloud]['default'] = False
        data[cloud]['info'] = "".join([
            url('<i class="fa fa-file-text-o"></i>', '/cm/cloud/{cloud}/'.format(**name)),
            url('<i class="fa fa-file-image-o"></i>', '/cm/image/{cloud}/'.format(**name)),
            url('<i class="fa fa-wrench"></i>', '/cm/flavor/{cloud}/'.format(**name)),
            url('<i class="fa fa-database"></i>', '/cm/vm/{cloud}/'.format(**name))])

    order = [
        'default',
        'active',
        'cm_label',
        'info',
        'cm_host',
        'cm_heading',
        'cm_type',
        'cm_type_version'
    ]
    header = [
        'Default',
        'Active',
        'Label',
        'Info',
        'Host',
        'Description',
        'Type',
        'Version'
    ]

    pprint(data)

    context = {
        'data': data,
        'title': "Cloud List",
        'order': order,
        'header': header,
    }
    return render(request,
                  'cloudmesh_portal/cm/cloud_list.jinja',
                  context)


def cloudmesh_cloud(request, cloud=None):
    if cloud is None:
        cloud = Default.get_cloud()
    config = ConfigDict(filename="cloudmesh.yaml")
    cloud_config = dict(config["cloudmesh.clouds"][cloud])
    active = cloud in config["cloudmesh.active"]
    default = Default.get_cloud()

    if 'OS_PASSWORD' in cloud_config['credentials']:
        cloud_config['credentials']['OS_PASSWORD'] = '********'
    context = {
        'data': cloud_config,
        'title': "Cloud {cm_heading}".format(**cloud_config),
    }
    return render(request,
                  'cloudmesh_portal/cm/cloud_table.jinja',
                  context)


#
# CLOUDMESH DEFAULTS
#


def cloudmesh_defaults(request):
    data = json.loads(Default.list(format='json'))

    order = [
        'cloud',
        'name',
        'value',
        'project',
        'user',
    ]
    header = [
        'Cloud',
        'Variable',
        'Value',
        'Project',
        'User',
    ]

    return (dict_table(request,
                       title="Cloudmesh Default",
                       data=data,
                       header=header,
                       order=order))


def cloudmesh_images(request, cloud=None):
    banner("images")
    if cloud is None:
        cloud = Default.get_cloud()

    data = Image.list(cloud, format='dict')

    default = Default.get_image(cloud)

    for index in data:
        element = data[index]
        element['default'] = element['name'] == default

    # print (json.dumps(data, indent=4))

    order, header = Attributes.list(cloud,"image")

    order.insert(0,"default")
    header.insert(0,"Default")

    return dict_table(request,
                       title="Cloudmesh Images {}".format(cloud),
                       data=data,
                       order=order,
                       header=header)


def cloudmesh_flavors(request, cloud=None):
    if cloud is None:
        cloud = Default.get_cloud()
    data = Flavor.list(cloud, format='dict')

    default = Default.get_flavor(cloud)

    for index in data:
        element = data[index]
        element['default'] = element['name'] == default

    # print (json.dumps(data, indent=4))

    order, header = Attributes.list(cloud,"flavor")

    order.insert(0,"default")
    header.insert(0,"Default")

    return dict_table(request,
                      title="Cloudmesh Flavors {}".format(cloud),
                      data=data,
                      order=order,
                      header=header)


def cloudmesh_vms(request, cloud=None):
    if cloud is None:
        cloud = Default.get_cloud()
    data = Vm.list(cloud=cloud, output_format='dict')
    print (json.dumps(data, indent=4))
    order = ['id',
             'uuid',
             'label',
             'status',
             'static_ip',
             'floating_ip',
             'key_name',
             'project',
             'user',
             'cloud']
    return dict_table(request,
                      title="Cloudmesh VMs {}".format(cloud),
                      data=data,
                      order=order)


def cloudmesh_refresh(request, action=None, cloud=None):
    if action is None:
        action = ['image', 'flavor', 'vm']
    else:
        action = [action]

    if cloud is None:
        cloud = Default.get_cloud()
        # TODO: should actually be all active clouds

    data = Vm.list(cloud=cloud, output_format='dict')
    print (json.dumps(data, indent=4))
    order = ['id',
             'uuid',
             'label',
             'status',
             'static_ip',
             'floating_ip',
             'key_name',
             'project',
             'user',
             'cloud']
    return dict_table(request,
                      title="Cloudmesh VMs {}".format(cloud),
                      data=data,
                      order=order)
