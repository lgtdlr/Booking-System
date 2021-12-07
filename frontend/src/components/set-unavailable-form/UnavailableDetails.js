import React from 'react'
import { Form, Button, Input } from 'semantic-ui-react';


const UnavailableDetails = (props) => {
    const { date } = props.values;


    return (

        <React.Fragment>
            <h1 className="ui centered">Event Details</h1>
                <Form.Input
                icon='calendar outline'
                iconPosition='left'
                type="date"
                name="date"
                label='Date'
                value = {date}
                onChange={props.handleChange}
                required
                />

            <Button onClick={props.next}>Next</Button>
        </React.Fragment>


    );
}


export { UnavailableDetails };