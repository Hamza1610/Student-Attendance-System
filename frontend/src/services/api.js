import axios from 'axios';

// Create an apiClient instance
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/', // Default base URL
});

// Use the instance for requests
apiClient.get('/') // Equivalent to 'http://your-backend-api-url.com/api/students'
  .then((response) => console.log(response.data))
  .catch((error) => console.error(error));

// You can also use this instance in your components
export default apiClient;
