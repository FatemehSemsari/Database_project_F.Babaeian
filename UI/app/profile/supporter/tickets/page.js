"use client"

import { useState,useEffect,useRef } from "react"
import { mockSupportReservations } from "@/data/mockData"
import ModifyModal from "@/components/layout/ModifyModal"
export default function tickets() {

     useEffect(()=>{
        const getDetails = async ()=>{
    
            const token = sessionStorage.getItem("access_token"); 
            const response = await fetch("http://127.0.0.1:8000/api/support/reservations/", {
            headers: {
            Authorization: `Bearer ${token}`
        }
        });
        
            const result = await response.json()
    
            if(response.ok){
                setTickets(result.data.reservations)
            } else{
                console.log(result)
            }
    
        }
        getDetails()
        
    
    },[])
    const [tickets, setTickets] = useState()
    const [id, setId] = useState()
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

    const approvHandler = async (id)=>{
        const token = sessionStorage.getItem("access_token")

        const res = await fetch(
         `http://127.0.0.1:8000/api/support/reservations/${id}/`, {
            method: "PATCH",
            headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
            body: JSON.stringify({
                action: "approve",
                note: "رزرو توسط پشتیبان تایید شد."
            })
         }
        )

        const result = await res.json()
        if(res.ok){
            alert("با موفقیت انجام شد.")
        } else{
            console.log(result)
        }
    }

    const cancellHandler = async (id)=>{
        const token = sessionStorage.getItem("access_token")

        const res = await fetch(
         `http://127.0.0.1:8000/api/support/reservations/${id}/`, {
            method: "PATCH",
            headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
            body: JSON.stringify({
                action: "cancel",
                note: "رزرو توسط پشتیبان لغو شد."
            })
         }
        )

        const result = await res.json()
        if(res.ok){
            alert("با موفقیت انجام شد.")
        } else{
            console.log(result)
        }
    }

    const showModal = async (id)=>{
       setId(id)
        setModal(true)
    }

    const closeModal = async ()=>{
        setModal(false)
        
    }

    const modifyHandler = async (newTime)=>{
        
        const token = sessionStorage.getItem("access_token")

        const res = await fetch(
         `http://127.0.0.1:8000/api/support/reservations/${id}/`, {
            method: "PATCH",
            headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
            body: JSON.stringify({
                action: "modify",
                expires_at: newTime,
                note:"مهلت رزرو تمدید شد"
            })
         }
        )

        const result = await res.json()
        setModal(false)
        if(res.ok){
            alert("با موفقیت انجام شد.")
        } else{
            console.log(result)
        }
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
                                    {ticket.support_reviewed_at ? <div><h1>{resMap[ticket.support_review_status]}</h1> <h3></h3>{ticket.support_note}</div> : <div><button onClick={()=>{approvHandler(ticket.reservation_id)}}>تایید </button>  <button onClick={()=>showModal(ticket.reservation_id)}>اصلاح</button> <button onClick={()=>{cancellHandler(ticket.reservation_id)}}>لغو</button></div>}
                                </div>
                               
                        </div>
                })
            }
        </div>
    )
}