import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Grid, Modal, Select} from "semantic-ui-react";
import axios from "axios";
import ReactDOM from "react-dom";
import {useNavigate} from "react-router-dom";
import _ from 'lodash';
import BookingFormContainer from "./components/booking-form";

function BookMeeting(){
    const navigate = useNavigate();
    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const [newEvent, setNewEvent] = useState({});
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [startTimeId, setStartTimeId] = useState("");
    const [endTimeId, setEndTimeId] = useState("");
    const [startTime, setStartTime] = useState("");
    const [endTime, setEndTime] = useState("");
    const [roomId, setRoomId] = useState("");
    const [allUsers, setAllUsers] = useState([]);
    const [allRooms, setAllRooms] = useState([]);
    const [allTimeslots, setAllTimeslots] = useState([]);
    const [invitees, setInvitees] = useState([]);
    const [allEvents, setAllEvents] = useState([]);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment);
    const node = document.createElement("div");
    let createdEvent = {};
    let events = [];
    let users = [];
    let rooms = [];
    let timeslots = [];

    const requestOptions = {
        headers: { Authorization: "Bearer " + token }
    };

    const handleBooking = () => {
        const booking = {
            title: title,
            description: description,
            date: moment(startDate).local().format("YYYY-MM-DD"),
            room_id: roomId,
            account_id: invitees,
            timeslot_id: [
                startTimeId,
                endTimeId
            ]
        }

        console.log(booking);

        axios.post(url + '/event/create-meeting', booking, requestOptions)
      .then(function (response) {

        createdEvent.start = moment.utc(createdEvent.start_time).toDate();
        createdEvent.end = moment.utc(createdEvent.end_time).toDate();

        setNewEvent(createdEvent);
        handleAddEvents();

      })
      .catch(function (error) {
        console.log(error);
        // setRegisterOpen(true)
      });
    }

    const handleAddEvents = () => {
        setAllEvents([...allEvents, newEvent])
    }

    const userOptions = _.map(allUsers, (username, index) => ({
        key: allUsers[index].username,
        text: allUsers[index].username + " ( " + allUsers[index].full_name + " )",
        value: allUsers[index].account_id,
    }));

    const roomOptions = _.map(allRooms, (name, index) => ({
        key: allRooms[index].name,
        text: allRooms[index].type + " : " + allRooms[index].name + " (  Max. capacity: " + allRooms[index].capacity + " )",
        value: allRooms[index].room_id,
    }));

    const timeslotOptions = _.map(allTimeslots, (name, index) => ({
        key: allTimeslots[index].start_time,
        text: allTimeslots[index].start_time,
        value: allTimeslots[index].timeslot_id,
    }));

    const endTimeslotOptions = _.map(allTimeslots, (name, index) => ({
        key: allTimeslots[index].end_time,
        text: allTimeslots[index].end_time,
        value: allTimeslots[index].timeslot_id,
    }));


    const popup = () => {
        document.body.appendChild(node);
          const PopupContent = () => {
            return (
              <Modal
                        centered={false}
                        open={open}
                    >
                        <Modal.Header>Not logged in</Modal.Header>
                        <Modal.Content>
                            <Modal.Description>
                                You are not logged in or your session has expired.
                            </Modal.Description>
                        </Modal.Content>
                        <Modal.Actions>
                            <Button onClick={() => {
                                clear();
                                navigate("/home")
                            }}>OK</Button>
                        </Modal.Actions>
                    </Modal>
            );
          };

          const clear = () => {
            ReactDOM.unmountComponentAtNode(node);
            node.remove();
          }

          ReactDOM.render(<PopupContent/>, node);
    };

    React.useEffect(() => {
        axios.get(url + '/account/events', requestOptions)
      .then(function (response) {

        events = response.data;

        for (let i = 0; i < events.length; i++) {
            events[i].start = moment.utc(events[i].start).toDate();
            events[i].end = moment.utc(events[i].end).toDate();
        }

        setAllEvents(events);


      })
      .catch(function (error) {
        console.log(error);
        sessionStorage.removeItem("token");
        popup();
      });

        axios.get(url + '/account', requestOptions)
      .then(function (response) {

        users = response.data;
        setAllUsers(users);

      })

        axios.get(url + '/room', requestOptions)
      .then(function (response) {

        rooms = response.data;
        setAllRooms(rooms);

      })

        axios.get(url + '/timeslot', requestOptions)
      .then(function (response) {

        timeslots = response.data;
        setAllTimeslots(timeslots);

      })
    }, []);

    return <Container style={{ height: 800 }}><Calendar
        selectable
        localizer={localizer}
        startAccessor="start"
        events={allEvents}
        endAccessor="end"
        showMultiDayTimes
        popup
        views={["month", "day"]}
        defaultDate={Date.now()}
        onSelectSlot = {(selected) => {
            setNewEvent({
                        'title': 'Selection',
                        'start': new Date(selected.start),
                        'end': new Date(selected.end)
                    } )
            handleAddEvents()

            setStartDate(moment(selected.start).utc(true).format('YYYY-MM-DD'));
            setStartTime(moment(selected.start).utc(true).format('HH:mm:ss'));
            setEndTime(moment(selected.end).utc(true).format('HH:mm:ss'));
            setOpen(true);
        } }
    >

    </Calendar>
        <Modal
                centered={false}
                open={open}
                onClose={() => {
                    setOpen(false)
                    if (newEvent !== {}) {
                            allEvents.pop();
                        }
                        setNewEvent({})
                }}
                onOpen={() => setOpen(true)}
            >
                <Modal.Header>EVENT BOOKING</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        Book a new event and invite guests
                        <h1> </h1>
                    </Modal.Description>
                    <BookingFormContainer />
                </Modal.Content>
                <Modal.Actions>
                    <Button onClick={() => {
                        setOpen(false)
                        if (newEvent !== {}) {
                            allEvents.pop();
                        }
                        setNewEvent({})
                    }}>Cancel</Button>
                </Modal.Actions>
            </Modal>
        <Container fluid>
        <Button
            fluid
            onClick={() => {setOpen(true)}}
        > Book Meeting </Button>
        <Button
            fluid
            onClick={() => {setOpen(true)}}
        > Mark as unavailable</Button>
    </Container>
    </Container>


}
export default BookMeeting;
