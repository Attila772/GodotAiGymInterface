extends Button

var timer =1
# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	
	if(timer<0):
		get_parent().get_node("Label").text = str(SharedMemoryTcp.counter)
		get_parent().get_node("Label2").text = str(SharedMemoryTcp.json)
		timer = 1
	else:
		timer-=delta
	pass


func _on_Button_pressed():
	SharedMemoryTcp.send_all()
	pass # Replace with function body.
