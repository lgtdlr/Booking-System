import React, {Component, useEffect, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Dimmer, Form, Grid, Input, Loader, Modal, Popup} from "semantic-ui-react";
import axios from "axios";
import {useNavigate} from "react-router-dom";
import ReactDOM from "react-dom";
import _ from "lodash";

let events = []
let invitees = []

async function getAllEvents(url, token) {

    const requestOptions = {
        method: 'GET',
        headers: { Authorization: "Bearer " + token }
    };
    await axios.get(url + '/account/events', requestOptions)
      .then(function (response) {

        events = response.data;

        for (let i = 0; i < events.length; i++) {
            events[i].start = moment.utc(events[i].start).toDate();
            events[i].end = moment.utc(events[i].end).toDate();
        }


          })
      .catch(function (error) {

      });
}

async function getAllEventInvitees(url, token, event_id) {

    const requestOptions = {
        method: 'GET',
        headers: { Authorization: "Bearer " + token }
    };
    await axios.get(url + '/invitee/'+event_id, requestOptions)
      .then(function (response) {

        invitees = response.data;

          })
      .catch(function (error) {

      });
}


function Schedule(){

    const url = "https://redpush.herokuapp.com/redpush"
    const token = sessionStorage.getItem("token")
    const navigate = useNavigate()
    const node = document.createElement("div");
    const [open, setOpen] = useState(false);
    const [unavailableOpen, setUnavailableOpen] = useState(false);
    const localizer = momentLocalizer(moment)
    const [isLoading, setIsLoading] = useState(true);
    const [eventId, setEventId] = useState('');
    const [selectedDate, setSelectedDate] = useState('');
    const [eventTitle, setEventTitle] = useState('');
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    const [eventDescription, setEventDescription] = useState('');
    const [isUpdate, setIsUpdate] = useState(false);
    const [eventInvitees, setEventInvitees] = useState(invitees);
    const [editInvitees, setEditInvitees] = useState(false);
    const [selectedInvitees, setSelectedInvitees] = useState([]);
    const inviteeOptions = _.map(eventInvitees, (username, index) => ({
        key: eventInvitees[index].username,
        text: eventInvitees[index].username + " ( " + eventInvitees[index].full_name + " )",
        value: eventInvitees[index].account_id,
    }));


    const [isAuth, setIsAuth] = useState(!!(token && token !== "undefined"));
    const [dates, setDates] = useState([{
        // 'title': 'Selection',
        // 'allDay': false,
        // 'start': new Date(moment.now()),
        // 'end': new Date(moment.now())
    }]);

    // const handleDelete = () => {
    //     const json = {
    //         event_id: eventId
    //     }
    //     const requestOptions = {
    //     method: 'POST',
    //     headers: { Authorization: "Bearer " + token }};
    //
    //     axios.post(url + '/event/delete-event', json, requestOptions)
    //   .then(function (response) {
    //       window.location.reload(false);
    //       })
    //   .catch(function (error) {
    //
    //   });
    //
    // }


    const handleUpdate = () => {
        const json = {
            event_id: eventId,
            title: eventTitle,
            date: selectedDate,
            description: eventDescription
        }
        const requestOptions = {
        method: 'PUT',
        headers: { Authorization: "Bearer " + token }};

        axios.put(url + '/event/'+eventId, json, requestOptions)
      .then(function (response) {
          window.location.reload(false);
          })
      .catch(function (error) {

      });

    }

    const handleEditInvitees = () => {
        getAllEventInvitees(url, token, eventId).then(_ => {
            setEventInvitees(invitees);
            setEditInvitees(true);
            console.log(invitees);
        });
    };

    const handleDeleteInvitees = () => {
        const jsonDeleteInvitees = {
            account_id: selectedInvitees,
            event_id: eventId
        }
        const requestOptions = {
        method: 'POST',
        headers: { Authorization: "Bearer " + token }};

        console.log(jsonDeleteInvitees)

        axios.post(url + '/invitee/delete-invitees', jsonDeleteInvitees, requestOptions)
      .then(function (response) {
          window.location.reload(false);
          })
      .catch(function (error) {

      });
    };


    const handleUnavailableDelete = () => {

        const json = {
            date: selectedDate,
            start_time: startTime,
            end_time: endTime,
            is_available: true
        }
        const requestOptions = {
        method: 'POST',
        headers: { Authorization: "Bearer " + token }};

        axios.post(url + '/account/set-availability-true', json, requestOptions)
      .then(function (response) {
          window.location.reload(false);
          })
      .catch(function (error) {

      });

    }

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

    useEffect(() => {
        getAllEvents(url, token).then(_ => {
            setDates(events);
            setIsLoading(false);
        });


    }, []);




    return <Container style={{ height: 800 }}>
        {isLoading === true && <Dimmer active={isLoading}>
            <Loader>Please wait</Loader>
        </Dimmer>}

        <Calendar
        localizer={localizer}
        startAccessor="start"
        events={dates}
        popup
        endAccessor="end"
        views={["month", "week", "day"]}
        defaultDate={Date.now()}
        onSelectEvent={event => {

                setEventId(event.id);
                setEventTitle(event.title);
                setEventDescription(event.description);
                setSelectedDate(moment(event.start).utc(true).format('YYYY-MM-DD'))
                setStartTime(moment(event.start).utc(true).format('HH:mm:ss'));
                setEndTime(moment(event.end).utc(true).format('HH:mm:ss'));
                getAllEventInvitees(event.id).then(_ => {
                    if (event.id > 0) {
                        setOpen(true);
                    } else {
                        setUnavailableOpen(true);
                     }
                });


        }
        }
    >


    </Calendar>
        <Modal
                centered={false}
                open={open}
                onClose={() => {
                    setOpen(false)
                }}
                onOpen={() => setOpen(true)}
            >
                <Modal.Header>{eventTitle}</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        {'Description:'} {eventDescription}
                        <h1> </h1>
                        {'Date:'} {selectedDate}
                        <h1> </h1>
                        {'Starts at:'} {startTime}
                    </Modal.Description>

                </Modal.Content>
                <Modal.Actions>
                    <Button color={"youtube"} onClick={() => {
                        setOpen(false)
                        // handleDelete();
                    }}>Delete</Button>
                    <Button color={"facebook"} onClick={() => {
                        setOpen(false)
                        setIsUpdate(true)
                    }}>Edit</Button>
                    <Button onClick={() => {
                        setOpen(false)
                    }}>Cancel</Button>
                </Modal.Actions>
            </Modal>
        <Modal
                centered={false}
                open={unavailableOpen}
                onClose={() => {
                    setUnavailableOpen(false)
                }}
                onOpen={() => setUnavailableOpen(true)}
            >
                <Modal.Header>{eventTitle}</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        <h1> </h1>
                        {'Date:'} {selectedDate}
                        <h1> </h1>
                        {'Starts at:'} {startTime}
                    </Modal.Description>
                </Modal.Content>
                <Modal.Actions>
                    <Button color={"youtube"} onClick={() => {
                        handleUnavailableDelete();
                        setUnavailableOpen(false);
                    }}>Delete</Button>
                    <Button onClick={() => {
                        setUnavailableOpen(false);
                    }}>Cancel</Button>
                </Modal.Actions>
            </Modal>
        <Modal
                centered={false}
                open={isUpdate}
                onClose={() => {
                    setIsUpdate(false)
                }}
                onOpen={() => setIsUpdate(true)}
            >
                <Modal.Header>{eventTitle}</Modal.Header>
                <Modal.Content>
                    <h1 className="ui centered">Edit event details</h1>
                    <Form.Input>
                        <Form.Field
                    control={Input}
                    icon='gg'
                    name='title'
                    iconPosition='left'
                    label='Title'
                    placeholder='Title'
                    maxLength ='50'
                    value = {eventTitle}
                    onChange={e => {
                        setEventTitle(e.target.value)
                    }
                    }
                    required
                />
                <Form.Field
                    control={Input}
                    name='description'
                    icon='sticky note outline'
                    iconPosition='left'
                    label='Description'
                    placeholder='Description'
                    maxLength ='400'
                    value = {eventDescription}
                    onChange={e => {
                        setEventDescription(e.target.value)
                    }
                    }
                    required
                />
                    </Form.Input>
                </Modal.Content>
                <Modal.Actions>
                    <Button color={'facebook'} onClick={() => {
                        handleEditInvitees();
                        setIsUpdate(false);
                    }}>Edit Invitees</Button>
                    <Button color={'vk'} onClick={() => {
                        handleUpdate();
                        setIsUpdate(false);
                    }}>Finish editing</Button>
                    <Button onClick={() => {
                        setIsUpdate(false);
                    }}>Cancel</Button>

                </Modal.Actions>
            </Modal>
        <Modal
                centered={false}
                open={editInvitees}
                onClose={() => {
                    setEditInvitees(false)
                }}
                onOpen={() => setEditInvitees(true)}
            >
                <Modal.Header>{eventTitle}</Modal.Header>
                <Modal.Content>
                    <h1 className="ui centered">Edit invitees</h1>
                    <Form.Dropdown
                          fluid
                          search
                          multiple
                          selection
                          name='account_id'
                          label='Remove selected invitees'
                          value={selectedInvitees}
                          placeholder='User(s)'
                          options= {inviteeOptions }
                          onChange={(e, value) => {
                              setSelectedInvitees(value.value)
                              console.log(selectedInvitees)
                          }
                          }
                      />
                </Modal.Content>
                <Modal.Actions>
                    <Button color={'youtube'} onClick={() => {
                        handleDeleteInvitees();
                        setEditInvitees(false);
                    }}>Remove invitees</Button>
                    <Button onClick={() => {
                        setEditInvitees(false);
                    }}>Cancel</Button>

                </Modal.Actions>
            </Modal>
    </Container>


}
export default Schedule;
