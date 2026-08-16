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
        const token = sessionStorage.getItem("access_token")
        console.log(token)
         const res = await fetch(
                "http://127.0.0.1:8000/api/accounts/profile/",
               {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    first_name: firstNameRef.current.value,
                    last_name: lastNameRef.current.value
                })
               }
            )

            const result = await res.json()

            console.log(result)
            if(res.ok){
                 alert("با موفقیت تغییر یافت.")
            }
            
    }

    const editPass = async()=>{
        if(newpassRef.current.value != confirmpassRef.current.value){
             alert("تکرار رمز عبور جدید با رمز عبور جدید یکسان نیست.")
             return
        }

        const token = sessionStorage.getItem("access_token")

         const res = await fetch(
                "http://127.0.0.1:8000/api/accounts/profile/password/change/",
               {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    current_password: passRef.current.value,
                    new_password: newpassRef.current.value,
                    new_password_confirm: confirmpassRef.current.value
                })
               }
            )

            const result = await res.json()
            console.log(result)
            if(res.ok){
                 alert("با موفقیت تغییر یافت.")
                 passRef.current.value=""
                 newpassRef.current.value=""
                 confirmpassRef.current.value=""

            } else{
                alert(result.errors.new_password)
            }
           
    }

    const editPhone =async()=>{
        
        const token = sessionStorage.getItem("access_token")
          if(!phoneOtpRef.current.value){
            alert("لطفا کد otp را وارد کنید.")
            return
        }
        const res = await fetch(
                "http://127.0.0.1:8000/api/accounts/profile/contact-change/confirm/",
               {
                 method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    identifier_type: "phone",
                    new_identifier: phoneRef.current.value,
                    otp_code: phoneOtpRef.current.value
                })
               }
            )

            const result = await res.json()
            if(res.ok){
                 alert("با موفقیت تغییر یافت.")
                 phoneOtpRef.current.value=""
                 phoneRef.current.value=""
                 phonePassRef.current.value=""

            } else{
                alert(result.errors)
            }
    }

    const editEmail =async()=>{
        const token = sessionStorage.getItem("access_token")
         if(!emailOtpRef.current.value){
            alert("لطفا کد otp را وارد کنید.")
            return
        }
        const res = await fetch(

                "http://127.0.0.1:8000/api/accounts/profile/contact-change/confirm/",
               {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    identifier_type: "email",
                    new_identifier: emailRef.current.value,
                    otp_code: emailOtpRef.current.value
                })
               }
            )

            const result = await res.json()

              if(res.ok){
                 alert("با موفقیت تغییر یافت.")
                 emailOtpRef.current.value=""
                 emailPassRef.current.value=""
                 emailOtpRef.current.value=""

            } else{
                alert(result.errors)
            }
    }

     const phoneOtpReauest =async()=>{
         const token = sessionStorage.getItem("access_token")
        if(!phoneRef.current.value || !phonePassRef.current.value){
            alert("لطفا برای درخواست کد ابتدا شماره موبایل و رمز عبور خود را وارد کنید")
            return
        }
        const res = await fetch(
                "http://127.0.0.1:8000/api/accounts/profile/contact-change/otp/request/",
               {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    identifier_type: "phone",
                    new_identifier: phoneRef.current.value,
                    password: phonePassRef.current.value
                })
               }
            )

             const result = await res.json()
            console.log(result.data.otp_code_for_test)
            if(res.ok){
                alert(`otp code is: ${result.data.otp_code_for_test}`)
            } else{
                console.log(result)
            }
    }

     const emailOtpReauest =async()=>{
         const token = sessionStorage.getItem("access_token")
        if(!emailRef.current.value || !emailPassRef.current.value){
            alert("لطفا برای درخواست کد ابتدا ایمیل و رمز عبور خود را وارد کنید")
            return
        }
        const res = await fetch(
                "http://127.0.0.1:8000/api/accounts/profile/contact-change/otp/request/",
               {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    identifier_type: "email",
                    new_identifier: emailRef.current.value,
                    password: emailPassRef.current.value
                })
               }
            )

          
            const result = await res.json()
            console.log(result.data.otp_code_for_test)
            if(res.ok){
                alert(`otp code is: ${result.data.otp_code_for_test}`)
            } else{
                console.log(result)
            }
            

        
    }

   return(
     <div className=" items-end flex flex-col gap-3 mt-25 p-5 w-7/12">
       <div className=" flex flex-col items-end gap-2">
            <h1>ویرایش نام</h1>
            <input ref={firstNameRef} placeholder="نام" type="text"/>
            <input ref={lastNameRef} placeholder=" نام خانوداگی" type="text"/>
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