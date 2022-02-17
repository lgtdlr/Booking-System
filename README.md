Designed, implemented and tested the backend of an application used to manage a booking system (using Google Calendar as reference). The data in the application is managed by a relational database system and exposed to client applications through a REST API. The database application and REST API was built using Flask, which forms the backend of the system. The database engine is relational, and the code was implemented in Python. The backend site provides the user with the features specified in this document. In addition, this provide a Web-based dashboard indicating relevant statistics that are also specified below and a basic frontend for all the operations.

Operations to be supported
The site supports the following operations:
1. Register a new user
2. Find available rooms (lab, classroom, study space, etc.) at a time frame given user role.
3. Find who appointed a room at a certain time
4. Give an all-day schedule for a room
5. Give an all-day schedule for a user
6. Find a time that is free for every user given.
7. Create a meeting with 2+ people in a room
8. Limit the access to rooms appointment, information and schedule according to person’s authorization. (Just for highest role)
9. Allow user to mark time-space as “Unavailable”/ “Available” in his schedule(should appear in user schedule and by default it is all marked as available)
10. Only highest can mark a time-space as “Unavailable”/ “Available” for any type of room (should appear in room schedule and By default it is all marked as available)
11. CRUD operations in the frontend
12. User Statistic
  - Most used Room by user given
- User most booked with user given
13. Global Statistic
- Find busiest hours (Find top 5)
- Find most booked users (Find top 10)
- Find most booked rooms (Find top 10)

Views for application:

Site has the following views:
- Login/Register
- User View: This view have functions divided by tabs. The number of tabs depends on the role and the functions that each role is allowed.
- Creating meeting/unavailability
- Schedule
- Modify User information
- User statistics
- Other that may be needed to comply with the spect.
- Buttons and other elements can be used to implements the functionalities.
- Include Logout
- Dashboard for statistics
