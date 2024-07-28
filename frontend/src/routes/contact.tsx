import { FormEvent, useRef, useState } from "react";
import { z } from "zod";
import { handleZodValidation, ValidationError } from "../utils/error_handling";
import ToastContainer from "../components/toast/toastcontainer";


interface IResponse {
  msg?: string;
  type?: "info" | "success" | "error";
  notify: boolean;
};

const invalid_type_error = "Invalid type provided for this field.";
const required_error = "This field cannot be blank.";

const contactSchema = z.object({
  first_name: z
    .string({
      invalid_type_error,
      required_error,
    })
    .min(1, { message: required_error })
    .min(3, "First name entry is too short")
    .max(35, "First name entry is too long")
    .regex(/[A-Za-zÀ-ž\s]/),
  last_name: z
    .string({
      invalid_type_error,
      required_error,
    })
    .min(3, "Last name entry is too short")
    .max(40, "Last name entry is too long")
    .regex(/[A-Za-zÀ-ž\s]/),
  email: z
    .string({
      invalid_type_error,
      required_error,
    })
    .email("Please provide a valid email")
    .min(1, "Email address entry is too short")
    .max(55, "Email address entry is too long"),
  title: z
    .string({
      invalid_type_error,
      required_error,
    })
    .min(4, "Title entry is too short")
    .max(70, "Title entry is too long")
    .regex(/[A-Za-zÀ-ž\s]/),
  comment: z
    .string({
      invalid_type_error,
      required_error,
    })
    .min(10, "Comment should be at least 10 characters long"),
});


export default function Contact() {
  const [errors, setErrors] = useState<ValidationError<typeof contactSchema>>({});
  const [response, setResponse] = useState<IResponse>({notify: false});
  const [loading, setLoading] = useState<Boolean>(false);
  const ref = useRef<HTMLDivElement>(null)

  const handleInput = (e: FormEvent<HTMLTextAreaElement>) => {
    if (ref.current) {
      ref.current.dataset.replicatedValue = e.currentTarget.value;
    }
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const csrftoken = document.querySelector<HTMLInputElement>('[name=csrfmiddlewaretoken]')?.value;
    const headers: HeadersInit = new Headers({
      'Accept': "application/json",
      'Content-Type': "application/json",
      'X-Requested-With': "XMLHttpRequest",
    });
    if (csrftoken) {
      headers.set('X-CSRFToken', csrftoken);
    }
    
    const data = Object.fromEntries(new FormData(e.currentTarget));


      handleZodValidation({
        onError: setErrors,
        data: data,
        onSuccess: async (res, timeout = 5000) => {
          setErrors({});
          const controller = new AbortController();
          const timeoutSignal = AbortSignal.timeout(timeout);
          try {
            setLoading(true);

            const resp = await fetch("/", {
              method: "POST",
              body: JSON.stringify(res),
              headers,
              mode: "same-origin",
              signal: AbortSignal.any([controller.signal, timeoutSignal]),
            });
  
            switch (resp.status) {
              case 201:
              case 400:
              case 500:
                const respData:IResponse = await resp.json()
                setResponse({
                  ...respData,
                  notify: true,
                });
                break;
              case 404:
                setResponse({
                  msg: "An error occurred, 404 (Not found)",
                  type: "info",
                  notify: true,
                });
                break;
              default:
                setResponse({
                  msg: "A problem occurred, please try again.",
                  type: "error",
                  notify: true,
                });
                break;
            }
            setLoading(false);

          } catch (error) {
            setLoading(false);
            setResponse({
              msg: "A network error occurred.",
              type: "info",
              notify: true
            });
          }
        },
        schema: contactSchema,
      });
  };

  return (
    <section className="section">
      <div className="container">
        <div className="post-comments">
          <header>
            <h3 className="section-title">Get in touch</h3>
            <p>Would you like to discuss your project and see how Divergent AG can help you? Fill the form and our team will contact you shortly.</p>
          </header>
          <form action="#" method="post" onSubmit={handleSubmit} noValidate>
          { (Object.keys(errors).length > 0) && <p className="fieldErrors"> Please review the following errors and resubmit the form</p>}
            <fieldset>
              <legend className="visually-hidden">
                Your personal information
              </legend>
              <div className="form-group">
                <label htmlFor="first-name">
                  First Name:
                </label>
                <div className="form-field">
                  <span className="form-field-container">
                    <input
                      type="text"
                      name="first_name"
                      placeholder="e.g Kgauhelo"
                      maxLength={35}
                      required
                      accessKey="f"
                      autoComplete="on"
                      id="first-name" />
                      <i className="form-field-icon"></i>
                  </span>
                  { errors.first_name ?
                    <p className="form-error">{ errors.first_name }</p>
                    : <p className="form-help">
                        First name should be at least 3 characters and only contains letters.
                      </p>
                  }
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="last-name">
                  Last Name:
                </label>
                <div className="form-field">
                  <span className="form-field-container">
                    <input
                      type="text"
                      name="last_name"
                      placeholder="e.g Hani"
                      maxLength={40}
                      required
                      accessKey="l"
                      autoComplete="on"
                      id="last-name" />
                      <i className="form-field-icon"></i>
                  </span>
                  { errors.last_name ?
                    <p className="form-error">{ errors.last_name }</p>
                    : <p className="form-help">
                        Last name should be at least 3 characters and only contains letters.
                      </p>
                  }
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="email">
                  Email:
                </label>
                <div className="form-field">
                  <span className="form-field-container">
                    <input
                      type="email"
                      name="email"
                      placeholder="e.g youremail@gmail.com"
                      maxLength={55}
                      required
                      accessKey="e"
                      autoComplete="on"
                      id="email" />
                      <i className="form-field-icon"></i>
                  </span>
                  {errors.email ?
                    <p className="form-error">{ errors.email }</p>
                    : <p className="form-help">
                        Email entered should be a valid email address.
                      </p>
                  }
                </div>
              </div>
            </fieldset>
            <fieldset>
              <legend className="visually-hidden">
                Your post
              </legend>
              <div className="form-group">
                <label htmlFor="title">
                  Subject:
                </label>
                <div className="form-field">
                  <span className="form-field-container">
                    <input
                      type="text"
                      name="title"
                      placeholder="e.g I need help with"
                      maxLength={75}
                      required
                      accessKey="t"
                      autoComplete="on"
                      id="title" />
                      <i className="form-field-icon"></i>
                  </span>
                  {errors.title ?
                    <p className="form-error">{ errors.title }</p>
                    : <p className="form-help">
                        Title should be at least 4 characters and only contains letters
                      </p>
                  }
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="comment">
                  Project Information:
                </label>
                <div className="form-field grow-wrap" ref={ref}>
                  <textarea
                    name="comment"
                    placeholder="Please share more about your wants & needs so we can direct your inquiry to the right internal resource."
                    accessKey="c"
                    required
                    onInput={handleInput}
                    id="comment"></textarea>
                  {errors.comment ?
                    <p className="form-error">{ errors.comment }</p>
                    : <p className="form-help">
                        Comment should be at least 10 characters
                      </p>
                  }
                </div>
              </div>
              <div className={loading ? "form-group is-submitting" : "form-group"}>
                <button type="submit" className="btn btn--m btn--primary">Submit</button>
              </div>
            </fieldset>
          </form>
        </div>
      </div>
      <ToastContainer>
        { {response, dispatch: setResponse} }
      </ToastContainer>
    </section>
  );
}