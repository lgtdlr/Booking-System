import React, {Component, useEffect, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Header, Image, List, Modal} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import axios from "axios";

let mostBookingsWith = [];
let mostBookedUsers = [];

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


function BookMeeting(){
        //data represents users with whom registered has the most bookings with
    const [data, setData] = useState([{"name": 1, "Counts": 5},
                                                {"name": 2, "Counts": 4},
                                                {"name": 3, "Counts": 3},
                                                {"name": 4, "Counts": 2},
                                                {"name": 5, "Counts": 1}]);

    const [mostBooked,setMostBooked] = useState([{"name": 1, "Counts": 1},
                                                            {"name": 2, "Counts": 4}])



    useEffect(() => {
        getMostBookingWithSelectedUser().then(  () => {
            setData(mostBookingsWith)
            console.log("Bookings with" + mostBookingsWith)
        })

        getMostBookedUsers().then( ()=>{
            setMostBooked(mostBooked)
            console.log(mostBookedUsers)
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
        <div><Header as='h1'> You share a maximum of {(data.length !== 0 ? data[0].Counts : 0)} bookings with these users </Header>
        <List horizontal ordered> {data.map (item=>
      (<List.Item key={item.account_id}>
          <Image avatar src='https://react.semantic-ui.com/images/avatar/small/tom.jpg' />
          <List.Content>
             <List.Header>{item.name}</List.Header>

          </List.Content>
        </List.Item>))}
      </List>
        </div>

    )

}
export default BookMeeting;
