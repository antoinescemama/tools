# HTTP-Requester
Fuzzing tool for HTTP Request

Python scripts which parse an HTTP request, then process it by using another file (typically a password file) and then sending the request.
Typical use case is brute forcing username/password. 

Request has to be given as argument. Optionnally the request can be sent via a proxy (test with burp), and the number of thread can be changed.
The password file and process can easely be changed in the source.

Python3 is required.

ex:  python3 ./Requester.py -f request4  -p 8080 -t 5

