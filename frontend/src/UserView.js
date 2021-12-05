import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Tab,Dropdown,Menu} from "semantic-ui-react";
import {Route, BrowserRouter, Routes, useNavigate} from 'react-router-dom';
import BookMeeting from "./BookMeeting";
import Schedule from "./Schedule";
import Dashboard from "./Dashboard";
import {navigate} from "react-big-calendar/lib/utils/constants";

function UserView(){
    const [isAuth, setIsAuth] = useState(false)
    const navigate = useNavigate()

  const handleLogOut = () => {
        sessionStorage.removeItem("token")
        navigate("/home")
  }



    const panes = [
        {
            menuItem: 'Booking', render: () => <BookMeeting/>
        },
        {
            menuItem: 'Schedule', render: () => <Schedule/>
        },
        {
            menuItem: 'Room Management', render: () => <Tab.Pane active={isAuth}><BookMeeting/></Tab.Pane>
        },
        {
            menuItem: 'Dashboard', render : () => <Dashboard/>
        }
    ]

    return (
        <Container>
            <Menu secundary size={"small"}>
                <Menu.Menu position={'right'}>
                    <Menu.Item>Home</Menu.Item>
                    <Menu.Item>Contact Us</Menu.Item>
                    <Menu.Item onClick={handleLogOut}>Sign Out</Menu.Item>
                </Menu.Menu>
            </Menu>
            <Tab panes={panes}/>

        </Container>
    )

}
export default UserView;
