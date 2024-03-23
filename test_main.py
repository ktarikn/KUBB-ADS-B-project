from PlaneData import PlaneData
import numpy as np


plane_instance = PlaneData("471f8f", "WZZ4641", "1710933062", "27.623", "40.4816", "False", "239.4", "158.18", "0")


def test_isInit_correct():
    assert (plane_instance.location_history[plane_instance.idx][1] =="27.623")

def test_is_update_functioning():
    plane_instance.update_data(longitude="28.000",latitude="40.4800",on_ground="False",true_track="160.00",velocity="300") #a change is made
    assert (plane_instance.location_history[plane_instance.idx][1] =="28.000")
