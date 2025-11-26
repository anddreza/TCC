import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

export const llmApi = createApi({
  reducerPath: "llmApi",
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.REACT_APP_API_URL || "http://localhost:8000",
    credentials: "include", // include cookies in requests
  }),
  endpoints: (build) => ({
    getProperties: build.query({
      query: (user_preferences) => ({ url: `/properties`, 
        params: { user_preferences } }),
    }),
    getPropertiesById: build.query({
      query: (id) => ({ url: `/properties/${id}` }),
    }),
  }),
})

//hook generated for usage in functional components
export const { useLazyGetPropertiesQuery, useGetPropertiesByIdQuery } = llmApi