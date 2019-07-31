# SciCat Performance monitoring

To run the performance test you currently have 2 options:

## Docker based ingest test

```
docker-compose up
```

This creates a mongodb instance, a catamel instance and a catanie instance.

It should return a time to ingest a number of datasets (currently 100)
```
scicatingest_1  | promise took 240 ms
```

## Locust Based performance tool

This test the API server by running a set of API calls which simulate groups of different users

### Prerequisites

1. Install locust tool

   Follow the installation description at https://docs.locust.io/en/stable/installation.html . 
   This will provide a new command "locust" . Adjust your PATh if needed.

2. Setup API server

   Any existing API server (catamel) instance with a connected DB backend will do. 
   This can be your locally running development instance, a docker based catamel instance like [above](#docker-based-ingest-test), 
   or a production system.

### Run tests with a Web GUI

Assuming your API server is running locally you simply do the following. 

```
cd locust
locust --host=http://localhost:3000  WebsiteUser BeamlineIngestor
```

The command will look for the file *locustfile.py* in your current working directory. 
This file defines which type of users exist and what API calls should be run.
An example file is in the folder locust/locustfile.py.
You then open http://localhost:8089 and enter the number of users to simulate
as well as the "hatch rate", i.e. how fast users are spawned per second. 
The browser then presents resulting statistics both in tabular and chart form.
Below you find two examples with 10 and 100 users respectively:

![Resulting Statistics for 10 users](/locust/images/locust-table-10users.png?raw=true "API Statistics for 10 users")
![Charts for 10 users](/locust/images/locust-chart-10users.png?raw=true "Charts for 10 users")
![Resulting Statistics for 100 users](/locust/images/locust-table-100users.png?raw=true "API Statistics for 100 users")
![Charts for 100 users](/locust/images/locust-chart-100users.png?raw=true "Charts for 100 users")

### Run test without Web GUI

The following command will run tests for 60 seconds with 100 users and a hatch rate of 5/s:

```
locust --host=http://localhost:3000 --no-web -c 100 -r 5 --run-time 60s WebsiteUser BeamlineIngestor
```

The final summary table looks like this:

```
 Name                                                          # reqs      # fails     Avg     Min     Max  |  Median   req/s
--------------------------------------------------------------------------------------------------------------------------------------------
 GET API index                                                      9     0(0.00%)     111       4     792  |      28    0.20
 DELETE Delete old test datasets                                 1260     0(0.00%)       9       7      37  |       8    0.00
 GET Facetquery for 5 facets with given ownerGroup                 37     0(0.00%)     747      93    3841  |     360    1.00
 GET Fullquery for 30 datasets in given ownerGroup                 40     0(0.00%)    1477     223    4291  |     400    0.80
 POST Ingest raw dataset                                         4132     0(0.00%)     117       9    8038  |      72  148.40
 POST Login as ingestor                                           102     0(0.00%)    4194      85    6703  |    4900    0.00
 POST Logout as ingestor                                          100     0(0.00%)     138      49     272  |     130    0.00
 GET Query for 100 datasets in given ownerGroup                    44     0(0.00%)     583      26    3358  |     120    1.50
 GET Query for 2 datasets in given ownerGroup                     204     0(0.00%)     683      13    4502  |     110    6.90
 GET Query for old test datasets                                    1     0(0.00%)     104     104     104  |     100    0.00
--------------------------------------------------------------------------------------------------------------------------------------------
 Total                                                           5929     0(0.00%)                                     158.80

Percentage of the requests completed within given times
 Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
--------------------------------------------------------------------------------------------------------------------------------------------
 GET API index                                                       9     28     31     35     44    790    790    790    790    790
 DELETE Delete old test datasets                                  1260      8      9      9      9     11     12     13     17     37
 GET Facetquery for 5 facets with given ownerGroup                  37    360    470    580    610   2700   3400   3800   3800   3800
 GET Fullquery for 30 datasets in given ownerGroup                  40    400   1900   3200   3400   3900   4100   4300   4300   4300
 POST Ingest raw dataset                                          4132     72     89    110    130    220    300    380    600   8000
 POST Login as ingestor                                            102   4900   5000   5000   5100   5200   5900   6400   6500   6700
 POST Logout as ingestor                                           100    130    160    180    190    220    240    250    270    270
 GET Query for 100 datasets in given ownerGroup                     44    120    160    190    250   2600   3300   3400   3400   3400
 GET Query for 2 datasets in given ownerGroup                      204    110    170    290   1600   3200   3400   3500   3600   4500
 GET Query for old test datasets                                     1    100    100    100    100    100    100    100    100    100
--------------------------------------------------------------------------------------------------------------------------------------------
 Total                                                            5929     63     84    100    130    240    360   3300   4900   8000
```
