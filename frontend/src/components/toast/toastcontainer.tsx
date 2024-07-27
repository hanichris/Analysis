import Toast from "./toast";

interface IResponse {
  msg?: string;
  type?: "info" | "success" | "error";
  notify: boolean;
};

interface Children {
  response: IResponse;
  dispatch: React.Dispatch<React.SetStateAction<IResponse>>;
}

type ToastProp = {
  children: Children;
}

export default function ToastContainer(props: ToastProp) {
  const { response, dispatch } = props.children;
  return (
    <div className="toast-container" style={ response.notify ? {"display": "flex"} : {"display": "none"}}>
      {
         (response.type && response.notify) &&
        <Toast type={response.type} message={response.msg}>
          { dispatch }
        </Toast>
      }
    </div>
  );
}