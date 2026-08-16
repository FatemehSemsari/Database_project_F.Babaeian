"use client"
import { useState, useEffect } from "react"
import { mockReports } from "@/data/mockData"
export default function Reports(){

    useEffect(()=>{
         const getDetails = async ()=>{
        
               const token = sessionStorage.getItem("access_token")
                const response = await fetch("http://127.0.0.1:8000/api/reports/", {
                headers: {
                Authorization: `Bearer ${token}`
            }
            });
            
                const result = await response.json()
        
                console.log(result)
        
            }
        
            setReports(mockReports)
        
    },[])

    const [reports, setReports]=useState()

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
    const reportStatusLabels = {
        pending: "در انتظار بررسی",
        in_review: "در حال بررسی",
        resolved: "حل شده",
        rejected: "رد شده",
        };

    return (
        reports && <div className=" flex flex-wrap gap-3 mt-25 flex-col justify-between p-5 w-7/12">
            {reports.map((report)=>{
                return <div className="bg-white flex flex-row-reverse justify-between items-center rounded-lg w-full p-3">
                        <div dir="rtl" className="w-4/12">
                            <h1 className=" font-bold">{issueTypeLabels[report.issue_type]}</h1>
                            <p className="text-[#64748B]">{report.message}</p>
                        </div>
                        <div className=" flex flex-col gap-2 items-center justify-center">
                            <h1 className="text-[#64748B]">شماره رزرو</h1>
                            <h3>{report.reservation_id}</h3>
                            <h1 className="text-[#64748B]">شماره بلیط</h1>
                            <h3>{report.ticket_id}</h3>
                        </div>
                        <div>
                            <h1 className=" font-bold">پاسخ پشتیبان</h1>
                            <p className="text-[#64748B]"></p>
                        </div>

                    </div>
            })}
        </div>
    )
}