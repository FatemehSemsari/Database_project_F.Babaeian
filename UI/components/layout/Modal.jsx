"use client"

import { useRef } from "react";

export default function Modal({modal, showModal, closeModal, login}){

  const checkRegex = (log)=>{
    const phoneRegex = /^09\d{9}$/;
    const emailRegex =  /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if(phoneRegex.test(log) || emailRegex.test(log)){
      return true
    }
    return false
  }
  
    const loginHandler =async ()=>{
      if(!checkRegex(logemailRef.current.value)){
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
              identifier:logemailRef.current.value,
               password:logpassRef.current.value,
               otp_code: loginOtpRef.current.value
           })
    })

    const result = await res.json();

    if(res.ok){
      alert("باموفقیت وارد شدید.")
      console.log(JSON.stringify(result, null, 2))
      sessionStorage.setItem("access_token", result.data.access_token)
      sessionStorage.setItem("role", result.data.user.role)
      console.log(sessionStorage.getItem("access_token"))
      login()
      closeModal()
    }
    else{
  
    console.log(JSON.stringify(result, null, 2))
    console.log("FULL RESPONSE:", result);
    alert(JSON.stringify(result.errors, null, 2))
    }
      logemailRef.current.value=""
      loginOtpRef.current.value=""
      logpassRef.current.value=""

     
  }

    const signupHandler = async()=>{
      const phoneRegex = /^09\d{9}$/;
      if(!checkRegex(signemailRef.current.value)){
        alert("(شماره موبایل و یا ایمیل معتبر وارد کنید.")
        return
      }

      const name_result = nameRef.current.value.split(/[-\s]/)
      let data
      if (phoneRegex.test(signemailRef.current.value)){
         data = {
          first_name: name_result[0],
          last_name: name_result[1],
          phone: signemailRef.current.value,
          password: signpassRef.current.value,
          otp_code: signupOtpRef.current.value  
        }
      } else {
          data = {
          first_name: name_result[0],
          last_name: name_result[1],
          email: signemailRef.current.value,
          password: signpassRef.current.value,
          otp_code: signupOtpRef.current.value  
        }
      }

      const res = await fetch(
          "http://127.0.0.1:8000/api/accounts/signup/",
          {
          method: "POST",
           headers: {
          "Content-Type": "application/json",
           }, 
           body : JSON.stringify(data)
    })
     const result = await res.json();
     if(res.ok){
      alert("حساب کاربری با موفقیت ساخته شد.")
     }
     else{
      alert(result.errors.detail)
     }
      console.log("STATUS:", res.status);
console.log("ERRORS:", result.errors);
console.log("FULL RESPONSE:", result);
      

      nameRef.current.value=""
      signemailRef.current.value=""
      signupOtpRef.current.value=""
      signpassRef.current.value=""


    }

    const signupotpHandler=async ()=>{
      if(!checkRegex(signemailRef.current.value)){
        alert("(شماره موبایل و یا ایمیل معتبر وارد کنید.")
        return
      }
      if(signpassRef.current.value.length < 8){
         alert("رمز عبور باید حداقل دارای 8 کاراکتر باشد")
        return
      }
      const phoneRegex = /^09\d{9}$/;
      let data
       if (phoneRegex.test(signemailRef.current.value)){
         data = { 
          phone: signemailRef.current.value,
        }
      } else {
          data = {
          email: signemailRef.current.value, 
        }
      }

      const res = await fetch(
        
          "http://127.0.0.1:8000/api/accounts/signup/otp/request/",
          {
          method: "POST",
           headers: {
          "Content-Type": "application/json",
           }, 
           body : JSON.stringify(data)
    })
      const result = await res.json();
      console.log("STATUS:", res.status);
console.log("ERRORS:", result.errors);
console.log("FULL RESPONSE:", result);
      if(res.ok){
         alert(result.data.otp_code_for_test)
      } else{
        alert(result.detail)
      }
    }
    

    const loginotpHandler=async ()=>{
      if(!checkRegex(logemailRef.current.value)){
        alert("شماره موبایل و یا ایمیل معتبر وارد کنید.")
        return
      }
      if(logpassRef.current.value.length < 8){
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
              identifier:logemailRef.current.value,
              password:logpassRef.current.value
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

   const logemailRef= useRef()
   const signemailRef= useRef()
   const nameRef= useRef()
   const logpassRef= useRef()
   const signpassRef= useRef()
   const loginOtpRef= useRef()
   const signupOtpRef= useRef()

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
                  <input  className="flip-card__input" ref={logemailRef} name="email" placeholder="ایمیل یا شماره موبایل" type="" />
                  <input className="flip-card__input" ref={logpassRef} name="password" placeholder="رمز عبور" type="password" />
                  <div className="flex justify-between gap-2 items-center">
                      <input className=" flip-card__input_code" ref={loginOtpRef} name="password" placeholder="کد ورود" type="" />
                     <button onClick={loginotpHandler} className="flip-card__btn_code" type="button">درخواست کد</button>
                  </div>
                  
                  <button onClick={loginHandler} className="flip-card__btn" type="button">ورود</button>
                </form>
              </div>
              <div className="flip-card__back">
                <div className="title">ثبت نام</div>
                <form className="flip-card__form" action>
                  <input ref={nameRef} className="flip-card__input" placeholder="نام" type="نام" />
                  <input className="flip-card__input" name="email" ref={signemailRef} placeholder="ایمیل یا شماره موبایل" type="" />
                  <input className="flip-card__input" name="password" ref={signpassRef} placeholder="رمز عبور" type="password" />
                   <div className="flex justify-between gap-2 items-center">
                      <input className=" flip-card__input_code" ref={signupOtpRef} name="password" placeholder="کد ورود" type="" />
                     <button onClick={signupotpHandler} className="flip-card__btn_code" type="button">درخواست کد</button>
                  </div>
                  <button onClick={signupHandler} className="flip-card__btn" type="button">ارسال</button>
                </form>
              </div>
            </div>
          </label>
        </div>   
      </div>
  );
}
