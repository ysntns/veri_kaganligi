import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const apiRequest = async (endpoint, method = 'GET', data = null) => {
  try {
    const config = {
      method,
      url: `${API_BASE_URL}${endpoint}`,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    if (data) {
      config.data = data;
    }

    const response = await axios(config);
    return response.data;
  } catch (error) {
    console.error(`API isteği hatası (${endpoint}):`, error);
    throw error;
  }
};