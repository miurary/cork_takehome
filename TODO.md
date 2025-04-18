Things I missed in the requirements:
1. Enforcing multi-tenancy - ran out of time, would add this by checking tenant_id in my GET query
2. GET endpoint unfinished - differences between SQLite and SQL caused me some last minute bugs that ate time. My query grabs all rows with failed logins in the last 5 minutes and counts them grouped by the origin. I was going to interate through these and check if the count per origin was greater than 3, and add it to a list to return to the user if so. I also wasn't able to get to pagination and sorting. For pagination, I was going to use the limit and offset keywords in my query. For sorting, I was going to accept a 'sort' and 'direction' parameters in the request which would specify the field to sort by and whether it should be ascending or descending. Though since we're only returning the origin, there should only be one field to sort by.

How I would expand this API:
1. On the SQL side, I would have tables for tenants and users so the ids aren't just dummy variables.
2. Add another endpoint to show the history of groups of failed login requests. Possible that the user checking won't have their account being brute-forced at the same time they access the first GET endpoint, so this would allow them to see if there were other attempts in the past.
3. Add an endpoint to detect a single successful login at the end of a string of failures from the same location to expose a possible security risk (brute force succeeded)
4. Add an endpoint to show origins where multiple logins have succeeded. Users can check this and make sure that all logins are coming from places they were.
