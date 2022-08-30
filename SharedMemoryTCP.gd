extends Node
var client : StreamPeerTCP
var wrapped_client : PacketPeerStream
var connected = false
var should_connect = false
var SharedTcpDataDict : Dictionary
var counter = 0
var json


func _ready():
	client = StreamPeerTCP.new()
	client.set_no_delay(true)
	connect_to_server(5)
	pass 

func _process(delta):
	if should_connect and not connected:
		pass
	if connected and not client.is_connected_to_host():
		connected = false
	if client.is_connected_to_host():
		synchronise()


func connect_to_server(timeout_seconds):
	set_process(true)
	should_connect = true
	var ip = "127.0.0.1"
	var port = 8000
	var connect = client.connect_to_host(ip, port)
	
	if client.is_connected_to_host():
		connected = true
		wrapped_client = PacketPeerStream.new()
		wrapped_client.set_stream_peer(client)
	

func disconnect_from_server():
	client.disconnect_from_host()


func synchronise():	
	while client.get_available_bytes() > 0:
		counter+=1
		var rcv = client.get_available_bytes()
		var str_rcv = client.get_string(rcv)
		var data = null
		
		if(str_rcv.split("}{").size()>1):
			
			data = JSON.parse(str_rcv.split("}{")[0]+"}")
		else:
			data = JSON.parse(str_rcv)
		
		if(data.result != null):
			json = data.result["tensor"]
		
		
			
func send_test_data():
			send_var("set-"+str(SharedTcpDataDict.keys()[0])+"-"+str(SharedTcpDataDict[SharedTcpDataDict.keys()[0]]) )

func send_all():
	for key in SharedTcpDataDict:
		var msg = "set-" + key + "-"+ str(SharedTcpDataDict[key]) 
		send_var(msg)

		
		pass
		
		
func send_var(msg):
	if client.is_connected_to_host():
		wrapped_client.put_var(msg)
		
func convert_str_to_array(string):
	string = string.replace("[","").replace("]","").replace("}","").replace("{","")
	var split = string.split(",")
	var parsed = []
	var key =""
	for a in split:
		if len(a.split(":"))>1:
			key = a.split(":")[0]
			key = key.replace(" ","")
			key = key.replace("\'","")
			var val = a.split(":")[1]
			
			val = val.replace(" ","")
			SharedTcpDataDict[key] =[]
			SharedTcpDataDict[key].append(val)
		else:
			SharedTcpDataDict[key].append(a)
	return
	pass
