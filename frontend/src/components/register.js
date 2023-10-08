import React, { useState } from "react";
import { Form, Button, Alert } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import axios from "axios";

import "../styles/register.css";

// This file contains the functionality for user registration

const RegisterForm = () => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm();

  const [showError, setShowError] = useState(false);
  const [showAccess, setShowAccess] = useState(false);
  const [serverResponse, setServerResponse] = useState("");

  const navigate = useNavigate();

  const SubmitRegisterForm = (data) => {
    const body = {
      username: data.username,
      email: data.email,
      password: data.password,
    };

    if (data.password === data.confirmPassword) {
      axios
        .post("/auth/register", body) 
        .then((response) => {
          const { data } = response;
          console.log(data);
          setServerResponse(data.message);
          if (data[1] === 401) {
            setShowError(true);
          } else {
            setShowAccess(true);
            navigate("/login"); 
          }
        })
        .catch((error) => console.log(error));
    }

    reset();
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault(); 
      handleSubmit(SubmitRegisterForm)();
    }
  };

  return (
    <main className="main-register">
      <div className="container-register">
      <h1 className="heading">Register a new account</h1>
        <br></br>
        <div className="form">
          {showError && (
            <>
              <Alert
                variant="danger"
                onClose={() => setShowError(false)}
                dismissible
              >
                <p>{serverResponse}</p>
              </Alert>
              <h1 className="heading">Register a new account</h1>
            </>
          )}
          {showAccess && (
            <>
              <Alert
                variant="success"
                onClose={() => setShowAccess(false)}
                dismissible
              >
                <p>{serverResponse}</p>
              </Alert>
              <h1 className="heading">Register a new account</h1>
            </>
          )}
          {!showAccess && !showError && (
            <h1 className="heading">Register a new account</h1>
          )}

          <form onKeyDown={handleKeyDown}>
            <Form.Group>
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter username here"
                {...register("username", { required: true, maxLength: 25 })}
              />
              {errors.username && (
                <p style={{ color: "red" }}>
                  <small>Username is required.</small>
                </p>
              )}
              {errors.username?.type === "maxLength" && (
                <p style={{ color: "red" }}>
                  <small>Username must not be longer than 25 characters.</small>
                </p>
              )}
              {/*error validation here against existing users in the database*/}
            </Form.Group>

            <Form.Group>
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email here"
                {...register("email", {
                  required: true,
                  maxLength: 100,
                  pattern: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+[a-zA-Z]{2,}/,
                })}
              />
              {errors.email && (
                <p style={{ color: "red" }}>
                  <small>Email is required.</small>
                </p>
              )}
              {errors.email?.type === "maxLength" && (
                <p style={{ color: "red" }}>
                  <small>
                    Username must not be longer than 100 characters.
                  </small>
                </p>
              )}
              {/*add some regex error validation here*/}
            </Form.Group>

            <Form.Group>
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="**********"
                {...register("password", {
                  required: true,
                  minLength: 8,
                  pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*).{8,}$/,
                })}
              />
              {errors.password?.type === "required" && (
                <p style={{ color: "red" }}>
                  <small>Password is required.</small>
                </p>
              )}
              {errors.password?.type === "minLength" && (
                <p style={{ color: "red" }}>
                  <small>Password must have 8 characters.</small>
                </p>
              )}
              {/*add some regex error validation here*/}
            </Form.Group>

            <Form.Group>
              <Form.Label>Confirm Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="**********"
                {...register("confirmPassword", { required: true })}
              />
              {errors.confirmPassword && (
                <p style={{ color: "red" }}>
                  <small>Confirm Password is required.</small>
                </p>
              )}
              {errors.password?.type === "minLength" && (
                <p style={{ color: "red" }}>
                  <small>Confirm Password must have 8 characters.</small>
                </p>
              )}
              {/*add some error validation here against the password field*/}
            </Form.Group>
            <br></br>

                <div className="button-wrapper-register">
                  <Form.Group>
              <Button
                className="button"
                as="sub"
                variant="primary"
                onClick={handleSubmit(SubmitRegisterForm)}
              >
                Submit
              </Button>
            </Form.Group>

                </div>
            
            <Form.Group>
              <small>
                Already registered?{" "}
                <Link to="/login">Log into your account here.</Link>
              </small>
            </Form.Group>
          </form>
        </div>
      </div>
    </main>
  );
};

export default RegisterForm;
