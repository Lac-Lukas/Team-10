#graphics path
GRAPHICS_PATH = "../graphics/Enemies/"

Minotaur_dict = {
	#enemy stats
	"max_health" : 15,
	"attack_dmg" : 15,
	"attack_dist" : 100,
	"attack_cooldown" : 600,
	"aggro_dist" : 400,
	"mvmt_speed" : 3,
    "damage_frame" : 2,
    "xp_drop" : 20,
    "gold_drop" : 10,
	#sprite variables
	"idle_frames" : [],
	"running_frames" : [],
	"death_frames" : [],
	"attack_frames" : [],
	"take_dmg_frames" : [],
	"num_idle_frames" : 5,
	"num_running_frames" : 8,
	"num_death_frames" : 6,
	"num_attack_frames" : 9,
    "num_take_damage_frames" : 2,
	"scale" : 3,
    #alternative attack mode
	"spin_attack" : [],
	"health_trigger" : 7,
    "aggro_range_gain" : 600,
    "speed_gain" : 1
}

Skeleton_dict = {
	#enemy stats
	"max_health" : 4,
	"attack_dmg" : 10,
	"attack_dist" : 100,
	"attack_cooldown" : 1000,
	"aggro_dist" : 400,
	"mvmt_speed" : 2,
    "damage_frame" : 6,
    "xp_drop" : 10,
    "gold_drop" : 5,
	#sprite variables
	"idle_frames" : [],
	"running_frames" : [],
	"death_frames" : [],
	"attack_frames" : [],
	"take_dmg_frames" : [],
	"num_idle_frames" : 4,
	"num_running_frames" : 4,
	"num_death_frames" : 4,
	"num_attack_frames" : 8,
    "num_take_damage_frames" : 5,
	"scale" : 2
}

Mushroom_dict = {
	#enemy stats
	"max_health" : 5,
	"attack_dmg" : 5,
	"attack_dist" : 120,
	"attack_cooldown" : 1500,
	"aggro_dist" : 600,
	"mvmt_speed" : 3,
    "damage_frame" : 6,
    "xp_drop" : 20,
    "gold_drop" : 10,
	#sprite variables
	"idle_frames" : [],
	"running_frames" : [],
	"death_frames" : [],
	"attack_frames" : [],
	"take_dmg_frames" : [],
	"num_idle_frames" : 4,
	"num_running_frames" : 8,
	"num_death_frames" : 4,
	"num_attack_frames" : 8,
    "num_take_damage_frames" : 5,
	"scale" : 2
}

Flyingeye_dict = {
	#enemy stats
	"max_health" : 2,
	"attack_dmg" : 7,
	"attack_dist" : 80,
	"attack_cooldown" : 500,
	"aggro_dist" : 800,
	"mvmt_speed" : 6,
    "damage_frame" : 6,
    "xp_drop" : 5,
    "gold_drop" : 10,
	#sprite variables
	"idle_frames" : [],
	"running_frames" : [],
	"death_frames" : [],
	"attack_frames" : [],
	"take_dmg_frames" : [],
	"num_idle_frames" : 8,
	"num_running_frames" : 8,
	"num_death_frames" : 4,
	"num_attack_frames" : 8,
    "num_take_damage_frames" : 5,
	"scale" : 2
}

Enemies_dict = {
    "Minotaur" : Minotaur_dict,
    "Skeleton" : Skeleton_dict,
    "Mushroom" : Mushroom_dict,
    "Flying Eye" : Flyingeye_dict
}