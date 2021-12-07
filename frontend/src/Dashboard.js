import React, {Component, useEffect, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Header, Image, List, Modal} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import axios from "axios";

let mostBookingsWith = [];

async function getMostBookingWithSelectedUser() {
    const token = sessionStorage.getItem("token");
    const url = "http://127.0.0.1:5000/redpush";
    const requestOptions = {
        headers: { Authorization: "Bearer " + token }
    };
    await axios.get(url+'/account/bookings-with-user', requestOptions).then(function
        (response) {
        mostBookingsWith = response.data
    })
}

function BookMeeting(){

    const [data, setData] = useState([]);
    useEffect(() => {
        getMostBookingWithSelectedUser().then(  () => {
            setData(mostBookingsWith)
            console.log("Bookings with" + mostBookingsWith)
        })

    }, [])

    // return <Container style={{ height: 800 }}>
    //
    //     <BarChart width={730} height={250} data={data}>
    //         <CartesianGrid strokeDasharray="3 3" />
    //         <XAxis dataKey="name" />
    //         <YAxis />
    //         <Tooltip />
    //         <Legend />
    //         <Bar dataKey="Counts" fill="#8884d8" />
    //     </BarChart>
    // </Container>

  // return <ul>
  //       {data.map(item => (
  //         <li key={item.account_id}>
  //           <div>{item.name}</div>
  //           <div>{item.Counts}</div>
  //         </li>
  //       ))}
  //     </ul>

// return (
//
//     <List horizontal ordered> {data.map (item => (<List.Item key={item.account_id}>
//       <Image avatar src='https://react.semantic-ui.com/images/avatar/small/tom.jpg' />
//       <List.Content>
//         <List.Header>{item.name}</List.Header>
//           {item.Counts}
//       </List.Content>
//     </List.Item>))}
//   </List>)

    return (
        <div><Header as='h1'> You share a maximum of {data[0].Counts} bookings with these users </Header>
        <List horizontal ordered> {data.map (item=> (<List.Item key={item.account_id}>
      <Image avatar src='https://react.semantic-ui.com/images/avatar/small/tom.jpg' />
      <List.Content>
        <List.Header>{item.name}</List.Header>

      </List.Content>
    </List.Item>))}
  </List>
        </div>

    )

}
export default BookMeeting;
