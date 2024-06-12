export default function ContactPage() {
  return (
    <div>
      <div>
        <img src="/static/analysis/img/radio-tower.jpg" alt="image of a radio tower"/>
      </div>
      <div>
        <h1>
          Hey! Feel free to reach out with any inquiries.
        </h1>
        <h2>
          Use the form below to send us a message and we will get back to you
          soon!
        </h2>

        <form
          action=""
          method="post"
        >
          <label>
            Name
            <input type="text" name="name"/>
          </label>
          <label>
            Email
            <input
              type="email"
              name="email"
            />
          </label>
          <label>
            Message
            <textarea name="name"/>
          </label>
          <button>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}