



getting data, since we technically don't need to serve live data (users should be using external resources)
we need a finance API to serve our data.
We COULD: cache data data periodically, disabling limit reqs if there are multiple users

scaling up: live users req their own data - can get rate limited pretty quick, so lets do caching for now




