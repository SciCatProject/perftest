# SciCat Performance Testing

To run the performance test:

```
docker-compose up
```

This creates a mongodb instance, a catamel instance and a catanie instance.

It should return a time to ingest a number of datasets (currently 100)
```
scicatingest_1  | promise took 240 ms
```
