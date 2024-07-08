import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";

import "./modal.css"

interface IModal {
  toggle: boolean;
  setToggle: () => void;
}

export default function SignInSignUp({
  toggle,
  setToggle,
}: IModal) {

  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let timeoutId = undefined;
    const body = document.querySelector("body");
    if (toggle) {
      timeoutId = setTimeout(() => {
        if (ref.current && body) {
          ref.current.className = "modal_element animate";
          body.className = "has-modal";
        }
      }, 3);
    } else {

      if (ref.current && body) {
        ref.current.className = "modal_element";
        body.className = "";
      }
    }

    return () => clearTimeout(timeoutId);
  }, [toggle]);

  return (
    <div
      className={toggle ? "modal is-visible" : "modal"}
      style={toggle ? {"display": "block"}: {}}
      >
      <div className="modal_container">
        <div className="modal_cell">
          <div
            ref={ref}
            className="modal_element">
            <div className="modal_title">
              <h2>Hello!</h2>
              <div>Use your email or another service to continue with Analysis.</div>
            </div>
            <button type="button" className="modal_button" onClick={setToggle}>
                <svg width="22" height="22" viewBox="1 1 22 22" focusable="false">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"></path>
                </svg>
            </button>
            <div className="modal_body">
              <a href="/accounts/login" className="btn btn--m btn--gray _m-b-2 btn--with-icon">
                <i className="icon">
                  <svg fill="#000000" height="800px" width="800px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" 
	 viewBox="0 0 210 210">
    <path d="M0,105C0,47.103,47.103,0,105,0c23.383,0,45.515,7.523,64.004,21.756l-24.4,31.696C133.172,44.652,119.477,40,105,40
	c-35.841,0-65,29.159-65,65s29.159,65,65,65c28.867,0,53.398-18.913,61.852-45H105V85h105v20c0,57.897-47.103,105-105,105
	S0,162.897,0,105z"/>
</svg>
                </i>
                <span>Continue with Google</span>
              </a>
              <a href="/accounts/login" className="btn btn--m btn--primary">
                Continue with email
              </a>
              <div className="small-text _m-t-3">
                By continuing, you agree to our <Link to={"tos"}>Terms of Service</Link>.
                <br />
                Read our <Link to={"privacy"}>Privacy Policy</Link>.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}