#Copyright (C) 2011 by John O'Brien
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
"""REST Resources of the files api."""
from u1rest.lib.client import ResourceClient
from u1rest.files.content import ContentClient

BASE_API_PATH = "/api/file_storage/v1"


def get_user(res_host, cont_host, auth):
    """Get a user object for accessing rest resources.

    @param res_host: The host for File Resources (metadata)
    @param cont_host: The host for File Content.
    @param auth: An authenticator used in authenticating requests.
    """
    resource_client = ResourceClient(res_host, auth, BASE_API_PATH)
    content_client = ContentClient(cont_host, auth)
    user_json = resource_client.get_resource()
    return FileStorageUser(user_json, resource_client, content_client)


class FileStorageUser(object):
    """A File Storage User resource.

    This is the main part of the API where typically every call is made.

    The get, put, delete are provided for user who do not need a simplified api
    and plan on parsing the JSON themselves.

    Other methods are provided that return serialized objects for simplified
    user of the API.
    """
    resource_path = None

    def __init__(self, res_json, resource_client, content_client):
        self.__dict__.update(res_json)
        self.resource_client = resource_client
        self.content_client = content_client

    def get(self, path, params=None):
        """GET a resource.

        @param path: The path of the resource relative to the base API.
        @param params: Optionally a dictionary of querystring values.
        """
        return self.resource_client.get_resource(path, params=params)

    def put(self, path, data=None, params=None):
        """PUT a resource.

        @param path: The path of the resource relative to the base API.
        @param data: A JSON Serializable object sent in the PUT
        @param params: Optionally a dictionary of querystring values.
        """
        return self.resource_client.put_resource(path, data, params=params)

    def delete(self, path, params=None):
        """DELETE a resource.
.
        @param path: The path of the resource relative to the base API.
        @param params: Optionally a dictionary of querystring values.
        """
        self.resource_client.delete_resource(path, params=params)

    def make_file(self, path):
        """Make a File.

        @param path: The path of the file using the <volume path>/<node path>.
            For example ~/Ubuntu One/a/b/c/file.txt
        """
        res_json = self.put(path, data={"kind": "file"})
        return FileNode(res_json, self)

    def make_directory(self, path):
        """Make a Directory.

        @param path: The path of the file using the <volume path>/<node path>.
            For example ~/Ubuntu One/a/b/c/dirname
        """
        res_json = self.put(path, data={"kind": "directory"})
        return DirectoryNode(res_json, self)

    def get_node(self, path, with_children=False):
        """Get a File or Directory node.

        @param path: The path of the file using the <volume path>/<node path>.
            For example ~/Ubuntu One/a/b/c/dirname
        @param with_children: If True, the children property of the directory
            will be filled with Node Resources of the direct children.
        """
        params = {'include_children': 'true'} if with_children else None
        res_json = self.get(path, params=params)
        return get_node_resource(res_json, self)

    def set_file_public(self, path, public=True):
        """Make a file public.

        @param path: The path of the file using the <volume path>/<node path>.
            For example ~/Ubuntu One/a/b/c/file.txt
        @param public: If True the file will be published else it will be
            unpublished. Defaults to True.
        """
        res_json = self.put(path, data={"is_public": public})
        return get_node_resource(res_json, self)

    def move_node(self, path, new_path):
        """Move a node from one path to the other.

        The new_path is a path relative path within the volume.
        """
        res_json = self.put(path, data={"path": new_path})
        return get_node_resource(res_json, self)

    def make_volume(self, path):
        """Create a new Volume (aka UDF)."""
        path = 'volumes/' + path.lstrip("/")
        res_json = self.put(path)
        return Volume(res_json, self)

    def get_volume(self, path):
        """Get a Volume."""
        path = 'volumes/' + path.lstrip("/")
        res_json = self.get(path)
        return Volume(res_json, self)

    def delete_volume(self, path):
        """Get a Volume."""
        path = 'volumes/' + path.lstrip("/")
        self.delete(path)

    def get_volumes(self):
        """Get a list of all Volumes."""
        res_json = self.get('volumes')
        return [Volume(v, self) for v in res_json]

    def load(self):
        """Reload this User Resource."""
        res_json = self.get(self.resource_path)
        self.__dict__.update(res_json)

    def download_file(self, path, destination=None):
        """Download a file.

        @param destination: The local directory to download the file to.
        """
        self.content_client.get_file(path, download_directory=destination)

    def upload_file(self, file_name, path):
        """Download a file."""
        response = self.content_client.put_file(file_name, path)
        return get_node_resource(response, self)


class Resource(object):
    """Base class for all resources providing common methods.

    All resources are dynamically loaded from the JSON returned in a Resource
    Response. This is done because all File Storage resource have a
    resource_path property which identifies the resource.
    """
    resource_path = None

    def __init__(self, res_json=None, user=None):
        self.__dict__.update(res_json)
        self.user = user

    def load(self):
        """Reload the resource."""
        res_json = self.user.get(self.resource_path)
        self.__dict__.update(res_json)

    def delete(self):
        """Delete the resource."""
        self.user.delete(self.resource_path)


def get_node_resource(res_json, user):
    """Used when given a Node Respresentation to return the right resource.

    @param res_json: The JSON representation of the node.
    @param user: The {FileStorageUser} Resource used to get the node.
    """
    if res_json.get('kind') == 'file':
        return FileNode(res_json, user)
    else:
        return DirectoryNode(res_json, user)


class DirectoryNode(Resource):
    """Directory Node Resource."""
    def __init__(self, res_json=None, user=None):
        super(DirectoryNode, self).__init__(res_json=res_json, user=user)
        if res_json and res_json.get('children'):
            self.children = [get_node_resource(n, user)
                             for n in res_json.get('children')]

    def make_file(self, name):
        """Make a file in this directory given a file name.

        @param name: The name of the file to be created under this path.
        """
        path = self.resource_path + '/' + name.lstrip('/')
        return self.user.make_file(path)

    def make_directory(self, name):
        """Make a subdirectory in this directory given a directory name.

        @param name: The name of the directory to be created under this path.
        """
        path = self.resource_path + '/' + name.lstrip('/')
        return self.user.make_directory(path)

    def load(self, with_children=False, cascade=False):
        """Reload this directory.

        @param with_children: If True, direct children will be loaded into
            children.
        @param cascade: If True all descendants of this node will be loaded
            into the children recursively. This should be used with caution.
        """
        node = self.user.get_node(self.resource_path,
                                  with_children=with_children or cascade)
        if cascade:
            for child in [d for d in node.children if d.kind == 'directory']:
                child.load(cascade=True)
        self.__dict__.clear()
        self.__dict__.update(node.__dict__)

    def move(self, new_path):
        """Move this node to a new path.

        @param new_path: The new path of the node. Note that this path is
            relative the volume path, so the volume path is not included.
            For example node.mode("/a/b/c") will move the node to a new path
            under the volume. Moving to a different volume is not permitted.
        """
        node = self.user.move_node(self.resource_path, new_path)
        self.__dict__.clear()
        self.__dict__.update(node.__dict__)


class FileNode(Resource):
    """A File Node Resource."""

    def set_public(self, public=True):
        """Set the file public.

        @param public: If True the file will be published else it will be
            unpublished. Defaults to True.
        """
        node = self.user.set_file_public(self.resource_path, public)
        self.__dict__.clear()
        self.__dict__.update(node.__dict__)

    def move(self, new_path):
        """Move this node to a new path.

        @param new_path: The new path of the node. Note that this path is
            relative the volume path, so the volume path is not included.
            For example node.mode("/a/b/c") will move the node to a new path
            under the volume. Moving to a different volume is not permitted.
        """
        node = self.user.move_node(self.resource_path, new_path)
        self.__dict__.clear()
        self.__dict__.update(node.__dict__)

    def download(self, destination=None):
        """Download this file.

        @param destination: The local directory to download the file to.
        """
        return self.user.download_file(
            self.resource_path, destination=destination)

class Volume(Resource):
    """A Volume Resource."""
    node_path = None

    def get_root_dir(self, with_children=False):
        """Get the root directory node for this volume."""
        return self.user.get_node(self.node_path, with_children)
