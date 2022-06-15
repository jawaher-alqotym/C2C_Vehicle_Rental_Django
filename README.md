# C2C_Vehicle_Rental_Django

[Idea](https://github.com/jawaher-alqotym/C2C_Car_Rental_Django/blob/main/README.md#idea "Idea")

[Inspiration](https://github.com/jawaher-alqotym/C2C_Car_Rental_Django/blob/main/README.md#inspiration "Inspiration")

[Impact&Challenges](https://github.com/jawaher-alqotym/C2C_Car_Rental_Django/blob/main/README.md#project-impact-and-challenges "Impact&Challenges")

[Services&Features](https://github.com/jawaher-alqotym/C2C_Car_Rental_Django/blob/main/README.md#list-of-services--features "Services&Features")

[User Stories](https://github.com/jawaher-alqotym/C2C_Car_Rental_Django/blob/main/README.md#user-stories "User Stories")
## Idea:
A platform to facilitate renting cars for both vehicle owners and vehicle rentee. The system will help users find a vehicle to rent directly from the vehicle owner without a “middle-man” and allow anyone with a vehicle to further benefit from it and generate an additional income by putting it up for rent.

## Inspiration:
Facilitate the renting process while reducing vehicle renting costs. Also, the C2C vehicle rental business model is not represented enough(if at all) in KSA.

## Project Impact and challenges:
The project helps reduce vehicle renting costs and gas costs for users(the person who rents the vehicle will pay for the gas). Although the idea is promising it has some weaknesses like authenticating the vehicle owner and vehicle rentee. Not many people would be happy to see strangers drive their vehicle without being sure of their identity and people are reluctant to pay without a guarantee of the existence of that vehicle. However, we can get around these weaknesses by requiring both parties to register an account to establish some credentials and provide a personal page for both with reviews.

## List of Services / Features:
- Manage renting vehicle.
- Manage offering vehicle for rent process.
- Reviewing the vehicle/vehicle rentee after renting process.


## User Stories
- Type of users: vehicle owner, vehicle rentee, and admin.

### Vehicle Owner
#### Role: offer their car for rent.
- Create, Read, Update, Delete Vehicle.
- Create, Read, Update, and Delete reviews they wrote about the people who rented their vehicle.
- Read, and delete a rent request.
- Register.


### Vehicle Rentee
#### Role: view and rent cars.
- View cars for rent.
- Create, Read, and delete a rent request.
- Create, Read, Update, and Delete reviews they wrote about the vehicle owner/ the vehicle.
- Register.

### Admin
#### Role: grant and revoke permissions.
- Read, update, and delete Vehicle. 
- Read rent request.
- Read, update, and delete users.
