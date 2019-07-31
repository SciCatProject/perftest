from locust import HttpLocust, TaskSet
import json
import urllib

pgroup = "p01234"

def login(l):
    resp=l.client.post("/api/v3/Users/login", {"username":"ingestor", "password":"aman"},name="Login as ingestor")
    content_json = json.loads(resp.content)
    return content_json['id']
 
def logout(l):
    l.client.post("/api/v3/Users/logout",headers=l.headers,name="Logout as ingestor")

def index(l):
    l.client.get("/",name="API index")

def query(l):
    # print(dir(l.client))
    # print("Headers:",l.client.headers)
    # print("Cookies:",l.client.cookies)
    filter={"where":{"ownerGroup":pgroup},"limit":100}
    filter_json = json.dumps(filter)
    url="/api/v3/Datasets?filter=%s"
    l.client.get(
            url % filter_json,
            headers=l.headers,
            name="Query for 100 datasets in given ownerGroup"
    )

def shortquery(l):
    filter={"where":{"ownerGroup":pgroup},"limit":2}
    filter_json = json.dumps(filter)
    url="/api/v3/Datasets?filter=%s"
    l.client.get(
            url % filter_json,
            headers=l.headers,
            name="Query for 2 datasets in given ownerGroup"
    )

def fullquery(l):
    # https://dacat-qa.psi.ch/api/v3/Datasets/fullquery?fields={"mode":{},"ownerGroup":["p17828"]}&limits={"skip":0,"limit":30,"order":"creationTime:desc"}
    fields={"ownerGroup":[pgroup]}
    limits={"skip":0,"limit":30,"order":"creationTime:desc"}
    fields_json = json.dumps(fields)
    limits_json = json.dumps(limits)
    url="/api/v3/Datasets/fullquery?fields=%s&limits=%s"
    l.client.get(
            url % (fields_json, limits_json),
            headers=l.headers,
            name="Fullquery for 30 datasets in given ownerGroup"
    )

def facetquery(l):
    # https://dacat-qa.psi.ch/api/v3/Datasets/fullfacet?fields={"mode":{},"ownerGroup":["p17828"]}&facets=["type","creationTime","creationLocation","ownerGroup","keywords"]
    fields={"ownerGroup":[pgroup]}
    facets=["type","creationTime","creationLocation","ownerGroup","keywords"]
    fields_json = json.dumps(fields)
    facets_json = json.dumps(facets)
    url="/api/v3/Datasets/fullquery?fields=%s&facets=%s"
    # print("Facet Url:",url % (fields_json, facets_json))
    l.client.get(
            url % (fields_json, facets_json),
            headers=l.headers,
            name="Facetquery for 5 facets with given ownerGroup"
    )

def ingest(l):
    data = {} 
    data['owner'] =  'Bertram Astor'
    data['ownerEmail'] =  'bertram.astor@grumble.com'
    data['contactEmail'] =  'bertram.astor@grumble.com'
    data['sourceFolder'] =  '/iramjet/tif/'
    data['creationTime'] =  '2011-09-14T06:08:25.000Z'
    data['keywords'] =  [
        'Cryo', 'Calibration'
    ]
    data['description'] =  'None'
    data['type'] =  'raw'
    data['license'] =  'CC BY-SA 4.0'
    data['isPublished'] =  False
    data['ownerGroup'] =  pgroup
    data['accessGroups'] =  ['slscsaxs']
    # print("Dump:",json.dumps(data))
    resp = l.client.post(
            url="/api/v3/Datasets",
            json=data,
            headers=l.headers,
            name="Ingest raw dataset"
        )

def delete(l):
    # get list of datasetsId
    login(l)
    filter={"where":{"ownerGroup":pgroup},"fields":{"pid":1}}
    filter_json = json.dumps(filter)
    url="/api/v3/Datasets?filter=%s"
    resp = l.client.get(
            url % filter_json,
            headers=l.headers,
            name="Query for old test datasets"
        )
    # print("Status:",resp.status_code)
    content_json = json.loads(resp.content)
    for dataset in content_json:
       # print(dataset['pid'],end='')
       url="/api/v3/Datasets/%s"
       resp = l.client.delete(
            url % urllib.parse.quote_plus(dataset['pid']),
            headers=l.headers,
            name="Delete old test datasets"
       )


class UserBehavior(TaskSet):
    tasks = {index: 1, query:5, shortquery:25, fullquery:5, facetquery:5}

    def __init__(self, parent):
       super(UserBehavior, self).__init__(parent)
       self.token = ""
       self.headers = {}

    def on_start(self):
      self.token = login(self)
      self.headers = {'Authorization': self.token}

    def on_stop(self):
        logout(self)

    def setup(self):
        print("user setup called")

    def teardown(self):
        # called when locust server is stopped, not when test is stopped via Webgui
        print("user teardown called")
        

class BeamlineBehavior(TaskSet):
    tasks = {ingest: 1}

    def __init__(self, parent):
       super(BeamlineBehavior, self).__init__(parent)
       self.token = ""
       self.headers = {}

    def on_start(self):
      self.token = login(self)
      self.headers = {'Authorization': self.token}

    def on_stop(self):
        logout(self)

    def setup(self):
        print("beamline setup called, remove ingests from previous run")
        # need login already in setup phase for clean up tasks
        self.token = login(self)
        self.headers = {'Authorization': self.token}
        delete(self)

    def teardown(self):
        # called when locust server is stopped, not when test is stopped via Webgui
        print("beamline teardown called")

class WebsiteUser(HttpLocust):
    weight = 3
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000

class BeamlineIngestor(HttpLocust):
    weight = 1
    task_set = BeamlineBehavior
    min_wait = 50
    max_wait = 90
