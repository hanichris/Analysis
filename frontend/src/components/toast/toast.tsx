import { useEffect } from "react";

interface IResponse {
  msg?: string;
  type?: "info" | "success" | "error";
  notify: boolean;
};

interface IToast {
  type: "success" | "error" | "info" ;
  message?: string;
  children: React.Dispatch<React.SetStateAction<IResponse>>;
}

const toastTypes = {
  success: {
    type: "success",
    element: (
      <svg width="22px" height="22px" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
        <path fill="currentColor" d="M512 64a448 448 0 1 1 0 896 448 448 0 0 1 0-896zm-55.808 536.384-99.52-99.584a38.4 38.4 0 1 0-54.336 54.336l126.72 126.72a38.272 38.272 0 0 0 54.336 0l262.4-262.464a38.4 38.4 0 1 0-54.272-54.336L456.192 600.384z"/>
      </svg>
    ),
  },
  error: {
    type: "error",
    element: (
      <svg width="22px" height="22px" viewBox="0 0 512 512" version="1.1" xmlns="http://www.w3.org/2000/svg">
        <g id="Page-1" stroke="none" strokeWidth="1" fill="none" fillRule="evenodd">
          <g id="add" fill="currentColor" transform="translate(42.666667, 42.666667)">
            <path d="M213.333333,3.55271368e-14 C331.136,3.55271368e-14 426.666667,95.5306667 426.666667,213.333333 C426.666667,331.136 331.136,426.666667 213.333333,426.666667 C95.5306667,426.666667 3.55271368e-14,331.136 3.55271368e-14,213.333333 C3.55271368e-14,95.5306667 95.5306667,3.55271368e-14 213.333333,3.55271368e-14 Z M262.250667,134.250667 L213.333333,183.168 L164.416,134.250667 L134.250667,164.416 L183.168,213.333333 L134.250667,262.250667 L164.416,292.416 L213.333333,243.498667 L262.250667,292.416 L292.416,262.250667 L243.498667,213.333333 L292.416,164.416 L262.250667,134.250667 Z" id="Combined-Shape"></path>
          </g>
        </g>
      </svg>
    ),
  },
  info: {
    type: "info",
    element: (
      <svg width="22px" height="22px" viewBox="0 0 512 512" version="1.1" xmlns="http://www.w3.org/2000/svg">
        <g id="Page-1" stroke="none" strokeWidth="1" fill="none" fillRule="evenodd">
          <g id="add" fill="currentColor" transform="translate(42.666667, 42.666667)">
            <path d="M213.333333,3.55271368e-14 C330.943502,3.55271368e-14 426.666667,95.7231591 426.666667,213.333333 C426.666667,330.943502 330.943502,426.666667 213.333333,426.666667 C95.7231591,426.666667 3.55271368e-14,330.943502 3.55271368e-14,213.333333 C3.55271368e-14,95.7231591 95.7231591,3.55271368e-14 213.333333,3.55271368e-14 Z M213.333333,272.042667 C198.095238,272.042667 186.666667,283.306667 186.666667,298.325333 C186.666667,314.026667 197.748918,325.290667 213.333333,325.290667 C228.571429,325.290667 240,314.026667 240,298.666667 C240,283.306667 228.571429,272.042667 213.333333,272.042667 Z M234.666667,85.3333333 L192,85.3333333 L192,234.666667 L234.666667,234.666667 L234.666667,85.3333333 Z" id="Combined-Shape"></path>
          </g>
        </g>
      </svg>
    ),
  },
};


export default function Toast(props: IToast) {
  const svg = toastTypes[props.type];

  useEffect(() => {
    const timerId = setTimeout(() => {
      props.children({
        notify: false,
        msg: undefined,
        type: undefined,
      });
    }, 2500);

    return () => clearTimeout(timerId);
  }, []);

  return (
    <div className={`toast toast--${svg.type} is-visible`}>
      <div className="toast_inner">
        { svg.element }
        <span>{ props.message }</span>
      </div>
    </div>
  );
}