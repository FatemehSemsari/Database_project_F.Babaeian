"use client"

import { useState,useEffect,useRef } from "react"
import { mockSupportReservations } from "@/data/mockData"
import ModifyModal from "@/components/layout/ModifyModal"
export default function tickets() {

     useEffect(()=>{
        // const getDetails = async ()=>{
    
        //     // const token = 
        //     const response = await fetch("", {
        //     headers: {
        //     Authorization: `Bearer ${token}`
        // }
        // });
        
        //     const result = await response.json()
    
        //     return result.data.active
    
        // }
    
        setTickets(mockSupportReservations)
    
    },[])
    const [tickets, setTickets] = useState()
    const [modal, setModal] = useState(false)
    const resRef= useRef()
    const reserveMap = {
        pending: "در انتظار پرداخت",
        paid:"پرداخت شده",
        expired:"منقضی شده",
        cancelled:"لغو شده"
    }

     const resMap = {
        approved: "تایید شده",
        modified:"ویرایش شده",
        cancelled:"لغو شده"
    }

    const approvHandler = async ()=>{
        const token = sessionStorage.getItem("access_token")

        const res = await fetch(
         ``, {
            method: "PATCH",
            headers: {},
            body: JSON.stringify({
                action: "approve",
                note: "رزرو توسط پشتیبان تایید شد."
            })
         }
        )

        const result = await res.json()
    }

    const cancellHandler = async ()=>{
        const token = sessionStorage.getItem("access_token")

        const res = await fetch(
         ``, {
            method: "PATCH",
            headers: {},
            body: JSON.stringify({
                action: "cancel",
                note: "رزرو توسط پشتیبان لغو شد."
            })
         }
        )

        const result = await res.json()
    }

    const showModal = async ()=>{
        setModal(true)
    }

    const closeModal = async ()=>{
        setModal(false)
    }

    const modifyHandler = async (newTime)=>{

        const token = sessionStorage.getItem("access_token")

        const res = await fetch(
         ``, {
            method: "PATCH",
            headers: {},
            body: JSON.stringify({
                action: "modify",
                expires_at: newTime,
                note:"مهلت رزرو تمدید شد"
            })
         }
        )

        const result = await res.json()
        setModal(false)
    }

    
    return(
       tickets && <div  className=" items-end flex flex-col gap-3 mt-25 p-5 w-7/12">
           { modal && <ModifyModal closeModal={closeModal} modify={modifyHandler}/>}
            {
                tickets.map((ticket)=>{
                    return <div key={ticket.user_id} className="p-5 w-full bg-white rounded-b-lg flex flex-row-reverse justify-between items-start">
                                <div dir="rtl" className="flex flex-col gap-2  justify-center items-start">
                                    <h1>اطلاعات کاربر:</h1>
                                    <h3>{ticket.first_name} {ticket.last_name}</h3>
                                    <h3> {ticket.user_id}شماره کاربری :</h3>
                                </div>

                                 <div dir="rtl" className="flex flex-col gap-2  justify-center items-start">
                                    <h1>اطلاعات بلیط:</h1>
                                    <h3>{ticket.home_team_name} - {ticket.away_team_name}</h3>
                                    <h3>{ticket.event_datetime}</h3>
                                    <h3>{reserveMap[ticket.reservation_status]}</h3>
                                </div>

                                <div dir="rtl" className="flex flex-col gap-2  justify-center items-start">
                                    <h1>وضعیت بررسی:</h1>
                                    {ticket.support_reviewed_at ? <div><h1>{resMap[ticket.support_review_status]}</h1> <h3></h3>{ticket.support_note}</div> : <div><button onClick={approvHandler}>تایید </button>  <button onClick={showModal}>اصلاح</button> <button onClick={cancellHandler}>لغو</button></div>}
                                </div>
                               
                        </div>
                })
            }
        </div>
    )
}