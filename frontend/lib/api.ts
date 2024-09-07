import apiUrl from '@/app/api/auth/[...nextauth]/route';
import axios from 'axios';
import { getSession } from "next-auth/react";


const api = axios.create({
    baseURL:apiUrl
})

api.interceptors.request.use(
    async (config) => {
      const session:any = await getSession();
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