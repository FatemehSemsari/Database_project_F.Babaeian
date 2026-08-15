"use client"
import { useState,useEffect,useRef } from "react"

export default function SupporterProfile(){

    const mockData= [
        {report_id: 1,
    user_id: 12,

    first_name: "زهرا",
    last_name: "احمدی",
    email: "zahra@example.com",
    phone: "09123456789",

    ticket_id: 125,
    reservation_id: 52,

    issue_type: "seat_problem",
    message: "شماره صندلی من اشتباه نمایش داده شده است.",

    status: "pending",

    support_response: null,

    reviewed_by: null,
    reviewed_at: null,

    reviewer_first_name: null,
    reviewer_last_name: null}
    ]

     const issueTypeLabels = {
        purchase_problem: "مشکل خرید",
        payment_problem: "مشکل پرداخت",
        ticket_information: "اطلاعات بلیط",
        pricing_problem: "مشکل قیمت",
        seat_problem: "مشکل صندلی",
        venue_problem: "مشکل ورزشگاه",
        event_time_change: "تغییر زمان مسابقه",
        unexpected_cancellation: "لغو غیرمنتظره",
        other: "سایر",
        };
   
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
    
        setReports(mockData)
    
    },[])
    const [reports, setReports] = useState()
    const resRef= useRef()

    const sendResponse = async ()=>{
        const token = sessionStorage.getItem("access_token")

        const res = await fetch(
         ``, {
            method: "PATCH",
            headers: {},
            body: JSON.stringify({
                status: "resolved",
                support_response: resRef.current.value
            })
         }
        )

        const result = await res.json()
    }

    return(
       reports && <div  className=" items-end flex flex-col gap-3 mt-25 p-5 w-7/12">
            {
                reports.map((report)=>{
                    return <div key={report.report_id} className="p-5 w-full bg-white rounded-b-lg flex flex-row-reverse justify-between items-start">
                                <div dir="rtl" className="flex flex-col gap-2  justify-center items-start">
                                    <h1>اطلاعات کاربر:</h1>
                                    <h3>{report.first_name} {report.last_name}</h3>
                                    <h3> {report.user_id}:id</h3>
                                </div>
                                <div  dir="rtl" className="flex flex-col gap-2 justify-center items-start">
                                    <h1 className="">گزارش:</h1>
                                    <h3>{issueTypeLabels[report.issue_type]}</h3>
                                    <p>{report.message}</p>
                                </div>
                                <div  dir="rtl" className="flex flex-col gap-2  justify-center items-start">
                                    <h1>پاسخ:</h1>
                                    {
                                        report.support_response ? <p>{report.support_response}</p> : <div><input className=" h-15" ref={resRef} placeholder="متن پاسخ" /> <button onClick={sendResponse}>ثبت پاسخ</button> </div>
                                    }
                                </div>
                        </div>
                })
            }
        </div>
    )
}