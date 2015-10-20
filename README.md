# gproxy carbon proxy
This is my very first piece of python code. 
Admittedly taken from some howto's and bits and pieces of other code and a little made up myself.

By no means am I a coder so use at your own risk. I do however love to hack things together bubblebum 
and ticky tape style. I had a need to push data to a public cloud server I am hosting and could not find 
anything that could help me do so securely when I am originating from dynamic IP ranges.

So I hacked this together.
It's effectively a small python daemon that listens on a given port (default 5000)

It accepts data via HTTP 
e.g. curl -X POST -u admin:password http:/www.server.com:5000/upload --data "data=Usage.MyData.count 25 1445366268"

It then sends that data to the same host running Graphite and Carbon to the Carbon port (default 2300)

It logs the incoming submission in /var/log/gproxy.log 
You can check for failed requests and add a further level of IDS type security with fail2ban for instance to 
help prevent brute force attacks on the gproxy python daemon.

Installation
It requires some python modules to be installed.
pip install Flask
pip install flup
pip install WSGIServer

Configuration
Edit the gproxy.py and change your username and password from default admin and password.
Edit HOST = 'localhost' and PORT = 2003 to your own Carbon IP and Port 
Remember to bind Carbon to localhost or firewall it out else you defaut the object.
Edit app.run(host='0.0.0.0', port=5000) to the IP and Port you would like your gproxy to bind to.

And that should be it.
Hope you find this useful.





