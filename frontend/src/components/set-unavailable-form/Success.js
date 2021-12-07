import React, {useEffect, useState} from 'react';
import axios from "axios";
import {Button, Dimmer, Image, Loader} from "semantic-ui-react";

let book = {};

export async function setUnavailable(date, start_time_id, end_time_id, availability) {

    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const requestOptions = {
        headers: { Authorization: "Bearer " + token}
    };
    const booking = {
            date: date,
            start_time_id: start_time_id,
            end_time_id: end_time_id,
            is_available: false
        }
    console.log(booking)
    await axios.post(url + '/account/set-availability', booking, requestOptions)
      .then(function (response) {
        book = response.data;
      })
}

const Success = (props) => {
    const { date, start_time_id, end_time_id, availability } = props.values;
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        setUnavailable(date, start_time_id, end_time_id, availability).then(_ => {
        setIsLoading(false);
    });
    }, []);

return (
    <React.Fragment>
      <h1 className="ui centered">Form submitted</h1>
        {isLoading === true && <Dimmer active={isLoading} inverted>
            <Loader>Please wait</Loader>
        </Dimmer>}
        {/*<div>*/}
        {/*        <h1 className="ui centered">Form Submitted</h1>*/}
        {/*        <div>*/}
        {/*           <pre>{JSON.stringify(props.values, null, 2)}</pre>*/}
        {/*        </div>*/}
        {/*    </div>*/}
        <Image src='https://i.pinimg.com/originals/70/a5/52/70a552e8e955049c8587b2d7606cd6a6.gif' size='medium' circular={true} fluid={true} centered={true} verticalAlign={"middle"}/>
        <h1> </h1>
        <Button fluid={true} animated={true}  content='OK'
                primary onClick={() => {
                    window.location.reload(false);
                }}/>
    </React.Fragment>



    )
}





export {Success}

