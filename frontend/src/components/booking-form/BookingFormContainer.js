import React from 'react'

import { Container } from 'semantic-ui-react';

import { EventDetails } from './EventDetails'
import { EventInvitees } from './EventInvitees'
import { EventSchedule } from './EventSchedule'
import { EventLocation } from './EventLocation'
import {Success} from "./Success";

import { Form } from 'semantic-ui-react';

export class BookingFormContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            step: 1,
            title: '',
            description: '',
            date: '',
            account_id: [],
            start_time_id: '',
            end_time_id: '',
            room_id: ''
        }
    }



    handleSubmit = (e) => {
        e.preventDefault();
        //just show the success page (step 5 )
        this.setState((prevState) => {
            return {
                ...prevState,
                step: 5
            }
        })
    }




    handleChange = (event, { name, value, type }) => {

        if (type === 'checkbox') {
            // add checked to function if this is going to be used
            // generic solution for these checkboxes!!
            // let { interests } = this.state;
            // if (checked) {
            //     interests = [...interests, value]
            // }
            // else {
            //     interests = interests.filter((item) => item !== value);
            // }
            // this.setState((prevState) => {
            //     return {
            //         ...prevState,
            //         interests: interests
            //     }
            // })

        }
        else {
            this.setState((prevState) => {
                return {
                    ...prevState,
                    [name]: value
                }
            })
        }

    }

    next = () => {
        this.setState((prevState) => {
            return {
                ...prevState,
                step: prevState.step + 1
            }
        });
    }

    prev = () => {
        this.setState((prevState) => {
            return {
                ...prevState,
                step: prevState.step - 1
            }
        });
    }



    render() {
        const { step } = this.state;
        const { title, description, date, account_id, start_time_id, end_time_id, room_id } = this.state;
        const values = { title, description, date, account_id, start_time_id, end_time_id, room_id };

        return (
            <Container textAlign='left'>
                <Form onSubmit={this.handleSubmit}>
                    <Step step={step} values={values} handleChange={this.handleChange} next={this.next} prev={this.prev} />
                </Form>
            </Container>
        )
    }

}

const Step = ({ step, values, handleChange, next, prev }) => {
    switch (step) {
        case 1:
            console.log(values)
            return <EventDetails values={values}
                handleChange={handleChange} next={next}
            />
        case 2:
            console.log(values)
            return <EventInvitees values={values}
                handleChange={handleChange} next={next} prev={prev}
            />
        case 3:
            console.log(values)
            return <EventSchedule values={values}
                handleChange={handleChange} next={next} prev={prev}
            />
        case 4:
            return <EventLocation values={values}
                handleChange={handleChange} next={next} prev={prev}

            />
        case 5:
            return <Success values={values}
            />
        default:
            return null;
    }
}