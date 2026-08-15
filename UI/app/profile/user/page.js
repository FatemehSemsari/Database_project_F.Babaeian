"use client";
import { useRef } from "react";
export default function UserProfile(){

    const firstNameRef =useRef()
    const lastNameRef =useRef()
    const passRef =useRef()
    const newpassRef =useRef()
    const confirmpassRef =useRef()
    const phoneRef =useRef()
    const phonePassRef =useRef()
    const phoneOtpRef =useRef()
    const emailRef =useRef()
    const emailPassRef =useRef()
    const emailOtpRef =useRef() 

    const editName =async ()=>{
         const res = await fetch(
                "",
               {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    // Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    first_name: firstNameRef.current.value,
                    last_name: lastNameRef.current.value
                })
               }
            )

            const result = await res.json()

            alert("با موفقیت تغییر یافت.")
    }

    const editPass = async()=>{
        if(newpassRef.current.value != confirmpassRef.current.value){
             alert("تکرار رمز عبور جدید با رمز عبور جدید یکسان نیست.")
             return
        }

         const res = await fetch(
                "",
               {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    // Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    current_password: passRef.current.value,
                    new_password: newpassRef.current.value,
                    new_password_confirm: confirmpassRef.current.value
                })
               }
            )

            const result = await res.json()

            alert("با موفقیت تغییر یافت.")
    }

    const editPhone =async()=>{
          if(!phoneOtpRef.current.value){
            alert("لطفا کد otp را وارد کنید.")
            return
        }
        const res = await fetch(
                "",
               {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    // Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    identifier_type: "phone",
                    new_identifier: phoneRef.current.value,
                    otp_code: phoneOtpRef.current.value
                })
               }
            )

            const result = await res.json()

            alert("با موفقیت تغییر یافت.")
    }

    const editEmail =async()=>{
         if(!emailOtpRef.current.value){
            alert("لطفا کد otp را وارد کنید.")
            return
        }
        const res = await fetch(
                "",
               {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    // Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    identifier_type: "email",
                    new_identifier: emailRef.current.value,
                    otp_code: emailOtpRef.current.value
                })
               }
            )

            const result = await res.json()

            alert("با موفقیت تغییر یافت.")
    }

     const phoneOtpReauest =async()=>{
        
        if(!phoneRef.current.value || phonePassRef.current.value){
            alert("لطفا برای درخواست کد ابتدا شماره موبایل و رمز عبور خود را وارد کنید")
            return
        }
        const res = await fetch(
                "",
               {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    // Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    identifier_type: "phone",
                    new_identifier: phoneRef.current.value,
                    password: phonePassRef.current.value
                })
               }
            )

            const result = await res.json()

            alert("otp code is:")
    }

     const emailOtpReauest =async()=>{
        
        if(!emailRef.current.value || emailPassRef.current.value){
            alert("لطفا برای درخواست کد ابتدا شماره موبایل و رمز عبور خود را وارد کنید")
            return
        }
        const res = await fetch(
                "",
               {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    // Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    identifier_type: "email",
                    new_identifier: emailRef.current.value,
                    password: emailPassRef.current.value
                })
               }
            )

            const result = await res.json()

            alert("otp code is:")
    }

   return(
     <div className=" items-end flex flex-col gap-3 mt-25 p-5 w-7/12">
       <div className=" flex flex-col items-end gap-2">
            <h1>ویرایش نام</h1>
            <input ref={firstNameRef} placeholder="نام و نام خانوداگی" type="text"/>
            <input ref={lastNameRef} placeholder="نام و نام خانوداگی" type="text"/>
            <button onClick={editName}>ویرایش</button>
       </div>
        <div  className=" flex flex-col items-end gap-2">
        <h1>ویرایش رمز عبور</h1>
            <input ref={passRef} placeholder="رمز عبور فعلی" />
            <input ref={newpassRef} placeholder="رمز عبور جدید" />
            <input ref={confirmpassRef} placeholder="تکرار رمز عبور جدید " />
            <button onClick={editPass}>ویرایش</button>
       </div>
        <div className=" flex flex-col items-end gap-2">
        <h1 >افزودن یا ویرایش شماره موبایل </h1>
            <input ref={phoneRef} placeholder="شماره موبایل" />
            <input ref={phonePassRef} placeholder="رمز عبور " />
            <div >
                <input ref={phoneOtpRef} placeholder="کد ارسال شده" />
                <button onClick={phoneOtpReauest}>دریافت کد</button>
            </div>
             <button onClick={editPhone}>ویرایش</button>

       </div>
       <div className=" flex flex-col items-end gap-2">
        <h1 >افزودن یا ویرایش ایمیل  </h1>
            <input ref={emailRef} placeholder="ایمیل " />
            <input ref={emailPassRef} placeholder="رمز عبور " />
            <div>
                <input ref={emailOtpRef}placeholder="کد ارسال شده" />
                <button onClick={emailOtpReauest}>دریافت کد</button>
            </div>
       </div>
        <button onClick={editEmail}>ویرایش</button>
    </div>
   )
}