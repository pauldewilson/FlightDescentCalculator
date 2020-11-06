from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import IntegerField, SubmitField


class DescentCalculator:

    def __init__(self, start_alt=None, dest_alt=None, kias=None, distance_nm=None):
        self.start_alt = start_alt
        self.dest_alt = dest_alt
        self.kias = kias
        self.distance_nm = distance_nm
        self.descent_angle = 3
        self.descent_required_min = None
        self.fpm_with_speed = None
        self.statement_min_fpm = None
        self.statement_fpm_with_speed = None

    def _required_distance(self):
        """
        Returns how many nm from the dest_alt the descent must begin
        Descent rate is 3 degrees according to online sources
        """
        descent_degrees = 3
        return (((self.start_alt - self.dest_alt)/100)/descent_degrees)

    def run(self):
        self._fpm_distance_and_speed()
        self._statement_min_fpm_required()
        self._statement_fpm_with_speed()

    def _kts_per_minute(self):
        return self.kias / 60

    def _fpm_descent_fixed_angle(self):
        return self.descent_angle * self._kts_per_minute() * 100

    def _fpm_descent_min(self):
        self.descent_required_min = (self.start_alt - self.dest_alt)/self.distance_nm

    def _time_to_travel_d(self):
        return self.distance_nm / self.kias

    def _fpm_distance_and_speed(self):
        try:
            feet_per_nm = (self.start_alt - self.dest_alt) / self.distance_nm
            descent_angle_varying = (feet_per_nm/100)
            descent_fpm = descent_angle_varying * self._kts_per_minute() * 100
            self.fpm_with_speed = descent_fpm
        except:
            print("#DIV/0! POSITION1")
            self.fpm_with_speed = 0


    def _statement_min_fpm_required(self):
        self.statement_min_fpm = f"{self.dest_alt-self.start_alt}ft over {self.distance_nm}nm requires a minimum descent of {self.descent_required_min} fpm"

    def _statement_fpm_with_speed(self):
        self.statement_fpm_with_speed = f"{self.dest_alt-self.start_alt}ft over {self.distance_nm}nm at {self.kias} kias requires a descent of {self.fpm_with_speed} fpm"

    def print_statements(self):
        print(self._statement_min_fpm_required())
        print(self._statement_fpm_with_speed())


class DescentForm(FlaskForm):
    alt_start = IntegerField(validators=[DataRequired()], label="Altitude Start", render_kw={"placeholder": "Start Altitude (feet)"})
    alt_end = IntegerField(validators=[DataRequired()], label="Altitude End", render_kw={"placeholder": "End Altitude (feet)"})
    kias = IntegerField(validators=[DataRequired()], label="KIAS", render_kw={"placeholder": "KIAS"})
    distance_nm = IntegerField(validators=[DataRequired()], label="Distance nm", render_kw={"placeholder": "Nautical Miles"})
    submit = SubmitField(label="Calculate")
