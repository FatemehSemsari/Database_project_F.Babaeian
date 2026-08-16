"use client"

import Link from "next/link"
import { useEffect, useState } from "react"

export default function SupporterProfileMenu(){

    const logoutHandler=()=>{
        sessionStorage.removeItem("access_token")
        sessionStorage.removeItem("role")
    }
         const getUser =async ()=> {
        const token = sessionStorage.getItem("access_token")
        console.log("TOKEN:", token);
        if(!token){
            alert("ابتدا وارد حساب خود شوید")
             return
        }

        const response = await fetch("http://127.0.0.1:8000/api/accounts/profile/",
        {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        }
    );
        const result = await response.json()
        console.log(result)
        setData(result.data.user)
    }
       useEffect(()=>{
        getUser()
    },[])

    const [data, setData] = useState()


    const mockUser = {
  id: 1,
  first_name: "زهرا",
  last_name: "احمدی",
  email: "zahra@example.com",
  phone: "09123456789",
  role: "user",
  email_verified: true,
  phone_verified: true,
  is_active: true,
  created_at: "2026-08-10T09:30:00Z",
  updated_at: "2026-08-14T16:45:00Z",
};

    return(
       data &&  <div className=" mt-25 rounded-xl shadow-2xl text-white w-2/12 h-auto p-5 bg-[#10243D]">
            <div className=" flex flex-col gap-3 items-center">
                <svg className="  rounded-full p-2 border-2 w-15" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640"><path className=" fill-white" d="M320 312C386.3 312 440 258.3 440 192C440 125.7 386.3 72 320 72C253.7 72 200 125.7 200 192C200 258.3 253.7 312 320 312zM290.3 368C191.8 368 112 447.8 112 546.3C112 562.7 125.3 576 141.7 576L498.3 576C514.7 576 528 562.7 528 546.3C528 447.8 448.2 368 349.7 368L290.3 368z"/></svg>
                <h1>{mockUser.first_name} {data.last_name}</h1>
                <h3 className=" text-sm">{data.email}</h3>
                <h3 className=" text-sm">{data.phone}</h3>
            </div>
             <div className=" w-full bg-amber-50 h-0.25 opacity-30 m-auto mt-5"></div>
            <div className=" flex flex-col gap-3 mt-5 items-end">
                <Link href={"/profile/supporter/"}>گزارش های ثبت شده</Link>
                <Link href={"/profile/supporter/tickets"}> مدیریت بلیط ها</Link>
                 <Link href={"/"}><button onclick={logoutHandler}>خروج از حساب</button></Link>

            </div>
        </div>
    )
}