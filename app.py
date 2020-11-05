class DescentCalculator:
    
    def __init__(self, start_alt, dest_alt, kias, distance_nm):
        self.start_alt = start_alt
        self.dest_alt = dest_alt
        self.kias = kias
        self.distance_nm = distance_nm
        self.descent_angle = 3
        self.descent_required_min = int(self._fpm_descent_min())
        self.fpm_with_speed = int(self._fpm_distance_and_speed())
        self.statement_min_fpm = self._statement_min_fpm_required()
        self.statement_fpm_with_speed = self._statement_fpm_with_speed()
        
    
    def _required_distance(self):
        """
        Returns how many nm from the dest_alt the descent must begin
        Descent rate is 3 degrees according to online sources
        """
        descent_degrees = 3
        return (((self.start_alt - self.dest_alt)/100)/descent_degrees)
    
    def _kts_per_minute(self):
        return self.kias / 60
    
    def _fpm_descent_fixed_angle(self):
        return self.descent_angle * self._kts_per_minute() * 100
    
    def _fpm_descent_min(self):
        return (self.start_alt - self.dest_alt)/self.distance_nm
    
    def _time_to_travel_d(self):
        return self.distance_nm / self.kias
    
    def _fpm_distance_and_speed(self):
        feet_per_nm = (self.start_alt - self.dest_alt) / self.distance_nm
        descent_angle_varying = (feet_per_nm/100)
        descent_fpm = descent_angle_varying * self._kts_per_minute() * 100
        return descent_fpm
    
    def _statement_min_fpm_required(self):
        return f"From {self.start_alt}ft to {self.dest_alt}ft ({self.dest_alt-self.start_alt}ft) over {self.distance_nm}nm requires a minimum descent of {self.descent_required_min} fpm"
    
    def _statement_fpm_with_speed(self):
        return f"From {self.start_alt}ft to {self.dest_alt}ft ({self.dest_alt-self.start_alt}ft) over {self.distance_nm}nm travelling at {self.kias} kias requires a descent of {self.fpm_with_speed} fpm"
    
    def print_statements(self):
        print(self._statement_min_fpm_required())
        print(self._statement_fpm_with_speed())

x = DescentCalculator(start_alt=6000, dest_alt=3000, kias=230, distance_nm=7 )

print(x.print_statements())