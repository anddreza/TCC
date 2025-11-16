import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"
// Define a service using a base URL and expected endpoints


export const llmApi = createApi({
  reducerPath: "llmApi",
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.REACT_APP_API_URL || "http://localhost:8000",
    credentials: "include",
  }),
  endpoints: (build) => ({
    getProperties: build.query({
      query: (user_preferences) => ({ url: `/properties`, params: { user_preferences } }),
    }),
    getPropertiesById: build.query({
      query: (id) => ({ url: `/properties/${id}` }),
    }),
  }),
})

// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const { useLazyGetPropertiesQuery, useGetPropertiesByIdQuery } = llmApi