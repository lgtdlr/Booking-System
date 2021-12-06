import React, {Component, useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import {Route, Navigate, BrowserRouter, Routes, useNavigate} from 'react-router-dom';
import axios from "axios";
import moment from "moment";


function HomePage() {
    const url = 'http://127.0.0.1:5000/redpush'
    const [open, setOpen] = useState(false);
    const [registerOpen, setRegisterOpen] = useState(false);
    const [token, setToken] = useState(sessionStorage.getItem("token"));
    const [isAuth, setIsAuth] = useState(!!(token && token !== "undefined"));
    const [name, setName] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("");
    const roles = [
        { key: 's', text: 'Student', value: 'Student' },
        { key: 'p', text: 'Professor', value: 'Professor' },
        { key: 'd', text: 'Department Staff', value: 'Department Staff' },
    ]

    const navigate = useNavigate()

    const handleChange = (event, newValue) => {
        setOpen(true);
    }

    const handleRegisterChange = (event, newValue) => {
        setRegisterOpen(true);
    }

    const handleLogin = (event, newValue) => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username, password: password})
        };

        fetch(url+'/account/login', requestOptions)
        .then(response => response.json())
        .then(data => {
            sessionStorage.setItem("token", data.access_token)
            setIsAuth(sessionStorage.getItem("token")!=="undefined")

        });
    }

    const handleRegister = (event, newValue) => {
        const user = {
            full_name: name,
            username: username,
            password: password,
            role: role
        }

        axios.post(url + '/account', user)
      .then(function (response) {

        handleLogin()

      })
      .catch(function (error) {
        console.log(error);
        setRegisterOpen(true)
      });
    }

    if (!isAuth) {
        return (
            <Segment><Header dividing textAlign="center" size="huge">Welcome to DB Demo</Header>
            <Modal
                centered={false}
                open={open}
                onClose={() => setOpen(false)}
                onOpen={() => setOpen(true)}
            >
                <Modal.Header>Register</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        Fill out the following information to register a new account.
                        <h1> </h1>
                    </Modal.Description>
                    <Grid columns={1} relaxed='very' stackable>
                    <Grid.Column>
                        <Form>
                            <Form.Input
                                icon='user outline'
                                iconPosition='left'
                                label='Name'
                                placeholder='Name'
                                maxLength ='255'
                                value = {name}
                                onChange={e => setName(e.target.value)}
                                required
                            />
                            <Form.Input
                                icon='user'
                                iconPosition='left'
                                label='Username'
                                placeholder='Username'
                                value = {username}
                                maxLength ='40'
                                onChange={e => setUsername(e.target.value)}
                                required
                            />
                            <Form.Input
                                icon='lock'
                                iconPosition='left'
                                label='Password'
                                placeholder='Password'
                                type='password'
                                value = {password}
                                onChange={e => setPassword(e.target.value)}
                                required
                            />
                            <Form.Select
                                fluid
                                label='Role'
                                placeholder='Role'
                                options={roles}
                                onChange={e => {
                                    setRole(e.currentTarget.textContent)
                                }}
                                required
                            />

                        </Form>
                    </Grid.Column>
                </Grid>
                </Modal.Content>
                <Modal.Actions>
                    <Button content='Register'
                                    primary onClick={() => {
                                        handleRegister()
                                    }}/>
                    <Button onClick={() => setOpen(false)}>Cancel</Button>
                </Modal.Actions>
            </Modal>
                <Modal
                centered={false}
                open={registerOpen}
                onClose={() => setRegisterOpen(false)}
                onOpen={() => setRegisterOpen(true)}
            >
                <Modal.Header>Unable to register</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        Please try another username and make sure all fields are filled.
                        <h1> </h1>
                    </Modal.Description>
                </Modal.Content>
                <Modal.Actions>
                    <Button onClick={() => setRegisterOpen(false)}>OK</Button>
                </Modal.Actions>
            </Modal>
            <Segment placeholder>

                    <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <Form>
                            <Form.Input
                                icon='user'
                                iconPosition='left'
                                label='Username'
                                placeholder='Username'
                                maxLength ='40'
                                value = {username}
                                onChange={e => setUsername(e.target.value)}
                                required
                            />
                            <Form.Input
                                icon='lock'
                                iconPosition='left'
                                label='Password'
                                type='password'
                                value = {password}
                                onChange={e => setPassword(e.target.value)}
                                required
                            />
                            <Button content='Login'
                                    primary onClick={() => {
                                        handleLogin()
                                    if (isAuth){
                                        navigate("/UserView")
                                    }

                                    }}/>
                        </Form>
                    </Grid.Column>
                    <Grid.Column verticalAlign='middle'>
                        <Button content='Sign up' icon='signup' size='big' onClick={handleChange}/>
                    </Grid.Column>
                </Grid>
                <Divider vertical>Or</Divider>


            </Segment>

        </Segment>
        )
    } else {
        return (<Navigate to="/UserView" />)
    }

}


export default HomePage;
