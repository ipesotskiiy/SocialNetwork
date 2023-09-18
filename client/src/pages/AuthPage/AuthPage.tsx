import React from "react";
import AuthForm from "../../components/auth/AuthForm";
import styles from "./AuthPage.module.scss";

const handleSubmit = (username: string, password: string) => {
  // Ваша логика аутентификации здесь, например, отправка запроса на сервер
  console.log("Username:", username);
  console.log("Password:", password);
};

const AuthPage = () => {
  return (
    <div className={styles.mainContainer}>
      <AuthForm onSubmit={handleSubmit} />
    </div>
  );
};

export default AuthPage;
