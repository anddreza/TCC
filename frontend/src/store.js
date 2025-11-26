import { configureStore } from "@reduxjs/toolkit"
import { setupListeners } from "@reduxjs/toolkit/query"
import { llmApi } from "./servies_properties"

export const store = configureStore({
  reducer: {
    [llmApi.reducerPath]: llmApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(llmApi.middleware),
})

setupListeners(store.dispatch)