class StopwatchMeta(type):
    _instance = None
    _instances = {}

    def __new__(cls, name, bases, dct):
        dct.setdefault('game_id', '')
        dct.setdefault('game_title', '')
        dct.setdefault('start_time', '')
        dct.setdefault('end_time', '')
        dct.setdefault('duration', 0)
        return super().__new__(cls, name, bases, dct)
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
class Stopwatch(metaclass=StopwatchMeta):
    # pass

    def __init__(self):
        pass

    def __str__(self):
        return f"Stopwatcch(game_id={self.game_id}, game_title={self.game_title}, start_time={self.start_time}, end_time={self.end_time}, duration={self.duration})"
    
    def __repr__(self):
        return f"Stopwatcch(game_id={self.game_id}, game_title={self.game_title}, start_time={self.start_time}, end_time={self.end_time}, duration={self.duration})"
    
    def to_dict(self):
        return {
            'game_id': self.game_id,
            'game_title': self.game_title,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
        }
    
    def clear(self):
        # self = None
        self.game_id = None
        self.game_title = None
        self.start_time = None
        self.end_time = None
        self.duration = None