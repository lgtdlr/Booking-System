import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal} from "semantic-ui-react";
import axios from "axios";


// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function Schedule(){

    const token = sessionStorage.getItem("token")
    const url = "http://127.0.0.1:5000/redpush"

    const [dates, setDates] = useState([{
        // 'title': 'Selection',
        // 'allDay': false,
        // 'start': new Date(moment.now()),
        // 'end': new Date(moment.now())
    }]);

    const requestOptions = {
        method: 'GET',
        headers: { Authorization: "Bearer " + token }
    };

    let events = {}

    axios.get(url + '/account/events', requestOptions)
      .then(function (response) {
        console.log(response.data);
        events = response.data;

        for (let i = 0; i < events.length; i++) {
            events[i].start = moment.utc(events[i].start).toDate();
            events[i].end = moment.utc(events[i].end).toDate();
        }

        setDates(events)

      })
      .catch(function (error) {
        console.log(error);
      });


    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment)

    return <Container style={{ height: 800 }}><Calendar
        localizer={localizer}
        startAccessor="start"
        events={dates}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
    >

    </Calendar>
    </Container>


}
export default Schedule;
