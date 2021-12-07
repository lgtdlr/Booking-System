import React, {Component, useEffect, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Header, Image, List, Modal} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import axios from "axios";

let mostBookingsWith = [];
let mostBookedUsers = [];
let mostBookingsIn_Room_by_Registered_User = [];
let top_10_Booked_Rooms = [];
let busiestHours = [];

async function getMostBookingWithSelectedUser() {
    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const requestOptions = {
        headers: { Authorization: "Bearer " + token }
    };
    await axios.get(url+'/account/bookings-with-user', requestOptions).then(function
        (response) {
        mostBookingsWith = response.data
    })
}


async function getMostBookedUsers() {

    const url = "http://127.0.0.1:5000/redpush";

    await axios.get(url+'/account/booked-users').then(function
        (response) {
        mostBookedUsers = response.data
    })
}



async function getMostBooking_InRoom_WithSelectedUser() {
    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const requestOptions = {
        headers: { Authorization: "Bearer " + token }
    };
    await axios.get(url+'/room/most-booked-room-by-user',requestOptions).then(function
        (response) {
        mostBookingsIn_Room_by_Registered_User = response.data
    })
}


async function getMostBookedRooms(){
    const url = "http://127.0.0.1:5000/redpush";

    await axios.get(url+'/room/most-booked').then(function
        (response) {
        top_10_Booked_Rooms = response.data
    })
}


async function getMostBusiestHours(){
    const url = "http://127.0.0.1:5000/redpush";

    await axios.get(url+'/event/busiest-hours').then(function
        (response) {
        busiestHours = response.data
    })
}


function BookMeeting(){
        //data represents users with whom registered has the most bookings with
    const [data, setData] = useState([{"name": 1, "Counts": 5},
                                                {"name": 2, "Counts": 4},
                                                {"name": 3, "Counts": 3},
                                                {"name": 4, "Counts": 2},
                                                {"name": 5, "Counts": 1}]);

    const [mostBooked,setMostBooked] = useState([{"name": 1, "Counts": 1},
                                                            {"name": 2, "Counts": 4}])


    const [mostBookedRoom_by_user,setMostBookedRoom] = useState(
        [{"name": 1, "room_uses": 2}]
    );

    const [ten_most_Booked_Rooms,set_10_MostBookedRooms] = useState(
        [{"name": 1, "room_uses": 2}]
    );

    const [top_5_busiest_Hours, setBusiestHours] = useState(
        [{"start_time" : "01:30:00", "end_time" : "2:00:00", "times_scheduled" : 23}]
    )


    useEffect(() => {
        getMostBookingWithSelectedUser().then(  () => {
            setData(mostBookingsWith)
            console.log("Bookings with" + mostBookingsWith)
        })

        getMostBookedUsers().then( ()=>{
            setMostBooked(mostBookedUsers)
            console.log(mostBookedUsers)
            }
        )


        getMostBooking_InRoom_WithSelectedUser().then( () =>{
            setMostBookedRoom(mostBookingsIn_Room_by_Registered_User)
            console.log(mostBookingsIn_Room_by_Registered_User)
            }

        )

        getMostBookedRooms().then(   ()=> {
            set_10_MostBookedRooms(top_10_Booked_Rooms)
            console.log(top_10_Booked_Rooms)
            }

        )

        getMostBusiestHours().then( ()=>{
            setBusiestHours(busiestHours)
            console.log(top_10_Booked_Rooms)
            }


        )


    }, [])

    // return <Container style={{ height: 800 }}>
    //
    //     <BarChart width={730} height={250} data={data}>
    //         <CartesianGrid strokeDasharray="3 3" />
    //         <XAxis dataKey="name" />
    //         <YAxis />
    //         <Tooltip />
    //         <Legend />
    //         <Bar dataKey="Counts" fill="#8884d8" />
    //     </BarChart>
    // </Container>

    return (
<div>
    <Header as='h1'> You share a maximum of {(data.length !== 0 ? data[0].Counts : 0)} bookings with these users </Header>
        <List horizontal ordered> {data.map (item=>
          (<List.Item key={item.account_id}>
              <Image avatar src='https://react.semantic-ui.com/images/avatar/small/tom.jpg' />
              <List.Content>
                 <List.Header>{item.name}</List.Header>

              </List.Content>
            </List.Item>))}
         </List>

    <Header as='h1'> Here are the top 10 most booked users </Header>
         <List horizontal ordered> {mostBooked.map (item=>
          (<List.Item key={item.account_id}>
              <Image avatar src='https://react.semantic-ui.com/images/avatar/small/tom.jpg' />
              <List.Content>
                 <List.Header>{item.name}</List.Header>
                  Bookings {item.Counts}
              </List.Content>
            </List.Item>))}
          </List>

    <Header as='h1'> These are the most used rooms or room used by you </Header>
         <List horizontal ordered> {mostBookedRoom_by_user.map (item=>
      (<List.Item key={item.account_id}>

          <List.Content>
             <List.Header>{item.name}</List.Header>
              Room uses {item.room_uses}
          </List.Content>
        </List.Item>))}
      </List>


    <Header as='h1'> These are the top 10 most used rooms </Header>
         <List horizontal ordered> {ten_most_Booked_Rooms.map (item=>
      (<List.Item key={item.account_id}>

          <List.Content>
             <List.Header>{item.name}</List.Header>
              Room uses {item.room_uses}
          </List.Content>
        </List.Item>))}
      </List>



    <Header as='h1'> These are the top 5 busiest hours </Header>
         <List horizontal ordered> {top_5_busiest_Hours.map (item=>
      (<List.Item key={item.timeslot_id}>

          <List.Content>
             <List.Header>start_time {item.start_time} </List.Header>
              <List.Header>end_time {item.end_time} </List.Header>
              Times scheduled {item.times_scheduled}
          </List.Content>
        </List.Item>))}
      </List>
</div>

    )

}
export default BookMeeting;
