import React, {Component, useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab, Confirm, Container} from 'semantic-ui-react';
import {Route, Navigate, BrowserRouter, Routes, useNavigate} from 'react-router-dom';
import axios from "axios";
import moment from "moment";
import UserView from "./UserView";

function EditRoom() {
    const url = 'http://127.0.0.1:5000/redpush'
    const [open, setOpen] = useState(false);
    const [registerOpen, setRegisterOpen] = useState(false);
    const [token, setToken] = useState(sessionStorage.getItem("token"));
    const [isAuth, setIsAuth] = useState(!!(token && token !== "undefined"));
    const [name, setName] = useState("");
    const [oldname,setOldName] = useState("");
    const [capacity, setCapacity] = useState("");
    const [type, setType] = useState("");


    const handleChange = () => {
        const requestOptions = {
        headers: { Authorization: "Bearer " + token }};
        const changes = {
            oldname : oldname,
            name: name,
            capacity: capacity,
            type: type
        }
        console.log(changes)
        axios.put(url + '/account/edit-room', changes,requestOptions).catch(function (error) {
            console.log(error);
        })
    }

    return(
        <Container>
        <Form>
             <Form.Field
                maxLength ='255'
                value = {oldname}
                onChange={e => setOldName(e.target.value)}
            >
                <label>Room name you want to change</label>
                <input placeholder='Old name' />
            </Form.Field>
            <Form.Field
                maxLength ='255'
                value = {name}
                onChange={e => setName(e.target.value)}
            >
                <label>New Name</label>
                <input placeholder='New name' />
            </Form.Field>

            <Form.Field
                maxLength ='255'
                value = {capacity}
                onChange={e => setCapacity(e.target.value)}
            >
                <label>Change Capacity</label>
                <input placeholder='Capacity' />
            </Form.Field>
            <Form.Field
                maxLength ='255'
                value = {type}
                onChange={e => setType(e.target.value)}
            >
                <label>Change Type</label>
                <input placeholder='Type' />
            </Form.Field>
                <Button type='submit'
                        primary onClick={() => {
                    handleChange()}} > Submit
                </Button>
        </Form>
            </Container>
)

}
export default EditRoom;