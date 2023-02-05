## Resty: 
A microservice that exposes a simple api with a post rest endpoint.
- The post endpoint expects a list with 10 NPM packages

## Healthy: 
A microservice that receives the above list and check for “security health” according to the following rules:
- Last Version is maximum 30 days old
- Number of maintainers is at least 2
- Latest commit in the related GitHub repository is maximum 14 days old 