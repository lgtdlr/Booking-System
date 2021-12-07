import React, {useEffect, useState} from 'react'
import {Form, Button, Loader, Dimmer} from 'semantic-ui-react';
import axios from "axios";
import _ from "lodash";

let users = [];

export async function getUsers() {

    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const requestOptions = {
        headers: { Authorization: "Bearer " + token }
    };
    await axios.get(url + '/account', requestOptions)
      .then(function (response) {
          // console.log(response.data)
        users = response.data;
        users = users[0]

      })
}


const EventInvitees = (props) => {


    const { account_id } = props.values;
    const [isLoading, setIsLoading] = useState(true);
    const [allUsers, setAllUsers] = useState(users);
    const userOptions = _.map(allUsers, (username, index) => ({
        key: allUsers[index].username,
        text: allUsers[index].username + " ( " + allUsers[index].full_name + " )",
        value: allUsers[index].account_id,
    }));

    useEffect(() => {
        getUsers().then(_ => {
        setIsLoading(false);
        setAllUsers(users);
    });
    }, []);


  return (

    <React.Fragment>
      <h1 className="ui centered">Invitations</h1>
        {isLoading === true && <Dimmer active={isLoading} inverted>
            <Loader>Please wait</Loader>
        </Dimmer>}

        <Form.Dropdown
          fluid
          search
          multiple
          selection
          name='account_id'
          label='Invite users'
          value={account_id}
          placeholder='User(s)'
          options= {userOptions }
          onChange={props.handleChange}
      />


      <Button onClick={props.prev}>Back</Button>
      <Button onClick={props.next}>Next</Button>
    </React.Fragment>


  );
}


export { EventInvitees };