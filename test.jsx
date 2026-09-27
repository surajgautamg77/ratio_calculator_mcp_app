import { useRef } from "react";

function UserForm() {
  const nameRef = useRef(null);
  const emailRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();

    const name = nameRef.current.value;
    const email = emailRef.current.value;

    console.log("Name:", name);
    console.log("Email:", email);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name:</label>
        <input type="text" ref={nameRef} />
      </div>

      <div>
        <label>Email:</label>
        <input type="email" ref={emailRef} />
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}

export default UserForm;
