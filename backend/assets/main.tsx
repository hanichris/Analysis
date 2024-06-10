import 'vite/modulepreload-polyfill';

import * as ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import ErrorPage from './error-page';
import Root from './routes/root';
import AboutPage from './routes/about';

import "./home.css";

const route = createBrowserRouter([
    {
        path: "/",
        element: <Root />,
        errorElement: <ErrorPage />,
        children: [
            {
                path: "",
                element: <div>Home page</div>,
            },
            {
                path: "about",
                element: <AboutPage />,
            },
            {
                path: "contact",
                element: <div>Contact page</div>,
            },
        ],
    },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
    <RouterProvider router={route} />
);