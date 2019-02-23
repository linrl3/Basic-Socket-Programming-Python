# DNS proxy from scratch
We implement a manipulated dns proxy from basic udp and tcp proxy. Some ISPs use the similar ideas to hijack your DNS to earn advertising dollars.

A basic dns proxy works like this: The proxy listens on port 53 for client DNS queries, forwards those queries to a single upstream DNS resolver like Google 8.8.8.8, waits for answers from it, and forwards the answers back to the client.

# Dependency
- python 2.7
- socket
- struct
## How to use
1. Two ways to go: Deploy your server on cloud service like AWS or Directly run on your local machine and test it.
2. As a client, change your DNS IP address to your AWS or your local machine, and then use `nslookup` or other tools to test it.

## Things to notice
1. UDP sockets must be declared with the SOCK_DGRAM, while TCP sockets are declared are SOCK_STREAM.
2. We use struct to build a fake DNS reponse.
