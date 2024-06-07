import 'vite/modulepreload-polyfill';

import * as React from "react";
import * as ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const route = createBrowserRouter([
    {
        path: "/",
        element: <div>Hello using React router</div>,
    },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
    <RouterProvider router={route} />
);