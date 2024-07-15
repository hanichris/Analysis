import { FormEvent, useRef } from "react";

export default function Contact() {
  const ref = useRef<HTMLDivElement>(null)

  const handleInput = (e: FormEvent<HTMLTextAreaElement>) => {
    if (ref.current) {
      ref.current.dataset.replicatedValue = e.currentTarget.value;
    }
  };

  return (
    <section className="section">
      <div className="container">
        <div className="post-comments">
          <header>
            <h3 className="section-title">Get in touch</h3>
            <p>Would you like to discuss your project and see how Divergent AG can help you? Fill the form and our team will contact you shortly.</p>
          </header>
          <form action="#" method="post">
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
                      pattern="[A-Za-zÀ-ž\s]{3,}"
                      maxLength={35}
                      required
                      accessKey="f"
                      autoComplete="on"
                      id="first-name" />
                  </span>
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
                      pattern="[A-Za-zÀ-ž\s]{3,}"
                      maxLength={40}
                      required
                      accessKey="l"
                      autoComplete="on"
                      id="last-name" />
                  </span>
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
                      pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
                      maxLength={55}
                      required
                      accessKey="e"
                      autoComplete="on"
                      id="email" />
                  </span>
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
                      pattern="[A-Za-zÀ-ž\s]{4,}"
                      maxLength={75}
                      required
                      accessKey="t"
                      autoComplete="on"
                      id="title" />
                  </span>
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
                </div>
              </div>
              <div className="form-group">
                <button type="submit" className="btn btn--m btn--primary">Submit</button>
              </div>
            </fieldset>
          </form>
        </div>
      </div>
    </section>
  );
}