from fast_flights import (
 	FlightQuery,
 	Passengers,
 	create_query,
 	get_flights
)

query = create_query(
 	flights=[
 	 	FlightQuery(
 	 	 	date="2027-1-1",
 	 	 	from_airport="MYJ",
 	 	 	to_airport="TPE",
 	 	),
 	],
 	seat="economy",
 	trip="one-way",
 	passengers=Passengers(infants_in_seat=1),
 	language="en-US",
)
res = get_flights(query)
print(res)
