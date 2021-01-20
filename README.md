# Charge
## Description:
Charge is a tool that is designed for the electric vehicle driving community that allows you to search by a city or state to locate nearby charging stations and detailed information on each individual station to ensure it is the best fit for your vehicle and your charging needs.  <br /> <br />
[Link to Charge EV Stations](https://chargecapstone.herokuapp.com/)
## Features:
* 	Users can search for electric vehicle charging stations based on a location.
*  Users can select a specific charging station to see more details on it.
*  Users are instructed to create an account to use the application, which they can later edit at will.
*  Users can favorite a station by selecting a star which will add it to their favorites list. They also have the ability to select it again to delete it from their favorites.
*  Users can view their favorites and account information in the profile tab.

## API(s) Used:
[Open Charge Map API](https://openchargemap.org/site/develop/api?ref=apilist.fun) <br />
[Mapquest Geocoding API](https://developer.mapquest.com/documentation/geocoding-api/)
## User Flow:
1. A user will be directed to the home page:
	* If the user is not signed in you will be presented with a description of the app and they will be instructed to either go to the sign up or log in forms via the links.
	* If the user is signed in they will presented with a search bar to search for stations by location and they will also be able to view the profile page or log out.
1. When a user searches a location, they will be presented with the ten nearest charging stations.
	* If a user does not like any of the selections, they can then search for a different location.
	* If a user does choose to select an option they will see in depth detail on the specified station and they will be presented with a star that they can click to add the station to their favorites list. If the user has happened to already favorite that station they will be able to select the star again to unfavorite it.
3. At any point while a user is signed in they are able to select the profile image icon to view their favorites list and below is where they are able to view their account information (the username and email that are associated with the account) and click the link below to be sent to the profile edit form where they must enter their password to confirm any changes. 	


## Technology Stack Utilized:
* Frontend:
	* HTML
	* CSS
	* Jinja
* Backend
	* Python
	* Flask
	* PostgreSQL
	* SQLAlchemy
	* WTForms
