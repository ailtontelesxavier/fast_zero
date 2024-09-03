import axios from 'axios';
import { getSession } from "next-auth/react";

//const apiUrl = process.env.NEXTAUTH_BACKEND_URL //'http://127.0.0.1:8002'
const apiUrl = 'http://127.0.0.1:8002'

const api = axios.create({
    baseURL:apiUrl
})

api.interceptors.request.use(
    async (config) => {
      const session:any = await getSession();
      //console.log(session)
      //console.log(session.access_token)
      if (session && session?.access_token) {
        config.headers['Authorization'] = `Bearer ${session.access_token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

export default api

//https://axios-http.com/docs/interceptors