"use client";
import { useRef } from "react";

export default function SendPage(){

    const ticketRef = useRef()
    const reserveRef = useRef()
    const messageRef = useRef()
    const issueRef = useRef()

    const sendReport=async()=>{
        if(!ticketRef.current.value &&issueRef.current.value ){
            alert("شماره بلیط یا کد رزرو را وارد کنید.")
        }
        const token = sessionStorage.getItem("access_token")

        const res = await fetch(
             
                "http://127.0.0.1:8000/api/reports/",
               {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    ticket_id: ticketRef.current.value,
                    reservation_id: reserveRef.current.value,
                    message: issueRef.current.value
                })
               }
            )

            const result = await res.json()
            console.log(result)
            if(res.ok){
                alert("گزارش جدید با موفقیت ثبت شد")
            }
    }

    return(
        <div className="flex flex-col gap-3 items-end flex-wrap mt-25 p-5 w-7/12">
            <h1 className=" w-fit border-b-2 mb-5"> ثبت گزارش جدید</h1>
            <div className="flex flex-row-reverse flex-wrap gap-3">
                <input ref={ticketRef}  placeholder="شماره بلیط"></input>
            <input ref={reserveRef}  placeholder="کد رزرو"></input>
            <select ref={issueRef}>
                <option value={"purchase_problem"}>مشکل خرید</option>
                <option value={"payment_problem"}>مشکل پرداخت</option>
                <option value={"ticket_information"}>اطلاعات بلیط</option>
                <option value={"pricing_problem"}>مشکل قیمت</option>
                <option value={"seat_problem"}>مشکل صندلی</option>
                <option value={"venue_problem"}>مشکل ورزشگاه</option>
                <option value={"event_time_change"}>تغییر زمان مسابقه</option>
                <option value={"unexpected_cancellation"}>لغو غیرمنتطره</option>
                <option value={"other"}>سایر</option>
            </select>
            
            </div>
            <input className="h-30 w-10/12" type="text" ref={messageRef}  placeholder="توضیحات"></input>
            <button onClick={sendReport}>ثبت گزارش</button>
        </div>
    )
}