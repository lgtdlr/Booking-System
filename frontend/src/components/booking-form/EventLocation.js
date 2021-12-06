import React, {useEffect, useState} from 'react'
import {Form, Button, Dimmer, Loader} from 'semantic-ui-react';
import axios from "axios";
import _ from "lodash";


let timeslots = [];

export async function getRooms(date, start_time_id, end_time_id) {

    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const requestOptions = {
        headers: { Authorization: "Bearer " + token }
    };
    const json = {
        date: date,
        start_time_id: start_time_id,
        end_time_id: end_time_id
    };
    console.log(json)
    await axios.post(url + '/room/find-available-room', json, requestOptions)
      .then(function (response) {
        timeslots = response.data;

      })
}

const EventLocation = (props) => {
  const { date, start_time_id, end_time_id } = props.values;
  const [isLoading, setIsLoading] = useState(true);
  const [allRooms, setAllRooms] = useState(timeslots);

  const roomOptions = _.map(allRooms, (name, index) => ({
        key: allRooms[index].name,
        text: allRooms[index].type + " : " + allRooms[index].name + " (  Max. capacity: " + allRooms[index].capacity + " )",
        value: allRooms[index].room_id,
    }));


  useEffect(() => {
        getRooms(date, start_time_id, end_time_id).then(_ => {
        setIsLoading(false);
        setAllRooms(timeslots);
    });
    }, []);


  return (

    <React.Fragment>
      <h1 className="ui centered">Location</h1>
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
            options= {roomOptions }
            onChange={props.handleChange}
            required
        />



        <Button onClick={props.prev}>Back</Button>
        {/*<Button onClick={props.next}>Next</Button>*/}
      <Button color='blue' type='submit' >Submit</Button>

    </React.Fragment>

  );
}


export { EventLocation };