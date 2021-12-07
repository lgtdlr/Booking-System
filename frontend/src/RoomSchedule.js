import React, {Component, useEffect, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Dimmer, Form, Grid, Loader, Modal, Popup} from "semantic-ui-react";
import axios from "axios";
import {useNavigate} from "react-router-dom";
import ReactDOM from "react-dom";
import _ from "lodash";

let events = [];
let rooms = [];


async function getAllRooms() {
    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const requestOptions = {
        headers: { Authorization: "Bearer " + token }
    };
    await axios.get(url + '/room', requestOptions)
      .then(function (response) {
          rooms = response.data

      })
      .catch(function (error) {
        console.log(error);
      });
}

async function getAllRoomEvents(room) {
    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const requestOptions = {
        headers: { Authorization: "Bearer " + token }
    };
    await axios.get(url + '/room/'+room+'/events', requestOptions)
      .then(function (response) {

          events =response.data

        for (let i = 0; i < events.length; i++) {
            events[i].start = moment.utc(events[i].start).toDate();
            events[i].end = moment.utc(events[i].end).toDate();
        }

      })
      .catch(function (error) {
        console.log(error);
      });
}

function RoomSchedule() {
    const navigate = useNavigate();
    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const localizer = momentLocalizer(moment);
    const [newEvent, setNewEvent] = useState({});
    const [room, setRoom] = useState(1);
    const [allRooms, setAllRooms] = useState(rooms);
    const [allEvents, setAllEvents] = useState(events);
    const [isLoading, setIsLoading] = useState(true);
    const roomOptions = _.map(allRooms, (name, index) => ({
        key: allRooms[index].name,
        text: allRooms[index].type + " : " + allRooms[index].name + " (  Max. capacity: " + allRooms[index].capacity + " )",
        value: allRooms[index].room_id,
    }));

    const requestOptions = {
        headers: {Authorization: "Bearer " + token}
    };

    useEffect(() => {
        getAllRooms().then(_ => {
            setIsLoading(false);
            setAllRooms(rooms);
        });
        getAllRoomEvents(room).then(_ => {
            setIsLoading(false);
            setAllEvents(events);
        });

    }, []);

        return <Container style={{height: 800}}>
            {isLoading === true && <Dimmer active={isLoading} inverted>
            <Loader>Please wait</Loader>
        </Dimmer>}
            <Form.Dropdown
            fluid
            search
            selection
            label='Select room'
            name='room_id'
            placeholder='Room(s)'
            defaultValue={1}
            options= {roomOptions }
            onChange={(e, value) => {
                setRoom(value.value)
                setIsLoading(true)
                console.log(room)
                getAllRoomEvents(room).then(_ => {
                    console.log(events);
                    setAllEvents(events)
                    setIsLoading(false)
                })
            }}
            required
        />
            <Calendar
            selectable
            localizer={localizer}
            startAccessor="start"
            events={allEvents}
            endAccessor="end"
            showMultiDayTimes
            popup
            views={["month", "week", "day"]}
            defaultDate={Date.now()}
            onSelectSlot={(selected) => {
                setNewEvent({
                    'title': 'Selection',
                    'start': new Date(selected.start),
                    'end': new Date(selected.end)
                })
                // handleAddEvents()

                // setStartDate(moment(selected.start).utc(true).format('YYYY-MM-DD'));
                // setStartTime(moment(selected.start).utc(true).format('HH:mm:ss'));
                // setEndTime(moment(selected.end).utc(true).format('HH:mm:ss'));
                // setOpen(true);
            }}
        >

        </Calendar>

        </Container>


}

export default RoomSchedule;
