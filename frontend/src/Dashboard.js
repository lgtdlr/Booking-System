import React, {Component, useEffect, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import axios from "axios";

var mostBookingsWith = [];

async function getMostBookingWithSelectedUser() {
    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const requestOptions = {
        headers: { Authorization: "Bearer " + token }
    };
    axios.get(url+'/account/bookings-with-user', requestOptions).then(function
        (response) {
        mostBookingsWith = response.data
        for (let i = 0; i < mostBookingsWith.length; i++) {
            mostBookingsWith.push(mostBookingsWith[i])
        }
    })
}

function BookMeeting(){

    const [data, setData] = useState([{"name": 1, "Counts": 5},
                                                {"name": 2, "Counts": 4},
                                                {"name": 3, "Counts": 3},
                                                {"name": 4, "Counts": 2},
                                                {"name": 5, "Counts": 1}]);
    useEffect(() => {
        getMostBookingWithSelectedUser().then(r => {

            setData(mostBookingsWith)
            console.log("Bookings with" + mostBookingsWith)
        })

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
