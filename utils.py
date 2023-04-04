import math
import vpython as vp

def distance(a, b) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)

def check_port(port: int) -> str or None:
    if port < 1_000 or port > 65_535:
        return "Port must be between 1,000 and 65,535"
    
def lerp(start: vp.vector, end: vp.vector, t: float):
    return (1 - t) * start + t * end