from datetime import datetime, timedelta
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.request import Request
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes

from users_app.models import UserCredential

# an unregistered user services
@api_view(['GET'])
def list_vehicles(request : Request):
    '''
    this method list all the Vehicles in the database
    :param: request
    :return: dataResponse
    '''
    vehicles = Vehicle.objects.all()

    dataResponse = {
        "msg" : "List of All vehicles",
        "cities" : VehicleSerializer(instance=vehicles, many=True).data
    }

    return Response(dataResponse)

@api_view(['GET'])
def list_reviews_about_user(request : Request, user_id):
    '''
    this method list all reviews written about a user, whether being a vehicle owner or a rentee
    :param user_id: request, a positive integer
    :return: list of reviews objects
    '''
    user = User.objects.get(id=user_id)
    user_credential = UserCredential.objects.get(user=user)
    reviews = Reviwes.objects.filter(about=user_credential)

    dataResponse = {
        "msg" : f"List of All reviews about {user.first_name} {user.last_name}",
        "reviews" : ReviwesSerializer(instance=reviews, many=True).data
    }

    return Response(dataResponse, status = status.HTTP_200_OK)


# A registered user services

# Vehicles
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_vehicle(request : Request):
    '''
     this method for adding a vehicle if and only if
     the user is: registered and has credentials and is logged in.
    :param request: request
    :return: dataResponse
    '''
    if request.user.is_authenticated:
     user = User.objects.get(id=request.user.id)
     user_credential = UserCredential.objects.get(user=user)

     new_vehicle = VehicleSerializer(instance= Vehicle(owner=user_credential), data=request.data)

     if new_vehicle.is_valid():
        new_vehicle.save()
        print(request.data)
        dataResponse = {
            "msg" : "Your vehicle added Successfully",
            "owner": f"{user_credential}",
            "vehicle" : new_vehicle.data
        }
        return Response(dataResponse)
     else:
        print(new_vehicle.errors)
        dataResponse = {"msg" : "couldn't add a vehicle"}
        return Response( dataResponse, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"msg": "Login first then add a vehicle"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
def update_vehicle(request : Request, vehicle_id):
    '''
    this method for updating a vehicle, and it is only allowed to do so
     if the user is: the owner of the vehicle and logged in
    :param: request, a positive integers
    :return: dataResponse
    '''
    if request.user.is_authenticated:
     user = User.objects.get(id=request.user.id)
     user_credential = UserCredential.objects.get(user=user)
     print(user_credential)
     try:
         vehicle = Vehicle.objects.get(owner=user_credential, id=vehicle_id)
         print(vehicle)
     except Exception as e:
         print(e)
         return Response({"msg" : "This is not yours to alter"}, status=status.HTTP_401_UNAUTHORIZED)

     update_vehicle = VehicleSerializer(instance=vehicle, data=request.data)


     if update_vehicle.is_valid():
        update_vehicle.save()
        dataResponse = {
            "msg" : "Your vehicle updated Successfully",
            "vehicle" : update_vehicle.data
        }
        return Response(dataResponse)
     else:
        print(update_vehicle.errors)
        dataResponse = {"msg" : "couldn't update your vehicle"}
        return Response( dataResponse, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"msg": "Login first then update your vehicle"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_vehicle(request : Request, vehicle_id):
    '''
     this method takes a vehicle id and deletes the vehicle if the user owns it
    :param vehicle_id: request, and a positive integer
    :return: dataResponse
    '''

    if request.user.is_authenticated:
     user = User.objects.get(id=request.user.id)
     user_credential = UserCredential.objects.get(user=user)

     try:
      vehicle = Vehicle.objects.get(owner=user_credential, id=vehicle_id)
      vehicle.delete()
     except Exception as e:
         return Response({"msg": f"Can not delete this vehicle {e}"}, status=status.HTTP_400_BAD_REQUEST)

     return Response({"msg": "Deleted Successfully"},status=status.HTTP_200_OK)

    else:
       dataResponse = {"msg": "couldn't delete this vehicle"}
       return Response(dataResponse, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def list_my_vehicles(request : Request):
    '''
     this method list all vehicles owned by the logded in user
    :param: request
    :return: dataResponse
    '''
    if request.user.is_authenticated:
     user = User.objects.get(id=request.user.id)
     user_credential = UserCredential.objects.get(user=user)
     vehicles = Vehicle.objects.filter(owner=user_credential)

     dataResponse = {
        "msg" : "List of All vehicles",
        "Vehicles" : VehicleSerializer(instance=vehicles, many=True).data
     }
     return Response(dataResponse)
    else:
        dataResponse = {"msg": "couldn't get this user vehicle"}
        return Response(dataResponse, status=status.HTTP_401_UNAUTHORIZED)


# Reviews
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_review(request : Request, user_id):
    '''
    this method for adding a review about a user whether it be a vehicle owner or rentee
    the user adding the review must bee is registered, logged in and ether rented
    or their vehicle was rented from them.
    :param:request, a positive integer
    :return:dataResponse
    '''
    if request.user.is_authenticated:
        author_user = User.objects.get(id=request.user.id)
        author_user_credential = UserCredential.objects.get(user=author_user)

        about_user = User.objects.get(id=user_id)
        about_user_credential = UserCredential.objects.get(user=about_user)

        if about_user_credential != author_user_credential:
          new_review_Serializer = ReviwesSerializer(instance=Reviwes(auther=author_user_credential, about=about_user_credential) , data=request.data)

          if new_review_Serializer.is_valid():
             update_user_rating_Avg(request.data['rating'],about_user)

             new_review_Serializer.save()
             dataResponse = {
                "msg": "Your review posted Successfully",
                 "about": f'{about_user_credential}',
                "review": new_review_Serializer.data
              }
             return Response(dataResponse)
          else:
            print(new_review_Serializer.errors)
            dataResponse = {"msg": "couldn't post a review"}
            return Response(dataResponse, status=status.HTTP_400_BAD_REQUEST)
        else:
          return Response({"msg": "You can not post a review about your self"}, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response({"msg": "Login first then post a review"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
def edit_review(request : Request, review_id):
  '''
  this method for editing reviews, and it is only allowed to do so
  if the user is: the author of the review and logged in
  :param: request, a positive integers
  :return: dataResponse
  '''
  if request.user.is_authenticated:
      user = User.objects.get(id=request.user.id)
      user_credential = UserCredential.objects.get(user=user)
      print(user_credential)
      try:
        review = Reviwes.objects.get(auther=user_credential, id=review_id)
        print(review)
      except Exception as e:
        print(e)
        return Response({"msg": "Only the author can edit/alter the review"}, status=status.HTTP_401_UNAUTHORIZED)
      update_review = ReviwesSerializer(instance=review, data=request.data)

      if update_review.is_valid():
        update_user_rating_Avg(request.data['rating'], user)
        update_review.save()
        dataResponse = {
            "msg" : "Your review edited Successfully",
            "review" : update_review.data
        }
        return Response(dataResponse)
      else:
        print(update_vehicle.errors)
        dataResponse = {"msg" : "couldn't edit the review"}
        return Response( dataResponse, status=status.HTTP_400_BAD_REQUEST)
  else:
    return Response({"msg": "Login first then edit your review"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_review(request : Request, review_id):
    '''
     this method takes a review_id and deletes the review if the user is the author.
    :param vehicle_id: request, and a positive integer
    :return: dataResponse
    '''

    if request.user.is_authenticated:
     user = User.objects.get(id=request.user.id)
     user_credential = UserCredential.objects.get(user=user)

     try:
      review = Reviwes.objects.get(auther=user_credential, id=review_id)
      review.delete()
     except Exception as e:
         return Response({"msg": f"Can not delete this review {e}"}, status=status.HTTP_400_BAD_REQUEST)

     return Response({"msg": "Deleted Successfully"},status=status.HTTP_200_OK)

    else:
       dataResponse = {"msg": "couldn't delete this review"}
       return Response(dataResponse, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def list_my_reviews(request : Request):
    '''
    this method list all reviews written by the currently logged in user
    :param user_id: request
    :return: list of reviews objects
    '''
    try:
      user = User.objects.get(id=request.user.id)
      print(user)
      user_credential = UserCredential.objects.get(user=user)
      print(user_credential)
      reviews = Reviwes.objects.filter(auther=user_credential)

      dataResponse = {
        "msg" : "List of all my reviews",
        "author": f"{user.first_name} {user.last_name}",
        "reviews" : ReviwesSerializer(instance=reviews, many=True).data
      }

      return Response(dataResponse, status = status.HTTP_200_OK)
    except Exception as e:
        return Response({f"{e}"})


# Booking ,creat(rentee only) read(both) delet(both) accsept(update only the owner can)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_booking(request : Request, vehicle_id):
  '''
   this method for booking a vehicle if and only if
   the user is: registered and has credentials and is logged in.
  :param: request, a positive integers
  :return: dataResponse
  '''
  if request.user.is_authenticated:
      rentee_user = User.objects.get(id=request.user.id)
      rentee_user_credential = UserCredential.objects.get(user=rentee_user)

      vehicle = Vehicle.objects.get(id=vehicle_id)

      #cost
      total_cost = calc_total_cost(vehicle, request.data['vehicle_delivery'], request.data['start_date'],request.data['end_date'])
      new_booking_serializer = BookingSerializer(instance=Booking(rentee=rentee_user_credential, vehicle=vehicle, cost=total_cost), data=request.data)

      if new_booking_serializer.is_valid():
              new_booking_serializer.save()
              dataResponse = {
                  "msg": "Your booking request is sent, wait  for the car owner to accept",
                  "rentee": f"{rentee_user.first_name} {rentee_user.last_name}",
                  "booking": new_booking_serializer.data,
                  "total_cost": f"{total_cost}"
              }
              return Response(dataResponse)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def list_owner_booking(request : Request):
    '''
     this method list all booking request received.
    :param: request
    :return: dataResponse
    '''
    if request.user.is_authenticated:
     user = User.objects.get(id=request.user.id)
     user_credential = UserCredential.objects.get(user=user)

     #get the owner from their vehicle, Note: not an efficient way to do so but it will do for now
     owner_vehicles = Vehicle.objects.filter(owner=user_credential)
     bookings = Booking.objects.all()

     list_of_received_req =[]
     for item1,item2 in owner_vehicles,bookings:
         if item1 in bookings:
             list_of_received_req.append(item2)

     dataResponse = {
        "msg" : "List of All bookings",
        "bookings" : VehicleSerializer(instance=bookings, many=True).data
     }
     return Response(dataResponse)
    else:
        dataResponse = {"msg": "couldn't get this user vehicle"}
        return Response(dataResponse, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def list_rentee_booking():
    pass

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def list_rentee_old_booking():
    pass

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def list_owner_old_booking():
    pass

def update_user_rating_Avg(rating: str, user)->None:
    '''
    this function is being called in add_review method view after saving the new posted review.
    its takes a rating(out of 5) and update the user rating avg.
    :param: rating is a string of positive integer
    '''
    try:
     temp = UserCredential.objects.get(user=user).rating_avg
     Avg = ((round(temp)+round(rating))/5)
     UserCredential.objects.filter(user=user).update(rating_avg=round(Avg,2))# get do not have update
    except Exception as e:
        print(e)

def calc_total_cost(vehicle: Vehicle, vehicle_delivery: bool, start_date: str, end_date: str  )-> float:
    '''
    this method calculate total cost of renting
    '''
    start_date_time = datetime(year=int(start_date[:4]), month=int(start_date[6:7]),
                               day=int(start_date[8:10]), hour=int(start_date[11:13]),
                               minute=int(start_date[14:16]))

    end_date_time = datetime(year=int(end_date[:4]), month=int(end_date[6:7]),
                             day=int(end_date[8:10]), hour=int(end_date[11:13]),
                             minute=int(end_date[14:16]))

    price_per_hour = vehicle.hourly_rental_price
    vehicle_delivery = vehicle_delivery

    timedelta = end_date_time - start_date_time
    renting_hours = (timedelta.days*24) + ((timedelta.seconds/60)/60)

    if timedelta.days < 0 or renting_hours < 5:
        raise Exception("Start date must bee at least 5 hours before the end date")

    no_delivery_fee_total_price = renting_hours * price_per_hour
    if vehicle_delivery == 'True':
     total_price = no_delivery_fee_total_price + (no_delivery_fee_total_price * 0.20) # 20% of cost for delivery fee
    else:
        total_price = no_delivery_fee_total_price

    return total_price

