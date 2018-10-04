from luna_touch import helpers, _const

class Touch(object):
     
    def __init__ ( self, center_of_mass, area ):
        
        self.id = 0

        self.position = tuple(map(int, center_of_mass))
        self.delta_position = ( 0 , 0 ) 
        
        self.area = area
        self.radius = int(helpers.get_circle_radius( area ))

        
        self.state = _const.TOUCH_STATE_BEGAN
        
        self.frames_missing = 0

        self.timestamp = helpers.timestamp_in_milliseconds()
        self.delta_time = 0

    
    def __str__(self):

        return str({"id": self.id, "pos": self.position, "state":self.state, "frames_missing":self.frames_missing}) 

    def __repr__(self):
        states = [ "undefinded", "Began", "Ended", "Still", "Moved", "Missing"]
        return str({"id": self.id, "pos": self.position, "state": states[self.state], "frames_missing":self.frames_missing} )


