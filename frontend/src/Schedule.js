import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Grid, Modal, Popup} from "semantic-ui-react";
import axios from "axios";
import {useNavigate} from "react-router-dom";
import ReactDOM from "react-dom";



function Schedule(){

    const navigate = useNavigate()
    const token = sessionStorage.getItem("token")
    const url = "http://127.0.0.1:5000/redpush"
    const node = document.createElement("div");
    const [open, setOpen] = useState(true);
    const localizer = momentLocalizer(moment)

    const [isAuth, setIsAuth] = useState(!!(token && token !== "undefined"));
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

        setDates(events)

      })
      .catch(function (error) {
        console.log(error);
        setIsAuth(false);
        sessionStorage.removeItem("token");
        popup();
      });
    }, []);







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
