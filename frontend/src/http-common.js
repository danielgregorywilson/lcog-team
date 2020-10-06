import axios from 'axios';

export default axios.create({
  // baseURL: 'http://localhost:8000/',
  baseURL: 'http://lcog-internal-env.eba-4t9yrmiu.us-west-2.elasticbeanstalk.com/',
  headers: {
    'Content-type': 'application/json'
  }
});
