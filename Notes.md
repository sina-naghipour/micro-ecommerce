at this point, i have developed the services auth, orders, products and on top of it an nginx lies so that it will handle sending requests to the appropriate service and vice versa. the only challenging part up until now was that some services started before database started. but it was only a matter of delaying the service for some time.

the only thing that has not been done, is that authentication service does not apply for orders and products.

after doing some research i have found that this is the best approach :

Each service validates JWT itself
Products & Orders verify tokens using the Auth service’s public key/secret
Fast (no extra network hop), scalable, microservice-friendly
Need shared secret/public key (via env vars or config)

