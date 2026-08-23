File configuration for the elk siem
I enabled xpack security in order to use the Detection engine on the siem.
In that matter i'll be able to edit detection rules.

Launched docker with : 
- sudo docker-compose up -d

Turn it down with :
- sudo docker-compose down

Restart kibana service :
- sudo docker-compose restart kibana

Check logs : 
- sudo docker-compose logs -f kibana

If you encoutered an error, it might be related to a default password synchronization.
To reset password manually :
- sudo docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u kibana_system -i

As i'm working on localhost usage, the keys section are not relevant
