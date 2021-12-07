import React from 'react'
import { Form, Button, Input } from 'semantic-ui-react';


const EditEventDetails = (props) => {
    const { title, description, date } = props.values;


    return (

        <React.Fragment>
            <h1 className="ui centered">Edit event details</h1>
                <Form.Field
                    control={Input}
                    icon='gg'
                    name='title'
                    iconPosition='left'
                    label='Title'
                    placeholder='Title'
                    maxLength ='50'
                    value = {title}
                    onChange={props.handleChange}
                    required
                />
                <Form.Field
                    control={Input}
                    name='description'
                    icon='sticky note outline'
                    iconPosition='left'
                    label='Description'
                    placeholder='Description'
                    maxLength ='400'
                    value = {description}
                    onChange={props.handleChange}
                    required
                />
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


export { EditEventDetails };