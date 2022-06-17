extends Node
var client : StreamPeerTCP
var wrapped_client : PacketPeerStream
var connected = false
var should_connect = false
var SharedTcpDataDict : Dictionary

# Called when the node enters the scene tree for the first time.
func _ready():
	client = StreamPeerTCP.new()
	client.set_no_delay(true)
	pass # Replace with function body.

func _process(delta):
	if should_connect and not connected:
		pass
	if connected and not client.is_connected_to_host():
		connected = false
	if client.is_connected_to_host():
		synchronise()
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass

func connect_to_server(timeout_seconds):
	set_process(true)
	should_connect = true
	var ip = "127.0.0.1"
	var port = 8080
	var connect = client.connect_to_host(ip, port)
	if client.is_connected_to_host():
		connected = true
		wrapped_client = PacketPeerStream.new()
		wrapped_client.set_stream_peer(client)
	

func disconnect_from_server():
	client.disconnect_from_host()


func synchronise():	
	while client.get_available_bytes() > 0:
		print(client.get_string(client.get_available_bytes()))
		var msg = client.get_string(client.get_available_bytes())
		var split = msg.split(",")
		var command = split[0]
		var key = split[1]
		var value = split[2]
		match command:
			"cmd":
				pass
			"set":
				var parsed = parse_value(split)
				SharedTcpDataDict[key] = parsed
			
		print(msg)
		var error = wrapped_client.get_packet_error()
		if msg == null:
			continue;
		
		
func send_var(msg):
	if client.is_connected_to_host():
		print(msg)
		wrapped_client.put_var(msg)
		
func convert_str_to_array(string):
	pass

func parse_value(split):
	var typetmp = typeof(SharedTcpDataDict[split[1]])
	match typetmp:
					TYPE_NIL:
						return null
					TYPE_BOOL:
						return bool(split[2])
					TYPE_INT:
						return int(split[2])
					TYPE_REAL:
						return float(split[2])
					TYPE_STRING:
						return str(split[2])
					TYPE_ARRAY:
						return convert_str_to_array(split[2])
