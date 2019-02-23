# DNS proxy from scratch
We implement a manipulated dns proxy from basic udp and tcp proxy. Some ISPs use the similar ideas to hijack your DNS to earn advertising dollars.

A basic dns proxy works like this: The proxy listens on port 53 for client DNS queries, forwards those queries to a single upstream DNS resolver like Google 8.8.8.8, waits for answers from it, and forwards the answers back to the client.

## How to use
1. Deploy your server on cloud service like AWS.
2. Directly run on your local machine and test it.

## Things to notice
1. UDP sockets must be declared with the SOCK_DGRAM, while TCP sockets are declared are SOCK_STREAM.
2. 
