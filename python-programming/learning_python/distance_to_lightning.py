#!/usr/bin/env python
# by Samuel Huckins


def dist_to_lightning(flash_to_sound_time):
    """
    Calculates the distance to a lightning strike based on the time between
    seeing the lightning flash and hearing the thunder.
    
    flash_to_sound_time -- Time (seconds) from seeing lightning flash to hearing
    thunder.
    """
    speed_of_sound = 1100 # feet/sec
    mile = 5280 # feet
    feet_dist = flash_to_sound_time * speed_of_sound
    mile_dist = (feet_dist / mile)
    if mile_dist < 1:
        print "The lightning struck %0.4f mile from you." % mile_dist
    else:
        print "The lightning struck %0.4f miles from you." % mile_dist

if __name__ == '__main__':
    flash_to_sound_time = float(raw_input("Enter the time in seconds between \
seeing the lightning flash and hearing the thunder: "))
    dist_to_lightning(flash_to_sound_time)
    if raw_input("Press RETURN to exit."):
        sys.exit(0)
