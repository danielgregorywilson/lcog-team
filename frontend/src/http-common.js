import axios from 'axios';

export default axios.create({
  baseURL: process.env.API_URL,
  headers: {
    'Content-type': 'application/json',
    'Authorization': 'Token 05c5ab7d90b00e4278ec37ffb8394953e4a8c97e'
  }
});
