from datetime import datetime, timezone

def parse_datetime(dt_str):
    if dt_str:
        try:
            return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            return dt_str  # fallback to original if parsing fails
    return None

class flight_summary:
    def __init__(self,
                 data
                 ):
        self.data = data

    def get_records(data):

        fr24_id = data.get("fr24_id")
        flight = data.get("flight",None)
        callsign = data.get("callsign",None)
        operating_as = data.get("operating_as",None)
        painted_as = data.get("painted_as",None)
        type = data.get("type",None)
        reg = data.get("reg",None)
        orig_icao = data.get("orig_icao",None)
        orig_iata = data.get("orig_iata",None)
        datetime_takeoff = parse_datetime(data.get("datetime_takeoff",None))
        runway_takeoff = data.get("runway_takeoff",None)
        dest_icao = data.get("dest_icao",None)
        dest_iata = data.get("dest_iata",None)
        dest_icao_actual = data.get("dest_icao_actual",None)
        dest_iata_actual = data.get("dest_iata_actual",None)
        datetime_landed = parse_datetime(data.get("datetime_landed",None))
        runway_landed = data.get("runway_landed",None)
        flight_time = data.get("flight_time",None)
        actual_distance = data.get("actual_distance",None)
        circle_distance = data.get("circle_distance",None)
        hex = data.get("hex",None)
        first_seen = parse_datetime(data.get("first_seen",None))
        last_seen = parse_datetime(data.get("last_seen",None))
        flight_ended = data.get("flight_ended",None)
        updated_at = datetime.now(timezone.utc)
        

        return {
            "fr24_id": fr24_id,
            "flight": flight,
            "callsign": callsign,
            "operating_as": operating_as,
            "painted_as": painted_as,
            "type": type,
            "reg": reg,
            "orig_icao": orig_icao,
            "orig_iata": orig_iata,
            "datetime_takeoff": datetime_takeoff,
            "runway_takeoff": runway_takeoff,
            "dest_icao": dest_icao,
            "dest_iata": dest_iata,
            "dest_icao_actual": dest_icao_actual,
            "dest_iata_actual": dest_iata_actual,
            "datetime_landed": datetime_landed,
            "runway_landed": runway_landed,
            "flight_time": flight_time,
            "actual_distance": actual_distance,
            "circle_distance": circle_distance,
            "hex": hex,
            "first_seen": first_seen,
            "last_seen": last_seen,
            "flight_ended": flight_ended,
            "updated_at": updated_at
        }
