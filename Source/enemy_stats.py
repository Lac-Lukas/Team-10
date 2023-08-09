#graphics path
GRAPHICS_PATH = "../graphics/Enemies/"

Minotaur_dict = {
	#enemy stats
	"max_health" : 4,
	"attack_dmg" : 10,
	"attack_dist" : 100,
	"attack_cooldown" : 600,
	"aggro_dist" : 300,
	"mvmt_speed" : 3,
	#sprite variables
	"idle_frames" : [],
	"running_frames" : [],
	"death_frames" : [],
	"attack_frames" : [],
	"num_idle_frames" : 5,
	"num_running_frames" : 8,
	"num_death_frames" : 6,
	"num_attack_frames" : 9,
}

Skeleton_dict = {
	#enemy stats
	"max_health" : 2,
	"attack_dmg" : 5,
	"attack_dist" : 100,
	"attack_cooldown" : 1000,
	"aggro_dist" : 400,
	"mvmt_speed" : 2,
	#sprite variables
	"idle_frames" : [],
	"running_frames" : [],
	"death_frames" : [],
	"attack_frames" : [],
	"num_idle_frames" : 4,
	"num_running_frames" : 4,
	"num_death_frames" : 4,
	"num_attack_frames" : 8,
}

Enemies_dict = {
    "Minotaur" : Minotaur_dict,
    "Skeleton" : Skeleton_dict
}