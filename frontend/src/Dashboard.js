import React, {Component, useEffect, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import axios from "axios";

//let mostBookingsWith = [];

// async function getMostBookingWithSelectedUser() {
//     const token = sessionStorage.getItem("token");
//     const url = "http://127.0.0.1:5000/redpush";
//     const requestOptions = {
//         headers: { Authorization: "Bearer " + token }
//     };
//     axios.get(url+'/account/bookings-with-user', requestOptions).then(function
//         (response) {
//         mostBookingsWith = response.data
//             console.log(mostBookingsWith)
//
//
//     })
// }

function BookMeeting(){
    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const requestOptions = {
        headers: { Authorization: "Bearer " + token }
    };
    let mostBookingsWith = [];

      //const [data, setData] = useState([]);
    const [data, setData] = useState([]);
    useEffect(() => {
        axios.get(url+'/account/bookings-with-user', requestOptions)
        .then(function
                (response) {
                mostBookingsWith = response.data
                setData(mostBookingsWith)



    })
    console.log(data)
    }, [])

    return <Container style={{ height: 800 }}>

        <BarChart width={730} height={250} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Meetings" fill="#8884d8" />
        </BarChart>
    </Container>


}
export default BookMeeting;
