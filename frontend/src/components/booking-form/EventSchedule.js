import React, {useEffect, useState} from 'react'
import {Form, Button, Dimmer, Loader} from 'semantic-ui-react';
import axios from "axios";
import _ from "lodash";


let timeslots = [];

export async function getTimeslots(date, account_id) {

    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const requestOptions = {
        headers: { Authorization: "Bearer " + token }
    };
    const json = {
        account_ids: account_id,
        dates: date,
    };
    console.log(json)
    await axios.post(url + '/account/find-available-time', json, requestOptions)
      .then(function (response) {
        timeslots = response.data;

      })
}

const EventSchedule = (props) => {
  const { date, account_id, start_time_id, end_time_id } = props.values;
  const [isLoading, setIsLoading] = useState(true);
  const [allTimeslots, setAllTimeslots] = useState(timeslots);

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


  useEffect(() => {
        getTimeslots(date, account_id).then(_ => {
        setIsLoading(false);
        setAllTimeslots(timeslots);
    });
    }, []);


  return (

    <React.Fragment>
      <h1 className="ui centered">Schedule</h1>
        {isLoading === true && <Dimmer active={isLoading} inverted>
            <Loader>Please wait</Loader>
        </Dimmer>}
        <Form.Group>
            <Form.Dropdown
          fluid
          search
          selection
          label='Start time'
          name='start_time_id'
          value={start_time_id}
          placeholder='00:00:00'
          options= {timeslotOptions }
          onChange={props.handleChange}
      />
            <Form.Dropdown
          fluid
          search
          selection
          label='End time'
          name='end_time_id'
          value={end_time_id}
          placeholder='00:00:00'
          options= {endTimeslotOptions }
          onChange={props.handleChange}
      />
        </Form.Group>



        <Button onClick={props.prev}>Back</Button>
        <Button onClick={props.next}>Next</Button>
      {/*<Button color='blue' type='submit' >Submit</Button>*/}

    </React.Fragment>

  );
}


export { EventSchedule };