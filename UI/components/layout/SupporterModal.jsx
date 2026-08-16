"use client"

import { useRef } from "react";

export default function SupporterModal({modal, showModal, closeModal, login}){

  const checkRegex = ()=>{
    const phoneRegex = /^09\d{9}$/;
    const emailRegex =  /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if(phoneRegex.test(emailRef.current.value) || emailRegex.test(emailRef.current.value)){
      return true
    }
    return false
  }
  
    const loginHandler =async ()=>{
      if(!checkRegex()){
        alert("(شماره موبایل و یا ایمیل معتبر وارد کنید.")
        return
      }
   
      console.log(loginOtpRef.current.value)
        const res = await fetch(
          "http://127.0.0.1:8000/api/accounts/login/",
          {
          method: "POST",
           headers: {
          "Content-Type": "application/json",
           }, 
           body : JSON.stringify({
              identifier:emailRef.current.value,
               password:passRef.current.value,
               otp_code: loginOtpRef.current.value
           })
    })

    const result = await res.json();

    if(res.ok){
      alert("باموفقیت وارد شدید.")
      console.log(JSON.stringify(result, null, 2))
      sessionStorage.setItem("access_token", result.data.access_token)
      console.log(sessionStorage.getItem("access_token"))
      login()
      closeModal()
    }
    else{
  
    console.log(JSON.stringify(result, null, 2))
    console.log("FULL RESPONSE:", result);
    alert(JSON.stringify(result.errors, null, 2))
    }
     
  }


    const loginotpHandler=async ()=>{
      if(!checkRegex()){
        alert("شماره موبایل و یا ایمیل معتبر وارد کنید.")
        return
      }
      if(passRef.current.value.length < 8){
         alert("رمز عبور باید حداقل دارای 8 کاراکتر باشد")
        return
      }
      const res = await fetch(
          "http://127.0.0.1:8000/api/accounts/login/otp/request/",
          {
          method: "POST",
           headers: {
          "Content-Type": "application/json",
           }, 
           body : JSON.stringify({
              identifier:emailRef.current.value,
              password:passRef.current.value
           })
    })
      const result = await res.json();
      
      if(res.ok){
        alert(result.data.otp_code_for_test)
      } else{
        alert(result.detail)
      }
      console.log("STATUS:", res.status);
      console.log("ERRORS:", result.errors);
      console.log("FULL RESPONSE:", result);
      
      
    }

   const emailRef= useRef()
   const nameRef= useRef()
   const passRef= useRef()
   const loginOtpRef= useRef()
   const signupOtpRef= useRef()

  return (
    modal &&
     <div className=" wrapper fixed inset-0 z-[100] flex justify-center items-center">
        <div  onClick={closeModal} className="absolute min-h-screen inset-0 bg-black/80" />
        <div className="card-switch">
          
            <span className="slider" />
            <span className="card-side" />
            <div className="flip-card__inner">
              <div className="flip-card__front">
                <div className="title">ورود</div>
                <form className="flip-card__form" action>
                  <input  className="flip-card__input" ref={emailRef} name="email" placeholder="ایمیل یا شماره موبایل" type="" />
                  <input className="flip-card__input" ref={passRef} name="password" placeholder="رمز عبور" type="password" />
                  <div className="flex justify-between gap-2 items-center">
                      <input className=" flip-card__input_code" ref={loginOtpRef} name="password" placeholder="کد ورود" type="" />
                     <button onClick={loginotpHandler} className="flip-card__btn_code" type="button">درخواست کد</button>
                  </div>
                  
                  <button onClick={loginHandler} className="flip-card__btn" type="button">ورود</button>
                </form>
              </div>
          
            </div>
          
        </div>   
      </div>
  );
}
