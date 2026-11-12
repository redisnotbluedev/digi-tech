from fast_flights.model import Flights, SingleFlight, Airport, SimpleDatetime, CarbonEmission

[
	Flights(
		type="AA",
		price=2461,
		airlines=["American"],
		flights=[
			SingleFlight(
				from_airport=Airport(
					name="Birmingham-Shuttlesworth International Airport", code="BHM"
				),
				to_airport=Airport(
					name="Charlotte Douglas International Airport", code="CLT"
				),
				departure=SimpleDatetime(date=(2027, 2, 4), time=(13, 19)),
				arrival=SimpleDatetime(date=(2027, 2, 4), time=(15, 51)),
				duration=92,
				plane_type="Embraer 175",
			),
			SingleFlight(
				from_airport=Airport(
					name="Charlotte Douglas International Airport", code="CLT"
				),
				to_airport=Airport(name="LaGuardia Airport", code="LGA"),
				departure=SimpleDatetime(date=(2027, 2, 4), time=(18, 8)),
				arrival=SimpleDatetime(date=(2027, 2, 4), time=(20, 0)),
				duration=112,
				plane_type="Boeing 737",
			),
		],
		carbon=CarbonEmission(typical_on_route=539000, emission=846000),
	),
	Flights(
		type="AA",
		price=2461,
		airlines=["American"],
		flights=[
			SingleFlight(
				from_airport=Airport(
					name="Birmingham-Shuttlesworth International Airport", code="BHM"
				),
				to_airport=Airport(
					name="Charlotte Douglas International Airport", code="CLT"
				),
				departure=SimpleDatetime(date=(2027, 2, 4), time=(18, 3)),
				arrival=SimpleDatetime(date=(2027, 2, 4), time=(20, 44)),
				duration=101,
				plane_type="Canadair RJ 900",
			),
			SingleFlight(
				from_airport=Airport(
					name="Charlotte Douglas International Airport", code="CLT"
				),
				to_airport=Airport(name="LaGuardia Airport", code="LGA"),
				departure=SimpleDatetime(date=(2027, 2, 4), time=(21, 58)),
				arrival=SimpleDatetime(date=(2027, 2, 4), time=(23, 44)),
				duration=106,
				plane_type="Airbus A320",
			),
		],
		carbon=CarbonEmission(typical_on_route=539000, emission=900000),
	),
	Flights(
		type="AA",
		price=2854,
		airlines=["American"],
		flights=[
			SingleFlight(
				from_airport=Airport(
					name="Birmingham-Shuttlesworth International Airport", code="BHM"
				),
				to_airport=Airport(
					name="Charlotte Douglas International Airport", code="CLT"
				),
				departure=SimpleDatetime(date=(2027, 2, 4), time=(8, 39)),
				arrival=SimpleDatetime(date=(2027, 2, 4), time=(11, 20)),
				duration=101,
				plane_type="Canadair RJ 900",
			),
			SingleFlight(
				from_airport=Airport(
					name="Charlotte Douglas International Airport", code="CLT"
				),
				to_airport=Airport(name="LaGuardia Airport", code="LGA"),
				departure=SimpleDatetime(date=(2027, 2, 4), time=(12, 13)),
				arrival=SimpleDatetime(date=(2027, 2, 4), time=(13, 59)),
				duration=106,
				plane_type="Airbus A320",
			),
		],
		carbon=CarbonEmission(typical_on_route=539000, emission=900000),
	),
	Flights(
		type="UA",
		price=3142,
		airlines=["United"],
		flights=[
			SingleFlight(
				from_airport=Airport(
					name="Birmingham-Shuttlesworth International Airport", code="BHM"
				),
				to_airport=Airport(
					name="Chicago O'Hare International Airport", code="ORD"
				),
				departure=SimpleDatetime(date=(2027, 2, 4), time=(7, 0)),
				arrival=SimpleDatetime(date=(2027, 2, 4), time=(9, 37)),
				duration=157,
				plane_type="Embraer 175",
			),
			SingleFlight(
				from_airport=Airport(
					name="Chicago O'Hare International Airport", code="ORD"
				),
				to_airport=Airport(name="LaGuardia Airport", code="LGA"),
				departure=SimpleDatetime(date=(2027, 2, 4), time=(11, 59)),
				arrival=SimpleDatetime(date=(2027, 2, 4), time=(15, 14)),
				duration=135,
				plane_type="Boeing 737",
			),
		],
		carbon=CarbonEmission(typical_on_route=539000, emission=854000),
	),
	Flights(
		type="UA",
		price=3285,
		airlines=["United"],
		flights=[
			SingleFlight(
				from_airport=Airport(
					name="Birmingham-Shuttlesworth International Airport", code="BHM"
				),
				to_airport=Airport(
					name="Chicago O'Hare International Airport", code="ORD"
				),
				departure=SimpleDatetime(date=(2027, 2, 4), time=(7, 0)),
				arrival=SimpleDatetime(date=(2027, 2, 4), time=(9, 37)),
				duration=157,
				plane_type="Embraer 175",
			),
			SingleFlight(
				from_airport=Airport(
					name="Chicago O'Hare International Airport", code="ORD"
				),
				to_airport=Airport(name="LaGuardia Airport", code="LGA"),
				departure=SimpleDatetime(date=(2027, 2, 4), time=(11, 0)),
				arrival=SimpleDatetime(date=(2027, 2, 4), time=(14, 21)),
				duration=141,
				plane_type="Boeing 737",
			),
		],
		carbon=CarbonEmission(typical_on_route=539000, emission=854000),
	),
]
