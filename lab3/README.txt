Aircraft 6 10 -> MaintenanceTechnician, MaintenanceLog, FuelRecord, Flight
Airline 8 14 -> Aircraft, Flight, LoyaltyProgram, FlightAttendant
FlightSchedule 4 9 -> Flight
Flight 13 16 -> Passenger, Route, FlightSchedule, Aircraft, Airline, Gate, BoardingPass, Pilot, FlightAttendant
Route 4 10 -> Airport
Airport 6 11 -> Terminal, Gate, GroundStaff, Flight
Elevator 7 11 -> 
Escalator 6 11 ->
Gate 7 12 -> Terminal, GroundStaff, Flight
Kiosk 6 11 -> 
Lounge 7 11 -> 
ParkingLot 6 11 -> 
Restaurant 7 12 -> Terminal
Restroom 6 10 -> 
RetailShop 7 13 -> Terminal
Runway 6 12 -> 
ShuttleBus 7 11 -> 
Terminal 4 9 -> Gate, GroundStaff
BoardingPass 5 8 -> Ticket, Passenger
BoardingProcedure 4 9 -> Flight, Passenger
CargoManifest 4 7 -> 
CheckInDesk 6 11 -> Passenger, Terminal
CustomDeclaration 5 7 -> Passenger
EmergencyProtocol 8 8 -> 
FlightPlan 6 7 -> Route, Aircraft
FuelRecord 5 7 -> Aircraft
IncidentReport 8 8 -> 
LostAndFoundReport 7 5 -> Restroom
MaintenanceLog 7 5 -> Aircraft, MaintenanceTechnician
SecurityCheck 6 8 -> Passenger
VisaControl 4 6 -> Passenger, Visa
WeatherReport 8 7 -> Aircraft, Runway
SpecialAssistanceRequest 6 7 -> Passenger
Baggage 6 8 -> Passenger
LoyaltyProgram 6 6 -> 
Passenger 7 21 -> Passenger, Ticket, Baggage, Visa, LoyaltyProgram
Passport 5 9 -> 
Ticket 7 8 -> Flight, Passenger
Visa 5 6 -> Passenger
AirTrafficController 4 9 -> Flight
BaggageHandler 4 12 -> Baggage
CleaningCrew 5 7 -> ReInvalidPassportExceptionstroom, Lounge
CrewSchedule 4 7 ->  Pilot, Flight, FlightAttendant
CustomsOfficer 5 10 -> Passenger
Dispatcher 6 11 -> Flight
FlightAttendant 4 9 -> Flight
GroundStaff 7 9 -> Airport, Gate, Lounge, Restroom, Flight
MaintenanceTechnician 5 7 -> Aircraft
Pilot 7 10 -> Flight, Aircraft
SecurityOfficer 7 10 -> Passenger

Исключения(12):
UnauthorizedAircraftAccessException 0 0 -> 
OverweightBaggageException 0 0 -> 
InvalidBoardingPassException 0 0 ->
FlightOverbookedException 0 0 ->
GateConflictException 0 0 ->
FlightCapacityExceededException 0 0 ->
InvalidPassportException 0 0 ->
DuplicatePassengerException 0 0 ->
SecurityFlaggedException 0 0 ->
TicketAlreadyCheckedInException 0 0 ->
InvalidTicketException 0 0 ->
InvalidVisaException 0 0 ->

Поля: 300
Поведения: 473
Исключения: 12