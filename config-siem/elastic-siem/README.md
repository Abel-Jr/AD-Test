SIEM Setup (ELK)

I'm running the ELK stack for log collection and detection. Enabled X-Pack security specifically so I could use the Detection Engine in Kibana and write/edit detection rules against the data coming from the AD lab.

Running it

Start the stack:
sudo docker-compose up -d

Stop it:
sudo docker-compose down

Restart just Kibana:
sudo docker-compose restart kibana

Check Kibana logs:
sudo docker-compose logs -f kibana

Common issue: password sync

If something's not working, it's often related to the default passwords not syncing properly between Elasticsearch and Kibana. Fix it by resetting the kibana_system password manually:
sudo docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u kibana_system -i

Then update the password in your .env / docker-compose.yml accordingly and restart Kibana.

Note on TLS/keys

Since everything here runs on localhost, I'm not bothering with the certificate/keys setup - not relevant for a local lab like this.