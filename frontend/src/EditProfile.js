import React, {Component, useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import {Route, Navigate, BrowserRouter, Routes, useNavigate} from 'react-router-dom';
import axios from "axios";
import moment from "moment";
import UserView from "./UserView";

function Edit() {
    const url = 'http://127.0.0.1:5000/redpush'
    const [open, setOpen] = useState(false);
    const [registerOpen, setRegisterOpen] = useState(false);
    const [token, setToken] = useState(sessionStorage.getItem("token"));
    const [isAuth, setIsAuth] = useState(!!(token && token !== "undefined"));
    const [name, setName] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("");

    const handleChange = () => {
        const requestOptions = {
        headers: { Authorization: "Bearer " + token }};
        const changes = {
            username: username,
            full_name: name,
            password: password,
            role: role
        }
        console.log(changes)
        axios.put(url + '/account/edit', changes,requestOptions).catch(function (error) {
            console.log(error);
        })
    }

    return(
        <Form>
            <Form.Field
                maxLength ='255'
                value = {name}
                onChange={e => setName(e.target.value)}
            >
                <label>Change Name</label>
                <input placeholder='Name' />
            </Form.Field>
            <Form.Field
                maxLength ='255'
                value = {username}
                onChange={e => setUsername(e.target.value)}
            >
                <label>Change Username</label>
                <input placeholder='Username' />
            </Form.Field>
            <Form.Field
                maxLength ='255'
                value = {password}
                onChange={e => setPassword(e.target.value)}
            >
                <label>Change Password</label>
                <input placeholder='Password' />
            </Form.Field>
                <Button type='submit'
                        primary onClick={() => {
                    handleChange()}} > Submit
                </Button>
        </Form>
)


}
export default Edit;