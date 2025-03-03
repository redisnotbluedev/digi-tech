from microbit import *

day_limits = (0, 4)
equipment_limits = (0, 2)

day_index = 0
equipment_index = 0
state = "days"

equipment = {
    "90009:99099:90909:90009:90009": [
        Image("99999:90509:95559:90509:99999"),
        Image("09000:99900:09599:00000:00999"),
        Image("99099:99999:09990:09990:00000"),
        Image("05950:09090:09590:09590:09990"),
        Image("90900:90900:90090:90009:99999"),
        Image("00900:99999:90909:99999:00900"),
        Image("99999:90009:92229:90009:99999")
    ],
    "99900:09000:09909:00909:00999": [
        Image("99999:90059:90059:90059:99999"),
        Image("00000:05900:09990:00950:00000"),
        Image("99099:99999:09990:09990:00000"),
        Image("05950:09090:09590:09590:09990"),
        Image("90900:90900:90090:90009:99999"),
        Image("00900:99999:90909:99999:00900"),
        Image("99999:90009:92229:90009:99999")
    ],
    "90009:90009:90909:99099:90009": [
        Image("00900:99999:90909:99999:00900"),
        Image("99999:90009:92229:90009:99999"),
        Image("99999:90509:95559:90509:99999"),
        Image("09000:99900:09599:00000:00999"),
        Image("99999:90059:90059:90059:99999"),
        Image("00000:05900:09990:00950:00000")
    ],
    "99900:09000:09909:00999:00909": [
        Image("99099:99999:09990:09990:00000"),
        Image("05950:09090:09590:09590:09990"),
        Image("90900:90900:90090:90009:99999"),
        Image("99999:90059:90059:90059:99999"),
        Image("00000:05900:09990:00950:00000"),
        Image("99999:90509:95559:90509:99999"),
        Image("09000:99900:09599:00000:00999")
    ],
    "09990:09000:09990:09000:09000": [
        Image("99999:90059:90059:90059:99999"),
        Image("00000:05900:09990:00950:00000"),
        Image("99099:99999:09990:09990:00000"),
        Image("05950:09090:09590:09590:09990"),
        Image("90900:90900:90090:90009:99999"),
        Image("00900:99999:90909:99999:00900"),
        Image("99999:90009:92229:90009:99999")
    ]
}

def move_left():
    global day_index
    global equipment_index
    global day_limits
    global equipment_limits
    
    if state == "days":
        if day_index == day_limits[0]:
            day_index = day_limits[1]
        else:
            day_index += -1
    elif state == "equipment":
        if equipment_index == equipment_limits[0]:
            equipment_index = equipment_limits[1]
        else:
            equipment_index += -1

def move_right():
    global day_index
    global equipment_index
    global day_limits
    global equipment_limits
    
    if state == "days":
        if day_index == day_limits[1]:
            day_index = day_limits[0]
        else:
            day_index += 1
    elif state == "equipment":
        if equipment_index == equipment_limits[1]:
            equipment_index = equipment_limits[0]
        else:
            equipment_index += 1

def switch_focus():
    global state
    
    if state == "days":
        state = "equipment"
    elif state == "equipment":
        state = "days"

while True:
    # Handle input
    b_pressed = button_b.was_pressed()
    if button_a.was_pressed():
        if b_pressed:
            switch_focus()
        else:
            move_left()
    elif b_pressed:
        move_right()

    if state == "days":
        display.show(Image(list(equipment.keys())[day_index]))
    elif state == "equipment":
        display.show(equipment[list(equipment.keys())[day_index]][equipment_index])