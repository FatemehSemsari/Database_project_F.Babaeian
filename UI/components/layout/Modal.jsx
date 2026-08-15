"use client"

import { useRef } from "react";

export default function Modal({modal, showModal, closeModal}){

  const checkRegex = ()=>{
    const phoneRegex = /^09\d{9}$/;
    const emailRegex =  /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if(phoneRegex.test(emailRef.current.value) || emailRegex.test(emailRef.current.value)){
      return true
    }
    return false
  }
  
    const loginHandler =async ()=>{
      if(!checkRegex){
        alert("(شماره موبایل و یا ایمیل معتبر وارد کنید.")
        return
      }
   
        const res = await fetch(
          "",
          {
          method: "POST",
           headers: {
          "Content-Type": "application/json",
           }, 
           body : JSON.stringify({
              identifier:emailRef.current.value,
               password:passRef.current.value,
               otp_code: otpRef.current.valyue
           })
    })
      alert(res)

      sessionStorage.setItem("access_token", res.data.access)
  }

    const signupHandler = async()=>{
      const phoneRegex = /^09\d{9}$/;
      if(!checkRegex){
        alert("(شماره موبایل و یا ایمیل معتبر وارد کنید.")
        return
      }

      const name_result = nameRef.current.value.split(/[-\s]/)
      let data
      if (phoneRegex.test(emailRef.current.value)){
         data = {
          first_name: name_result[0],
          last_name: name_result[1],
          phone: emailRef.current.value,
          password: passRef.current.value,
          otp_code: otpRef.current.value  
        }
      } else {
          data = {
          first_name: name_result[0],
          last_name: name_result[1],
          email: emailRef.current.value,
          password: passRef.current.value,
          otp_code: otpRef.current.value  
        }
      }

      const res = await fetch(
          "",
          {
          method: "POST",
           headers: {
          "Content-Type": "application/json",
           }, 
           body : JSON.stringify(data)
    })
      alert(res)
    }

    const signupotpHandler=async ()=>{
      if(!checkRegex){
        alert("(شماره موبایل و یا ایمیل معتبر وارد کنید.")
        return
      }
      let data
       if (phoneRegex.test(emailRef.current.value)){
         data = { 
          phone: emailRef.current.value,
        }
      } else {
          data = {
          email: emailRef.current.value, 
        }
      }

      const res = await fetch(
          "",
          {
          method: "POST",
           headers: {
          "Content-Type": "application/json",
           }, 
           body : JSON.stringify(data)
    })
      alert(res)
    }
    

    const loginotpHandler=async ()=>{
      if(!checkRegex){
        alert("(شماره موبایل و یا ایمیل معتبر وارد کنید.")
        return
      }
      const res = await fetch(
          "",
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
      alert(res)
      
    }

   const emailRef= useRef()
   const nameRef= useRef()
   const passRef= useRef()
   const otpRef= useRef()

  return (
    modal &&
     <div className=" wrapper fixed inset-0 z-[100] flex justify-center items-center">
        <div  onClick={closeModal} className="absolute min-h-screen inset-0 bg-black/80" />
        <div className="card-switch">
          <label className="switch">
            <input type="checkbox" className="toggle" />
            <span className="slider" />
            <span className="card-side" />
            <div className="flip-card__inner">
              <div className="flip-card__front">
                <div className="title">ورود</div>
                <form className="flip-card__form" action>
                  <input  className="flip-card__input" ref={emailRef} name="email" placeholder="ایمیل یا شماره موبایل" type="" />
                  <input className="flip-card__input" ref={passRef} name="password" placeholder="رمز عبور" type="password" />
                  <div className="flex justify-between gap-2 items-center">
                      <input className=" flip-card__input_code" ref={otpRef} name="password" placeholder="کد ورود" type="" />
                     <button onClick={signupHandler} className="flip-card__btn_code">درخواست کد</button>
                  </div>
                  
                  <button onClick={loginHandler} className="flip-card__btn">ورود</button>
                </form>
              </div>
              <div className="flip-card__back">
                <div className="title">ثبت نام</div>
                <form className="flip-card__form" action>
                  <input ref={nameRef} className="flip-card__input" placeholder="نام" type="نام" />
                  <input className="flip-card__input" name="email" ref={emailRef} placeholder="ایمیل یا شماره موبایل" type="" />
                  <input className="flip-card__input" name="password" ref={passRef} placeholder="رمز عبور" type="password" />
                   <div className="flex justify-between gap-2 items-center">
                      <input className=" flip-card__input_code" ref={otpRef} name="password" placeholder="کد ورود" type="" />
                     <button onClick={loginHandler} className="flip-card__btn_code">درخواست کد</button>
                  </div>
                  <button onClick={signupHandler} className="flip-card__btn" >ارسال</button>
                </form>
              </div>
            </div>
          </label>
        </div>   
      </div>
  );
}
