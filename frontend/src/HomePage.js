import React, {Component, useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import {Route, Navigate, BrowserRouter, Routes, useNavigate} from 'react-router-dom';


function HomePage() {
    const url = 'http://127.0.0.1:5000/redpush'
    const [open, setOpen] = useState(false);
    const [token, setToken] = useState(sessionStorage.getItem("token"));
    const [isAuth, setIsAuth] = useState(!!(token && token !== "undefined"));
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");


    const navigate = useNavigate()
    const handleChange = (event, newValue) => {
        setOpen(true);
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

    if (!isAuth) {
        return (
            <Segment><Header dividing textAlign="center" size="huge">Welcome to DB Demo</Header>
            <Modal
                centered={false}
                open={open}
                onClose={() => setOpen(false)}
                onOpen={() => setOpen(true)}
            >
                <Modal.Header>Needs changing!</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        This is a modal but it serves to show how buttons and functions can be implemented.
                    </Modal.Description>
                    <Grid columns={1} relaxed='very' stackable>
                    <Grid.Column>
                        <Form>
                            <Form.Input
                                icon='user'
                                iconPosition='left'
                                label='Username'
                                placeholder='Username'
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
                            <Button content='Register'
                                    primary onClick={() => {
                                        handleLogin()
                                        navigate("/userview")
                                    }}/>
                        </Form>
                    </Grid.Column>
                </Grid>
                </Modal.Content>
                <Modal.Actions>
                    <Button onClick={() => setOpen(false)}>OK</Button>
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
