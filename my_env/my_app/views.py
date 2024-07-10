from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime as time
from socket import *
from threading import Thread
from .models import PortScanResult

def home_redirect(request):
    return redirect('port_scan')

def connScan(tgtHost, tgtPort, open_ports, closed_ports):
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        result = sock.connect_ex((tgtHost, tgtPort))
        if result == 0:
            open_ports.append(tgtPort)
        else:
            closed_ports.append(tgtPort)
        sock.close()
    except gaierror:
        pass

def Port_Scan(tgtHost, tgtPorts):
    open_ports = []
    closed_ports = []
    try:
        tgt_IP = gethostbyname(tgtHost)
    except gaierror:
        return [], [], "Oops Error : Please Enter Valid HOST_NAME or IP."

    setdefaulttimeout(2)
    threads = []
    for port in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(port), open_ports, closed_ports))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return open_ports, closed_ports, None

def save_port_scan(host_name, open_ports, closed_ports, start_time, end_time):
    open_ports_str = ' '.join(map(str, open_ports))
    closed_ports_str = ' '.join(map(str, closed_ports))
    result = PortScanResult(
        host_name=host_name,
        open_ports=f"Open: {open_ports_str} | Closed: {closed_ports_str}",
        start_time=start_time,
        end_time=end_time
    )
    result.save()

def port_scan(request):
    tgtHost = request.GET.get('host', None)
    tgtPorts = request.GET.get('ports', None)

    if not tgtHost or not tgtPorts:
        return render(request, 'my_app/results.html', {'error': 'Host and Ports are required'})

    try:
        tgtPorts = [int(port) for port in tgtPorts.split(',')]
    except ValueError:
        return render(request, 'my_app/results.html', {'error': 'Oops Error : Ports must be a comma-separated list of numbers range(1,65535)'})

    start_time = time.now()

    open_ports, closed_ports, error = Port_Scan(tgtHost, tgtPorts)
    end_time = time.now()

    if error:
        return render(request, 'my_app/results.html', {'error': error})

    # Save  scan results in  database
    save_port_scan(tgtHost, open_ports, closed_ports, start_time, end_time)

    context = {
        'target': tgtHost,
        'start_time': start_time,
        'end_time': end_time,
        'open_ports': open_ports,
        'closed_ports': closed_ports,
    }
    return render(request, 'my_app/results.html', context)

