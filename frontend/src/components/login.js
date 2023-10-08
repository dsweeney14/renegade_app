import React from "react";
import { Form, Button } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { login } from "../auth";
import { useAuthContext } from "../authContext";
import axios from "axios";

import "../styles/login.css";

// This file contains the login functionality. 

const LoginForm = () => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm();

  const navigate = useNavigate();
  const auth = useAuthContext();

  const SubmitLoginForm = (data) => {
    axios
      .post("/auth/login", data)
      .then((response) => {
        const { access_token, refresh_token, user_id } = response.data;
        sessionStorage.setItem("userId", user_id)
        auth.loginContext(access_token, refresh_token);
        login(access_token);
        navigate("/dashboard");
      })
      .catch((error) => {
        console.error(error);
      });
    reset();
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault(); 
      handleSubmit(SubmitLoginForm)();
    }
  };

  return (
    <div className="main-login">
      <div className="container-login">
        <h1 className="heading">Login</h1>
        <br></br>
        <div className="form">
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
              {errors.password && (
                <p style={{ color: "red" }}>
                  <small>Password is required</small>
                </p>
              )}
            </Form.Group>

            <div className="button-wrapper">
              <Form.Group>
                <Button
                  className="button"
                  as="sub"
                  variant="primary"
                  onClick={handleSubmit(SubmitLoginForm)}
                >
                  Login
                </Button>
              </Form.Group>
            </div>

            <Form.Group>
              <small className="link">
                Not registered?{" "}
                <Link to="/register">Create an account here.</Link>
              </small>
            </Form.Group>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
