import { useRouteError } from "react-router-dom";

type Error = {
  statusText?: string;
  message: string;
};

export default function ErrorPage() {
  const error = useRouteError() as Error;

  return (
    <div id="error-page">
      <div className="container">
        <h1>Oops!</h1>
        <p>Sorry, an unexpected error has occurred.</p>
        <p className="error--type">
          {error.statusText || error.message}
        </p>
      </div>
    </div>
  );
}