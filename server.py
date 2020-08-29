import socket
import time
import pickle
import solution
import pkr_range
from interface import get_window_list

host = '192.168.1.220' #Server ip
port = 4000
buf_size = 16384
header_size = 16

def make_header(size):
    encoded = str(size).encode('utf-8')
    return b'0' * (header_size - len(encoded)) + encoded

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()
comm_sock = s.accept()[0]
comm_sock.setblocking(0)

solvers = [solution.Solver(0, window[0], window[1], window[2][0], window[2][1])
    for window in get_window_list() if 'Untitled - GTO' in window[1]]


    
'''
Message Parsing:

!!!: End of message
#: Parameter Seperator

Create Solve:   solve#{solver_id}#{oop_range}#{ip_range}#{board}#{pot_size}#{stack_size}#{profile}!!!
Get Ranges:     get#{solver_id}#{is_oop}#{facing}#{action}!!!
Reset:          reset#{solver_id}!!!
Status Check:   status#{solver_id}!!!
'''

while True:
    message = b''
    requests = []
    size = None

    try: 
        size = int(comm_sock.recv(header_size).decode('utf-8'))
    except BlockingIOError:
        pass

    if size:
        while len(message) < size:
            try:
                data = comm_sock.recv(buf_size)
                print(data)
                message += data
            except BlockingIOError:
                pass
    
    if len(message) > 0:
        requests = pickle.loads(message)

    while len(requests) != 0:
        if requests[0] == 'solve':
            oop_range = pkr_range.PkrRange()
            oop_range.list_to_range(pickle.loads(requests[2]))
            ip_range = pkr_range.PkrRange()
            ip_range.list_to_range(pickle.loads(requests[3]))

            solvers[int(requests[1])].create_solve(
                oop_range,
                ip_range,
                requests[4],
                requests[5],
                requests[6],
                requests[7],
            )
            del requests[0:8]
        
        elif requests[0] == 'get':
            if solvers[int(requests[1])].status == 'ready':
                ranges = solvers[int(requests[1])].get_ranges(
                    bool(requests[2]), requests[3], requests[4]
                )
                resp = [ranges, requests[5], requests[1]]
                pickeled = pickle.dumps(resp)
                comm_sock.send(make_header(len(pickeled)))
                comm_sock.send(pickeled)
            elif solvers[int(requests[1])].status == 'solving':
                solvers[int(requests[1])].queue.append((
                    bool(requests[2]),
                    requests[3],
                    requests[4],
                    requests[5],
                ))
            else:
                print("Invalid Get Ranges request.")
            del requests[0:6]

        elif requests[0] == 'reset':
            solvers[int(requests[1])].reset()
            del requests[0:2]
            
    for solver in solvers:
        if solver.status == 'solving':
            if solver.done_solving():
                for request in solver.queue:
                    ranges = solver.get_ranges(
                        request[0],
                        request[1],
                        request[2]
                    )
                    resp = [ranges, request[3], solver.id]
                    pickeled = pickle.dumps(resp)
                    comm_sock.send(make_header(len(pickeled)))
                    comm_sock.send(pickeled)
    #con.send(data.encode('utf-8'))
comm_sock.close()
